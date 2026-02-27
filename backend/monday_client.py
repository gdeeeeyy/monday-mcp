import requests
from config import MONDAY_API_KEY

MONDAY_URL = "https://api.monday.com/v2"

def query_monday(graphql_query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(
        MONDAY_URL,
        json={"query": graphql_query},
        headers=headers,
    )

    return response.json()

def fetch_board_items(board_id):
    query = f"""
    query {{
      boards(ids: {board_id}) {{
        items_page(limit: 200) {{
          items {{
            name
            column_values {{
              text
            }}
          }}
        }}
      }}
    }}
    """

    # 🔥 LIVE FETCH
    return query_monday(query)