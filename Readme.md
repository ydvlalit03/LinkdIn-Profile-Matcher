# LinkedIn Profile Matcher

A powerful tool for finding and comparing LinkedIn profiles to identify potential B2B sales leads by calculating similarity scores between profiles.

## About Recepto

Recepto is a B2B sales lead generation platform that identifies buying intent from various online channels. The platform collects unstructured data, structures it, and uses it to enrich a database of millions of people profiles. Through sophisticated algorithms, Recepto defines the relevance and strength of buying intent based on a variety of factors..

## Project Overview

This tool is designed to:
1. Extract detailed information from LinkedIn profiles
2. Transform raw profile data into a structured format
3. Compare profiles using semantic similarity metrics and image recognition
4. Identify the most similar profiles for potential lead generation

## Technical Approach

Our approach combines several advanced techniques:

### Data Extraction
- Uses web scraping with rotating user agents to mimic different bots
- Extracts structured data from LinkedIn profile pages using BeautifulSoup
- Captures personal information, work history, education, and more

### Profile Analysis
- Converts unstructured profile data into standardized formats
- Enriches profiles with additional company information
- Implements semantic text comparison using sentence transformers
- Uses image recognition with BEiT model for profile picture similarity

### Search and Matching
- Performs intelligent search queries based on profile information
- Uses weighted scoring system across multiple profile fields
- Combines text and image similarity for comprehensive matching

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/NeevaditVerma/NLP_GCTech_PS.git
cd linkedin-profile-matcher
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

⚠️ **Note:** This tool is for **educational purposes only**. Web scraping LinkedIn may violate their [Terms of Service](https://www.linkedin.com/legal/user-agreement). Use responsibly and at your own risk.
