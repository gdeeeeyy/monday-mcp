import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
MONDAY_API_URL = "https://api.monday.com/v2"


def query_board(board_id: str):
    """
    Fetches live board data from monday.com
    Flattens the GraphQL structure
    Returns clean structured rows + metadata
    """

    if not MONDAY_API_KEY:
        raise Exception("MONDAY_API_KEY not found in environment variables")

    timestamp = datetime.datetime.utcnow().isoformat()

    print("\n[TRACE] ===== MONDAY API CALL START =====")
    print(f"[TRACE] Board ID: {board_id}")
    print(f"[TRACE] Timestamp (UTC): {timestamp}")

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 100) {{
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

    print(f"[TRACE] HTTP Status Code: {response.status_code}")

    if response.status_code != 200:
        raise Exception(f"Monday API request failed: {response.text}")

    data = response.json()

    # Safety check
    boards = data.get("data", {}).get("boards", [])
    if not boards:
        print("[TRACE] No boards found or invalid Board ID.")
        return {"rows": [], "meta": {}}

    items = boards[0].get("items_page", {}).get("items", [])

    print(f"[TRACE] Raw Items Retrieved: {len(items)}")
    #flatten
    cleaned_rows = []

    for item in items:
        row = {
            "item_id": item["id"],
            "name": item["name"]
        }

        for col in item["column_values"]:
            row[col["id"]] = col["text"]

        cleaned_rows.append(row)

    print(f"[TRACE] Flattened Rows Created: {len(cleaned_rows)}")
    print("[TRACE] ===== MONDAY API CALL END =====\n")

    return {
        "rows": cleaned_rows,
        "meta": {
            "rows_retrieved": len(cleaned_rows),
            "api_called_at": timestamp
        }
    }