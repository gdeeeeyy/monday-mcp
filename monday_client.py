import requests
from config import MONDAY_API_KEY

URL = "https://api.monday.com/v2"

HEADERS = {
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json"
}


def query_board(board_id):
    query = """
    query ($board_id: ID!) {
      boards(ids: [$board_id]) {
        items_page(limit: 100) {
          items {
            name
            column_values {
              id
              text
            }
          }
        }
      }
    }
    """

    response = requests.post(
        URL,
        headers=HEADERS,
        json={"query": query, "variables": {"board_id": board_id}}
    )

    return response.json()