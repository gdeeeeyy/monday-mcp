from mcp.server.fastmcp import FastMCP
from monday_client import query_board
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("business-intelligence-agent")

#Both of these triggers actual API calls to monday.com
@mcp.tool()
def fetch_deals():
    """Fetch live Deals board data"""
    board_id = os.getenv("DEALS_BOARD_ID")
    return query_board(board_id, "deals")


@mcp.tool()
def fetch_work_orders():
    """Fetch live Work Orders board data"""
    board_id = os.getenv("WORK_BOARD_ID")
    return query_board(board_id, "work_orders")


if __name__ == "__main__":
    mcp.run()