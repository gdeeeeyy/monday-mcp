import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONDAY_API_KEY = os.getenv("MONDAY_API_KEY")
DEALS_BOARD_ID = os.getenv("DEALS_BOARD_ID")
WORK_BOARD_ID = os.getenv("WORK_BOARD_ID")

MONDAY_API_URL = "https://api.monday.com/v2"


def query_board(board_id: str):
    """Generic function to fetch board items live from monday.com"""

    timestamp = datetime.datetime.utcnow().isoformat()

    print(f"\n[TRACE] Monday API Call Initiated")
    print(f"[TRACE] Board ID: {board_id}")
    print(f"[TRACE] Timestamp (UTC): {timestamp}")

    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page {{
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
        raise Exception("Monday API request failed")

    data = response.json()

    item_count = len(
        data["data"]["boards"][0]["items_page"]["items"]
    )

    print(f"[TRACE] Items Retrieved: {item_count}")
    print("[TRACE] Monday API Call Completed\n")

    return {
        "timestamp": timestamp,
        "item_count": item_count,
        "raw_data": data
    }