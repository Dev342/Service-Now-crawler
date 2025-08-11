# ServiceNow Data Crawler (Read-Only)

A secure, **read-only** Python crawler that exports data from ServiceNow tables to structured JSON files.

## Features
- Crawls multiple tables via the ServiceNow REST API
- Stores outputs in `output/` as `{table}.json`
- Uses environment variables (`.env`) for credentials
- Ships with safe **READ_ONLY** mode enabled

## Quick Start
1) Create and populate a `.env` file (see `.env.example`):
```
SERVICENOW_INSTANCE=https://your-instance.service-now.com
SERVICENOW_USERNAME=your_username
SERVICENOW_PASSWORD=your_password
```

2) Install dependencies:
```
pip install -r requirements.txt
```

3) Run the crawler:
```
python crawler.py
```

Outputs will be saved to the `output/` folder.

## Customizing Tables
Edit the `TABLES` list in `crawler.py` to include any tables you want:
```python
TABLES = [
    "incident",
    "kb_knowledge",
    "sys_user",
    "sys_app_module",
    # "x_company_custom_table",
]
```

## Notes
- Do **not** commit real credentials. Use `.env` locally and keep it out of source control.
- This project is intended for read-only data pulls; it does not modify records.
