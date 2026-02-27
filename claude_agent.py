import os
import re
import json
from anthropic import Anthropic
from dotenv import load_dotenv
from monday_client import query_board
import os

load_dotenv()
# Setup
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

claude = Anthropic(api_key=ANTHROPIC_API_KEY)

def execute_tool(tool_name):

    if tool_name == "fetch_deals":
        return query_board(os.getenv("DEALS_BOARD_ID"))

    if tool_name == "fetch_work_orders":
        return query_board(os.getenv("WORK_BOARD_ID"))

    return None

# Tool Definitions (For Claude Prompt)
TOOLS_DESCRIPTION = """
You are a Business Intelligence agent.

You have access to these tools:

1. fetch_deals()
   → Returns live deal funnel data in clean JSON format.

2. fetch_work_orders()
   → Returns live work order data in clean JSON format.

When you need data, respond EXACTLY in this format:

CALL_TOOL: fetch_deals
OR
CALL_TOOL: fetch_work_orders

Do not explain. Just write the CALL_TOOL line.
"""

# Step 1 — Ask Claude what to do
def ask_claude_for_tool(user_query: str):

    prompt = f"""
{TOOLS_DESCRIPTION}

User Question:
{user_query}
"""

    response = claude.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.content[0].text.strip()
    return text

# Step 2 — Detect Tool Call
def extract_tool_call(response_text):

    match = re.search(r"CALL_TOOL:\s*(\w+)", response_text)

    if match:
        return match.group(1)

    return None

# Step 3 — Execute MCP Tool
def execute_tool(tool_name):

    if tool_name == "fetch_deals":
        return mcp.call("fetch_deals")

    if tool_name == "fetch_work_orders":
        return mcp.call("fetch_work_orders")

    return None

# Step 4 — Final Claude Reasoning
def generate_final_answer(user_query, tool_data):

    prompt = f"""
You are a senior BI analyst.

User question:
{user_query}

Here is the live data:
{json.dumps(tool_data, indent=2)}

Provide a clear business explanation with insights.
"""

    response = claude.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=800,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text

# Main Agent Function
def run_claude_agent(user_query):

    # Ask Claude which tool to call
    tool_decision = ask_claude_for_tool(user_query)

    tool_name = extract_tool_call(tool_decision)

    if tool_name:
        print(f"🔧 Tool Called: {tool_name}")

        tool_data = execute_tool(tool_name)

        final_answer = generate_final_answer(user_query, tool_data)

        return final_answer

    else:
        # If no tool required, just respond normally
        return tool_decision