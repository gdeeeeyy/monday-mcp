import os
from dotenv import load_dotenv
from monday_client import query_board

from langchain_community.chat_models import ChatOllama
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

load_dotenv()

# TOOLS
def fetch_deals_fn(_):
    return str(query_board(os.getenv("DEALS_BOARD_ID")))

def fetch_work_orders_fn(_):
    return str(query_board(os.getenv("WORK_BOARD_ID")))

tools = [
    Tool(
        name="fetch_deals",
        func=fetch_deals_fn,
        description="Use for deals, revenue, pipeline, sector, probability, deal status."
    ),
    Tool(
        name="fetch_work_orders",
        func=fetch_work_orders_fn,
        description="Use for work orders, execution status, receivables, billing."
    ),
]

# MODEL
llm = ChatOllama(
    model="llama3",   # better tool reasoning
    temperature=0
)

# REACT PROMPT (explicit)
react_template = """
You are a business intelligence assistant.

You have access to the following tools:

{tools}

Use this format:

Question: the input question
Thought: think about what to do
Action: the tool name
Action Input: input to the tool
Observation: result of the tool
... (repeat Thought/Action/Observation as needed)
Final Answer: the final answer to the original question

Begin!

Question: {input}
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(react_template)

# AGENT
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
)

# RUN FUNCTION
def run_agent(query: str):
    result = agent_executor.invoke({"input": query})
    return result["output"]