from mcp.server.fastmcp import FastMCP
from monday_client import query_board
import os


mcp = FastMCP("monday-bi-agent")

#Both of these triggers actual API calls to monday.com
@mcp.tool()
def fetch_deals():
    """
    Fetch live Deals board data from monday.com.
    """
    board_id = os.getenv("DEALS_BOARD_ID")
    return query_board(board_id)


@mcp.tool()
def fetch_work_orders():
    """
    Fetch live Work Orders board data from monday.com.
    """
    board_id = os.getenv("WORK_BOARD_ID")
    return query_board(board_id)

if __name__ == "__main__":
    mcp.run()