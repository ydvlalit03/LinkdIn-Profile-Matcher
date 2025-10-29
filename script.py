from pydantic import BaseModel
import json
import re
from typing import Optional
from typing_extensions import TypedDict
import requests
from bs4 import BeautifulSoup

user_agents = [
    "Slackbot-LinkExpanding 1.0 (+https://api.slack.com/robots)",
    "LinkedInBot/1.0",
    "Twitterbot/1.0",
    "facebookexternalhit/1.1",
    "WhatsApp/2.0",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]

import itertools
user_agent_cycle = itertools.cycle(user_agents)


def mimic_bot_headers() -> str:
    """
    Mimic bot headers
    """

    # Cycle through user agents
    return next(user_agent_cycle)


def get_first_last_name(name: str) -> tuple[str, Optional[str]]:
    """
    Extracts first and last name from full name
    """

    name_parts = name.split(" ")
    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else None

    return first_name, last_name


class Workspace(TypedDict):
    name: str
    url: Optional[str]


class LinkedinPersonProfile(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    linkedin: Optional[str]
    workspaces: Optional[list[Workspace]]




class LinkedinCompanyProfile(BaseModel):
    name: Optional[str]
    website: Optional[str]
    description: Optional[str]
    address: Optional[str]
    number_of_employees: Optional[int]



class LinkedInProvider:
    """
    Get data from linkedin URL using web scraping
    """

    def _fetch_data(self, url: str) -> Optional[str]:
        retry_count = 3

        for _ in range(retry_count):
            user_agent = mimic_bot_headers()

            headers = {
                "User-Agent": user_agent,
            }

            proxies = {
                "https": "http://brd-customer-hl_6c1f36a6-zone-datacenter_proxy2:1qyqs0lnh5zi@brd.superproxy.io:33335",
                "http": "http://brd-customer-hl_6c1f36a6-zone-datacenter_proxy2:1qyqs0lnh5zi@brd.superproxy.io:33335",
            }

            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
            )

            if response.status_code == 200:
                return response.text

        print(
            f"Failed to fetch the linkedin URL: {url}",
        )

    def _json_ld_data(self, html_content: str) -> Optional[dict]:
        try:
            # Parse HTML content
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract JSON-LD script content
            script_tag = soup.find("script", {"type": "application/ld+json"})
            json_ld_data = json.loads(script_tag.string) if script_tag else {}
            return json_ld_data
        except Exception as e:
            print(f"Error in extracting JSON-LD data: {e}")

    def person_profile(self, url: str) -> Optional[LinkedinPersonProfile]:
        """
        Profile details of a person
        """

        try:
            url = url

            html_content = self._fetch_data(url)

            if not html_content:
                return

            data_obj_test = extract_profile_data(html_content)
            json_ld_data = self._json_ld_data(html_content)

            if json_ld_data:
                # Extract information for type "Person"
                if json_ld_data.get("@type") == "ProfilePage":
                    person_data = json_ld_data["mainEntity"]
                else:
                    person_data = next(
                        (
                            item
                            for item in json_ld_data["@graph"]
                            if item["@type"] == "Person"
                        ),
                        {},
                    )

                name = person_data.get("name", None)
                workplaces = [
                    {
                        "name": org.get("name"),
                        "url": org.get("url", None),
                    }
                    for org in person_data.get("worksFor", [])
                    if "name" in org
                ]

                first_name, last_name = (
                    get_first_last_name(name) if name else (None, None)
                )

                return LinkedinPersonProfile(
                    first_name=first_name,
                    last_name=last_name,
                    linkedin=url,
                    workspaces=workplaces,
                ), data_obj_test

        except Exception as e:
            print(f"Error in extracting person profile: {e}")

    def company_profile(self, username: str) -> Optional[LinkedinCompanyProfile]:
        """
        Profile details of a company
        """
        try:
            url = f"https://www.linkedin.com/company/{username}"

            html_content = self._fetch_data(url)

            if not html_content:
                return

            json_ld_data = self._json_ld_data(html_content)

            if json_ld_data:
                # Extract information for type "Organization"
                if json_ld_data.get("@type") == "ProfilePage":
                    organization_data = json_ld_data["mainEntity"]
                else:
                    organization_data = next(
                        (
                            item
                            for item in json_ld_data["@graph"]
                            if item["@type"] == "Organization"
                        ),
                        {},
                    )

                name = organization_data.get("name", None)
                website = organization_data.get("sameAs", None)
                description = organization_data.get("description", None)
                number_of_employees = organization_data.get(
                    "numberOfEmployees", {}
                ).get("value", None)

                # Extract address details
                address_dict = organization_data.get("address", {})
                street = address_dict.get("streetAddress", None)
                locality = address_dict.get("addressLocality", None)
                region = address_dict.get("addressRegion", None)
                postal_code = address_dict.get("postalCode", None)
                country = address_dict.get("addressCountry", None)

                address_parts = [street, locality, region, postal_code, country]
                address = ", ".join(filter(None, address_parts))

                return LinkedinCompanyProfile(
                    name=name,
                    website=website,
                    description=description,
                    address=address,
                    number_of_employees=number_of_employees,
                )
        except Exception as e:
            print(f"Error in extracting company profile: {e}")


