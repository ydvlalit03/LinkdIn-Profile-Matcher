# LinkedIn Profile Matcher

A tool for finding and comparing LinkedIn profiles to identify potential **B2B sales leads**, by computing similarity scores between profiles using both semantic text matching and image recognition.

---

## Overview

The tool:

1. Extracts detailed information from LinkedIn profiles
2. Transforms raw profile data into a structured format
3. Compares profiles using semantic similarity + image recognition
4. Ranks the most similar profiles for lead generation

---

## How It Works

### Data Extraction
- Web scraping with rotating user agents
- Structured parsing of profile pages with BeautifulSoup (personal info, work history, education)

### Profile Analysis
- Normalizes unstructured profiles into a standard schema, enriched with company info
- **Semantic text similarity** via sentence transformers
- **Image similarity** via the BEiT vision model on profile pictures

### Search & Matching
- Builds intelligent search queries from profile fields
- Weighted scoring across multiple fields, combining text + image similarity

---

## Tech Stack

- **Scraping**: requests, BeautifulSoup, rotating user agents
- **NLP**: sentence-transformers (semantic similarity)
- **Vision**: BEiT (image similarity)
- **Language**: Python 3.8+

---

## Quick Start

```bash
git clone https://github.com/ydvlalit03/LinkdIn-Profile-Matcher.git
cd LinkdIn-Profile-Matcher
pip install -r requirements.txt
python script.py
```

---

## Disclaimer

For **educational purposes only**. Scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement) — use responsibly and at your own risk.
