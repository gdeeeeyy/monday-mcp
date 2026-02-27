import os
import json
from dotenv import load_dotenv
from groq import Groq
from monday_client import query_board

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b" #"llama-3.1-8b-instant" 


# ============================
# CALL GROQ
# ============================
def call_llm(messages):

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=600
    )

    return response.choices[0].message.content


# ============================
# DECIDE TOOL
# ============================
def decide_tool(question):

    messages = [
        {"role": "system", "content": """
You are a BI agent.

Available tools:
- fetch_deals
- fetch_work_orders

Respond ONLY with:
CALL_TOOL: fetch_deals
CALL_TOOL: fetch_work_orders
or
NO_TOOL
"""},

        {"role": "user", "content": question}
    ]

    decision = call_llm(messages)

    if "fetch_deals" in decision:
        return "fetch_deals"
    if "fetch_work_orders" in decision:
        return "fetch_work_orders"

    return None


# ============================
# EXECUTE TOOL
# ============================
def execute_tool(tool):

    if tool == "fetch_deals":
        return query_board(os.getenv("DEALS_BOARD_ID"))

    if tool == "fetch_work_orders":
        return query_board(os.getenv("WORK_BOARD_ID"))

    return None


# ============================
# FINAL REASONING
# ============================
def final_answer(question, data):

    messages = [
        {"role": "system", "content": "You are a senior BI financial analyst."},
        {"role": "user", "content": question},
        {"role": "assistant", "content": f"Here is the board data:\n{json.dumps(data)}"}
    ]

    return call_llm(messages)


# ============================
# CLI
# ============================
if __name__ == "__main__":

    print("\n⚡ Groq BI Agent\n")

    while True:

        q = input("Ask: ")

        if q.lower() in ["exit", "quit"]:
            break

        tool = decide_tool(q)

        if tool:
            print(f"\n🔧 Using {tool}")
            data = execute_tool(tool)
            answer = final_answer(q, data)
        else:
            answer = call_llm([{"role": "user", "content": q}])

        print("\n📊 Answer:\n")
        print(answer)
        print("\n" + "-"*60)