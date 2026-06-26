import requests
import pandas as pd
import os
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# --- Path to the CSV ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # folder of this script
csv_path = os.path.join(BASE_DIR, "../data/1000_companies.csv")  # go up one folder to data

# --- Load the CSV ---
if os.path.exists(csv_path):
    companies_df = pd.read_csv(csv_path)
    print(f"Loaded {len(companies_df)} companies from CSV.")
else:
    companies_df = pd.DataFrame()  # empty DataFrame if CSV not found
    print("CSV not found, companies_df is empty.")

def fetch_live_data():
    """
    Fetch live startup news from NewsAPI
    """
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "startup funding OR startup investment",
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data.get("articles", [])

def get_company_info(company_name):
    """
    Search the loaded CSV for a company by name
    """
    if companies_df.empty:
        return f"No company data available."
    
    result = companies_df[companies_df['Company Name'].str.lower() == company_name.lower()]
    
    if result.empty:
        return f"Company '{company_name}' not found."
    
    return result.to_dict(orient="records")[0]  # return first matching company as dict