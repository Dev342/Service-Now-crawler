import requests
import json
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

INSTANCE = os.getenv("SERVICENOW_INSTANCE")  # e.g., https://your-instance.service-now.com
USERNAME = os.getenv("SERVICENOW_USERNAME")
PASSWORD = os.getenv("SERVICENOW_PASSWORD")

AUTH = HTTPBasicAuth(USERNAME, PASSWORD)
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Safety flag: READ-ONLY mode (do not modify records)
READ_ONLY = True  # Keep True for safe crawling

# Tables to crawl (replace/extend with your own)
TABLES = [
    "incident",
    "kb_knowledge",
    "sys_user",
    "sys_app_module",
    # Add your own custom tables here, e.g., "x_company_custom_table"
]

def crawl_table(table, limit=500):
    """Fetch up to `limit` records from a ServiceNow table and save to output/{table}.json"""
    if not READ_ONLY:
        print(f"[!] WRITE MODE ENABLED — Skipping table: {table}")
        return

    url = f"{INSTANCE}/api/now/table/{table}?sysparm_limit={limit}"
    try:
        res = requests.get(url, auth=AUTH, headers=HEADERS, timeout=60)
        res.raise_for_status()
        data = res.json().get("result", [])
        os.makedirs("output", exist_ok=True)
        with open(os.path.join("output", f"{table}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[✓] Fetched {len(data)} records from {table}")
    except Exception as e:
        print(f"[!] Failed to fetch {table}: {e}")

def crawl_user_inputs():
    """Example: fetch selected fields from the incident table."""
    if not READ_ONLY:
        print("[!] WRITE MODE ENABLED — Skipping user input crawl")
        return

    table = "incident"  # Change if your ticket table differs
    fields = "number,short_description,description,comments,work_notes,caller_id,impact,urgency,state"
    url = f"{INSTANCE}/api/now/table/{table}?sysparm_limit=100&sysparm_fields={fields}"
    try:
        res = requests.get(url, auth=AUTH, headers=HEADERS, timeout=60)
        res.raise_for_status()
        data = res.json().get("result", [])
        os.makedirs("output", exist_ok=True)
        with open(os.path.join("output", "user_inputs_sample.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[✓] Pulled {len(data)} user-submitted records into output/user_inputs_sample.json")
    except Exception as e:
        print(f"[!] Failed to pull user inputs: {e}")

def main():
    for table in TABLES:
        crawl_table(table)
    crawl_user_inputs()

if __name__ == "__main__":
    main()
