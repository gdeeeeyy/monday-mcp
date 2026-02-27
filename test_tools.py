from monday_client import query_board
import os
from dotenv import load_dotenv
import json

load_dotenv()

print("\n====== FIRST 5 DEALS ======\n")
deals = query_board(os.getenv("DEALS_BOARD_ID"))
print(json.dumps(deals, indent=2))

print("\n====== FIRST 5 WORK ORDERS ======\n")
work_orders = query_board(os.getenv("WORK_BOARD_ID"))
print(json.dumps(work_orders, indent=2))