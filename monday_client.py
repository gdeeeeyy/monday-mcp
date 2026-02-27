import requests
import os
import json
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
MONDAY_API_URL = "https://api.monday.com/v2"


# ======================================================
# FETCH BOARD DATA
# ======================================================

def fetch_board(board_id: str):

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        columns {{
          id
          title
          type
        }}
        items_page(limit: 500) {{
          items {{
            id
            name
            column_values {{
              id
              text
              value
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        MONDAY_API_URL,
        json={"query": query},
        headers={"Authorization": MONDAY_API_KEY}
    )

    if response.status_code != 200:
        raise Exception(response.text)

    board = response.json()["data"]["boards"][0]
    return board["columns"], board["items_page"]["items"]


# ======================================================
# SAFE VALUE EXTRACTOR
# ======================================================

def extract_value(col_obj):

    if col_obj["text"]:
        return col_obj["text"]

    if col_obj["value"]:
        try:
            parsed = json.loads(col_obj["value"])
            if isinstance(parsed, dict):
                return list(parsed.values())[0]
            return parsed
        except:
            return col_obj["value"]

    return None


# ======================================================
# AUTO NORMALIZER BASED ON COLUMN TYPE + TITLE
# ======================================================

def auto_clean(value, title):

    if not value:
        return None

    title = title.lower()

    # Date detection
    if "date" in title:
        try:
            return pd.to_datetime(value).date().isoformat()
        except:
            return None

    # Money detection
    if any(word in title for word in ["amount", "value", "rupees"]):
        try:
            return float(str(value).replace(",", ""))
        except:
            return 0.0

    # Probability mapping
    if "prob" in title:
        val = str(value).strip().lower()
        return {"high": 75.0, "medium": 50.0, "low": 25.0}.get(val, 0.0)

    # Quantity detection
    if "quantity" in title:
        try:
            return int(float(value))
        except:
            return 0

    # Status / sector formatting
    if "status" in title or "sector" in title:
        return str(value).strip().title()

    # Default
    return str(value).strip()


# ======================================================
# GENERIC BOARD NORMALIZATION
# ======================================================

def normalize_board(board_id: str, limit=5):

    columns, items = fetch_board(board_id)

    # Build id -> title map
    id_to_title = {col["id"]: col["title"] for col in columns}

    normalized = []

    for item in items[:limit]:

        row = {"deal_name": item["name"]}

        for col in item["column_values"]:

            title = id_to_title.get(col["id"])
            if not title:
                continue

            clean_key = title.lower().strip().replace(" ", "_").replace("/", "_")
            value = extract_value(col)

            row[clean_key] = auto_clean(value, title)

        normalized.append(row)

    return normalized


# ======================================================
# ENTRY POINT
# ======================================================

def query_board(board_id: str):
    return normalize_board(board_id, limit=5)