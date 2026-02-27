# Decision Log – Monday.com AI BI Agent

## Project Overview

The goal of this project was to build a live, AI-powered business intelligence agent that integrates directly with monday.com boards, retrieves real-time data, and provides conversational analytics through a deployed web application.

The system needed to:

- Connect securely to monday.com using their GraphQL API
- Fetch data live (no preloading or caching)
- Expose tools through an MCP-compatible server
- Use an LLM to generate revenue and pipeline insights
- Support streaming responses
- Ask clarifying questions when needed
- Support follow-up conversational context
- Be fully deployable to Render

This document explains the key technical and architectural decisions made during implementation.

---

# Core Architecture & Data Decisions

## 1. Live Query-Time Fetching (No Caching)

One of the most important design decisions was to avoid preloading or caching monday board data at server startup.

Instead, I implemented live query-time fetching:

- Every time a relevant user query is processed,
- A fresh GraphQL request is sent directly to monday.com,
- The latest board data is retrieved and passed to the LLM.

### Why this approach?

- Ensures always up-to-date revenue and pipeline data.
- Reflects immediate board edits.
- Avoids cache invalidation complexity.
- Aligns closer to how real BI dashboards function.
- Keeps the system simpler and more predictable.

This decision significantly improves reliability and correctness in business analytics scenarios.

---

## 2. Modular Backend Architecture

The backend was structured into clear modules instead of combining all logic into one file.

### Backend Modules

- `monday_client.py` → Handles GraphQL API calls
- `tool_router.py` → Maps user intent to appropriate board tools
- `agent.py` → Orchestrates tool execution + LLM interaction
- `groq_client.py` → Handles streaming LLM responses
- `memory.py` → Maintains session context
- `mcp_server.py` → Exposes tools in MCP format
- `main.py` → FastAPI entry point

This separation ensures:

- Clean debugging
- Easy future upgrades
- Replaceable memory backend (Redis-ready)
- Scalability
- Production readiness

Keeping modules focused reduced coupling and made testing easier.

---

## 3. LLM Choice & Integration Strategy

Initially, Claude was planned. However, I used Groq’s OpenAI-compatible OSS model for the following reasons:

- Strong streaming support
- Low latency
- Compatible with OpenAI-style tool calls
- Good balance between reasoning quality and speed

The LLM is invoked only after tools fetch real data. The model does not hallucinate board content — it reasons strictly over retrieved data.

---

## 4. MCP Compatibility

I implemented an MCP server layer so the monday tools can be exposed to external AI systems.

This ensures:

- Expandability beyond this frontend
- Compatibility with advanced AI clients
- Tool transparency
- Future multi-agent integration readiness

Even though the Streamlit frontend calls the backend directly, the MCP layer keeps the architecture future-proof.

---

# Interaction Design & UX Decisions

## 5. Streaming Responses

Rather than waiting for a full response from the LLM, I implemented streaming token output.

This improves:

- User experience
- Perceived speed
- Transparency
- Debug visibility

Responses are streamed through a FastAPI `StreamingResponse` endpoint and rendered live in Streamlit.

---

## 6. Tool / API Trace Visibility

To improve transparency and debugging clarity, the agent streams tool traces before and after execution.

For example:

- 🔍 Parsing intent
- 🔧 Fetching LIVE data from monday.com
- 📊 Data received
- 🤖 Generating answer

These traces are shown directly in the UI.

This serves two purposes:

1. Improves user trust
2. Makes the system easier to debug in production

It clearly distinguishes:

- Data retrieval
- Reasoning
- LLM generation

---

## 7. Clarifying Question Handling

Business questions can be ambiguous (e.g., “What’s total revenue?”).

To handle ambiguity:

- The agent checks for incomplete parameters (e.g., timeframe, board scope).
- Instead of guessing, it asks a follow-up clarification.
- The session waits for user input before continuing.

This makes the system more professional and prevents misleading analytics.

---

## 8. Follow-Up Context Support

Each user session is assigned a unique session ID.

Conversation history is stored per session and sent along with future prompts.

This enables:

- Drill-down analytics
- Iterative refinement
- Multi-turn BI conversations

Example flow:

User: “What’s the pipeline value?”
User: “Now break it by sector.”
User: “Filter only this month.”

The system retains context and applies the necessary logic incrementally.

---

## 9. Deployment Decisions

I deployed:

- Backend → FastAPI service on Render
- Frontend → Streamlit service on Render

These are completely separate services, communicating via HTTPS.

Environment variables are securely configured within Render.

Additionally:

- Python version was forced to 3.11 to avoid dependency build issues.
- No sensitive data is committed to the repository.
- The architecture allows easy migration to Redis, Docker, or containerized deployments.

---

## Time Spent

Approximately 20 hours were spent across:

- Initial board setup and schema validation
- GraphQL integration and debugging
- Live fetching logic implementation
- Streaming backend setup
- Frontend streaming client implementation
- Render deployment troubleshooting
- Final testing and refinement

---

## Final Status

The application is:

- Fully functional
- Live-fetching (no caching)
- Streaming-enabled
- Trace-transparent
- Context-aware
- Modular
- Deployed
- Production-ready in structure

The architecture is intentionally designed to support future scaling into a more advanced enterprise BI assistant.

---