def extract_profile_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    data = {}

    name_tag = soup.find('h1', class_=lambda x: x and 'top-card-layout__title' in x)
    data["name"] = name_tag.get_text(strip=True) if name_tag else None

        # Try to find the location under the name/headline section
    name_section = soup.find('div', class_=lambda x: x and 'top-card-layout__entity-info' in x)
    location = None
    if name_section:
        possible_spans = name_section.find_all('span')
        for span in possible_spans:
            txt = span.get_text(strip=True)
            if re.search(r'\b[A-Za-z]+,\s+[A-Za-z]+(?:,\s+[A-Za-z]+)?\b', txt):
                location = txt
                break
    data["location"] = location

    canonical = soup.find('link', rel="canonical")
    data["profileUrl"] = canonical['href'] if canonical and canonical.get('href') else None

    profile_img = soup.find('img', alt=data["name"])
    if profile_img:
        data["profileImage"] = profile_img.get('data-delayed-url') or profile_img.get('src')
    else:
        data["profileImage"] = None

    about_section = soup.find('section', class_=lambda x: x and 'summary' in x)
    if about_section:
        p_about = about_section.find('p')
        data["about"] = p_about.get_text(strip=True) if p_about else None
    else:
        data["about"] = None

    exp_items = []
    exp_section = soup.find('section', attrs={"data-section": "experience"})
    if exp_section:
        for li in exp_section.find_all('li', class_=lambda x: x and 'experience-item' in x):
            company = None
            location = None
            company_tag = li.find('span', class_=lambda x: x and 'experience-item__subtitle' in x)
            if company_tag:
                company = company_tag.get_text(strip=True)
            location_tag = li.find('p', class_=lambda x: x and 'experience-item__meta-item' in x)
            if location_tag:
                location = location_tag.get_text(strip=True)
            if company or location:
                exp_items.append({
                    "company": company,
                    "location": location
                })
    data["experience"] = exp_items

    edu_items = []
    edu_section = soup.find('section', attrs={"data-section": "educationsDetails"})
    if edu_section:
        for li in edu_section.find_all('li', class_=lambda x: x and 'education__list-item' in x):
            institution = None
            period = None
            description = None
            inst_link = li.find('a', href=re.compile("school"))
            if inst_link:
                institution = inst_link.get_text(strip=True)
            period_tag = li.find('span', class_=lambda x: x and 'date-range' in x)
            if period_tag:
                period = period_tag.get_text(strip=True)
            desc_div = li.find('div', class_=lambda x: x and 'show-more-less-text' in x)
            if desc_div:
                description = desc_div.get_text(" ", strip=True)
            edu_items.append({
                "institution": institution,
                "period": period,
                "description": description
            })
    data["education"] = edu_items

    languages = []
    lang_section = soup.find('section', class_=lambda x: x and 'languages' in x)
    if lang_section:
        for li in lang_section.find_all('li'):
            language = None
            proficiency = None
            lang_name_tag = li.find('h3')
            prof_tag = li.find('h4')
            if lang_name_tag:
                language = lang_name_tag.get_text(strip=True)
            if prof_tag:
                proficiency = prof_tag.get_text(strip=True)
            if language:
                languages.append({"language": language, "proficiency": proficiency})
    data["languages"] = languages

    recommendations_received = None
    rec_section = soup.find('section', class_=lambda x: x and 'recommendations' in x)
    if rec_section:
        rec_text = rec_section.get_text(" ", strip=True)
        m = re.search(r"(\d+)\s+people\s+have\s+recommended", rec_text)
        if m:
            recommendations_received = int(m.group(1))
    data["recommendationsReceived"] = recommendations_received

    return data


