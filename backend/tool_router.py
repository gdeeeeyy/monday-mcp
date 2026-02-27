from monday_client import fetch_board_items
from config import DEALS_BOARD_ID, WORK_BOARD_ID

def route_tools(user_input):

    if "pipeline" in user_input.lower():
        return lambda: fetch_board_items(DEALS_BOARD_ID)

    if "sector" in user_input.lower():
        return lambda: fetch_board_items(WORK_BOARD_ID)

    return None