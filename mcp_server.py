from mcp.server.fastmcp import FastMCP
from intent_parser import parse_intent
from aggregator import aggregate_sum
from monday_client import query_board
from groq_client import call_llm
import os

mcp = FastMCP("Monday-BI-Agent")


@mcp.tool()
def query_bi(question: str):
    """Query business intelligence across Monday boards"""

    intent = parse_intent(question)

    board_id = os.getenv("DEALS_BOARD_ID")
    data = query_board(board_id)

    result = aggregate_sum(data, intent["field"])

    insight = call_llm([
        {"role": "system", "content": "You are a CFO."},
        {"role": "user", "content": f"Result: {result}. Provide insight."}
    ])

    return {
        "result": result,
        "insight": insight,
        "intent": intent
    }