def transform_data(data,complete_data) :
    original_data = complete_data

    # Prepare transformed data
    transformed_data = {
        "name": original_data.get("name"),
        "image": original_data.get("profileImage"),
        "intro": "",
        "timezone": None,
        "company_industry": None,
        "company_size": None,
        "social_profile": []
    }

    # Build intro text
    about = original_data.get("about", "")
    first_experience = next((exp for exp in original_data.get("experience", []) if exp.get("company")), None)
    if first_experience:
        company_name = first_experience.get("company")
        intro_text = f"{about} {company_name} "
    else:
        intro_text = about
    if(intro_text==None):
      transformed_data["intro"] = None
    else:
      transformed_data["intro"] = intro_text.strip()
    transformed_data["timezone"]  = complete_data.get("location")
    def get_company_url (data):
        return data.workspaces[0]['url']

    def scrape_company_details(company_url: str):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        response = requests.get(company_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch {company_url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        company_details = {"url": company_url}

        try:
            industry_tag = soup.find("dt", string=lambda text: text and "Industry" in text)
            if industry_tag:
                industry_value = industry_tag.find_next_sibling("dd")
                company_details["industry"] = industry_value.get_text(strip=True) if industry_value else None
            else:
                company_details["industry"] = None

            size_tag = soup.find("dt", string=lambda text: text and "Company size" in text)
            if size_tag:
                size_value = size_tag.find_next_sibling("dd")
                company_details["company_size"] = size_value.get_text(strip=True) if size_value else None
            else:
                company_details["company_size"] = None

        except Exception as e:
            print(f"Error extracting company data: {e}")
            return None

        return company_details
    company_url = None
    company_industry = None
    company_size = None

    if hasattr(data, 'workspaces') and isinstance(data.workspaces, list) and len(data.workspaces) > 0:
        workspace = data.workspaces[0]
        if isinstance(workspace, dict) and 'url' in workspace and workspace['url']:
            company_url = workspace['url']
            if isinstance(company_url, str) and company_url.startswith(("http://", "https://")):
                company_data = scrape_company_details(company_url)
                company_industry = company_data.get("industry") if company_data else None
                company_size = company_data.get("company_size") if company_data else None

    return transformed_data

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-mpnet-base-v2')

## Module to compare Images
from transformers import BeitFeatureExtractor, BeitModel
from PIL import Image
import requests
from io import BytesIO
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load BEiT model and feature extractor
feature_extractor = BeitFeatureExtractor.from_pretrained('microsoft/beit-base-patch16-224')
modeli = BeitModel.from_pretrained('microsoft/beit-base-patch16-224')

def fix_google_drive_url(url):
    if "drive.google.com" in url and "/file/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return url

def load_image(input_data):
    if isinstance(input_data, str) and input_data.startswith("http"):
        input_data = fix_google_drive_url(input_data)
        response = requests.get(input_data)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(input_data).convert('RGB')
    return image
def extract_features(image):
    """
    Tokenizes image and extracts feature embeddings using BEiT.
    """
    inputs = feature_extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = modeli(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()  # global feature vector

def calculate_similarity(image1_input, image2_input):
    """
    Calculates cosine similarity between two images.
    """
    image1 = load_image(image1_input)
    image2 = load_image(image2_input)

    features1 = extract_features(image1)
    features2 = extract_features(image2)

    similarity = cosine_similarity(features1, features2)[0][0]
    return similarity

def safe_text(value):
    return value if value is not None else ""

# Compare field by field
def scores(fields,encoded_profile1,encoded_profile2,person):
  sum=0.0
  score=0.0
  for field in fields:
    if(person[field]==None):
      continue
    emb1 = encoded_profile1[field].reshape(1, -1)
    emb2 = encoded_profile2[field].reshape(1, -1)
    similarity = cosine_similarity(emb1, emb2)[0][0]
    score+=similarity*weights[field]
    sum+=weights[field]
    # print(f"{field} similarity: {similarity:.4f}")
  return (sum,score)

# %pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tempfile
import shutil
import time
def prepare_query(persona):
    fields_to_use = ['name', 'intro', 'timezone', 'company_industry', 'company_size']
    query_parts = []

    for field in fields_to_use:
        value = persona.get(field)
        if value and isinstance(value, str):
            # Remove URLs and anything in parentheses (e.g., links or extra info)
            cleaned = re.sub(r'\(.*?\)', '', value)  # remove anything in parentheses
            cleaned = re.sub(r'https?://\S+', '', cleaned)  # remove URLs
            cleaned = cleaned.strip()
            if cleaned:
                query_parts.append(cleaned)

    # Join fields and add search hint + site restriction
    query = ' '.join(query_parts)
    query += ' LinkedIn profile site:linkedin.com/in/'

    # Clean extra spaces
    query = ' '.join(query.split())
    return query

def filter_linkedin_profiles(links):
    linkedin_profiles = []
    for link in links:
        if "linkedin.com/in/" in link:
            linkedin_profiles.append(link)
    return linkedin_profiles

def search_linkedin_profiles_selenium(query, max_results=5):
    # Create a temp directory to avoid conflicts with existing Chrome sessions
    temp_profile = tempfile.mkdtemp()

    options = Options()
    options.add_argument("--headless")  # run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument(f"--user-data-dir={temp_profile}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(f"https://www.bing.com/search?q={query}")
        time.sleep(2)  # wait for page to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "linkedin.com/in/" in href and href not in links:
                links.append(href)
            if len(links) >= max_results:
                break

        return filter_linkedin_profiles(links)

    finally:
        driver.quit()
        shutil.rmtree(temp_profile)  # Always clean up!

fields = ['name', 'intro', 'timezone', 'company_industry', 'company_size']
weights={'name':0.2,'intro':0.15,'timezone':0.1,'company_industry':0.2,'company_size':0.1}
sum = 0.75
weight_of_image_if_positive = 0.35
weight_of_image_if_negative = 0.1
