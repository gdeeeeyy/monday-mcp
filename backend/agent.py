from tool_router import route_tools
from groq_client import stream_llm
from memory import get_memory, update_memory
import json

async def run_agent_stream(session_id, user_input):

    memory = get_memory(session_id)

    yield "🔍 Parsing intent...\n"

    tool = route_tools(user_input)

    if tool:
        yield "🔧 Fetching LIVE data from monday.com...\n"

        data = tool()  # 🔥 LIVE CALL

        yield "📊 Data received.\n"

        context = f"""
        Conversation History:
        {memory}

        LIVE Data:
        {json.dumps(data)}
        """

    else:
        yield "🧠 No tool needed.\n"
        context = memory

    # Clarifying Question Example
    if "revenue" in user_input.lower() and "timeframe" not in user_input.lower():
        yield "\n❓ Are you asking about current month revenue or full pipeline revenue?\n"
        return

    yield "\n🤖 Generating answer...\n\n"

    async for token in stream_llm(user_input, context):
        yield token

    update_memory(session_id, user_input)