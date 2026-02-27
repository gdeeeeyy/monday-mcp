from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from agent import run_agent_stream

app = FastAPI()

class Query(BaseModel):
    session_id: str
    question: str

@app.post("/query/stream")
async def query_stream(q: Query):

    return StreamingResponse(
        run_agent_stream(q.session_id, q.question),
        media_type="text/plain"
    )

@app.get("/")
async def root():
    return {"status": "AI BI Backend Live 🚀"}