from intent_parser import parse_intent
from fastapi import FastAPI
from mcp_server import mcp

app = FastAPI()

# Mount MCP
app.mount("/mcp", mcp.sse_app())

@app.get("/")
async def root():
    return {"status": "Groq + MCP BI Agent running 🚀"}

@app.post("/query")
def query_api(payload: dict):

    question = payload["question"]

    intent = parse_intent(question)

    return {
        "intent": intent
    }