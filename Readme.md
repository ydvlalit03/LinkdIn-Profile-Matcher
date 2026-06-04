<div align="center">

# 🔗 LinkedIn Profile Matcher

### Find and rank similar LinkedIn profiles for B2B lead generation — text + image similarity

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-semantic-FFD21E?style=flat-square&logo=huggingface&logoColor=black)
![BEiT](https://img.shields.io/badge/BEiT-image_similarity-6A5ACD?style=flat-square)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-scraping-43B02A?style=flat-square)

</div>

---

## 📖 Overview

**LinkedIn Profile Matcher** finds and compares LinkedIn profiles to surface potential **B2B sales leads**. Given a reference profile, it scrapes and structures candidate profiles, then scores how similar they are using both **semantic text matching** and **profile-picture image recognition** — combining the two into a single weighted relevance score for lead generation.

> Built around the kind of buying-intent lead-enrichment problem platforms like Recepto tackle: take unstructured profile data, structure it, and rank it by relevance.

---

## 📑 Table of Contents

- [What it does](#-what-it-does)
- [How it works](#-how-it-works)
- [Tech stack](#-tech-stack)
- [Installation](#-installation)
- [Disclaimer](#-disclaimer)

---

## 🎯 What it does

1. **Extracts** detailed information from LinkedIn profiles
2. **Transforms** raw profile data into a structured format
3. **Compares** profiles using semantic similarity + image recognition
4. **Ranks** the most similar profiles for potential lead generation

---

## 🔄 How it works

### 🕸️ Data extraction
- Web scraping with **rotating user agents** to mimic different clients
- Structured parsing of profile pages with **BeautifulSoup** — captures personal info, work history, education and more

### 🧬 Profile analysis
- Normalizes unstructured profiles into a standard schema, enriched with company information
- **Semantic text similarity** via sentence transformers
- **Image similarity** via the **BEiT** vision model on profile pictures

### 🔍 Search & matching
- Builds intelligent search queries from profile fields
- Applies a **weighted scoring system** across multiple fields
- Combines text + image similarity into one comprehensive match score

---

## 🛠️ Tech stack

| Concern | Technology |
|---------|------------|
| **Scraping** | requests, BeautifulSoup, rotating user agents |
| **Text similarity** | sentence-transformers (semantic embeddings) |
| **Image similarity** | BEiT vision model |
| **Language** | Python 3.8+ |

---

## 📦 Installation

### Prerequisites
- Python 3.8+ and pip

```bash
git clone https://github.com/ydvlalit03/LinkdIn-Profile-Matcher.git
cd LinkdIn-Profile-Matcher
pip install -r requirements.txt
python script.py
```

---

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Web scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). Use responsibly and at your own risk.
