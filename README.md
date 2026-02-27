# Monday App Integration

This project connects our monday.com boards to a Python-based MCP server, cleans the data, and prepares it for LLM-powered analysis.

## What Was Done

### 1. Board Setup

- Imported Deal Funnel and Work Order Tracker boards into monday.com.
- Verified column structures and data consistency.

### 2. API Integration

- Generated monday.com API key.
- Connected via GraphQL API.
- Successfully fetched board schema and items.

### 3. MCP Setup

- Installed FastMCP.
- Created:
  - `monday_client.py` → Handles API calls + data normalization
  - `mcp_server.py` → Exposes tools
  - `test_tool.py` → Testing script

### 4. Data Cleaning & Normalization

Instead of hardcoding column names, the system:

- Reads column titles dynamically
- Extracts both text and raw value
- Cleans:
  - Dates → ISO format
  - Amounts → Floats
  - Probabilities → Numeric scores
  - Status/Sector → Standardized text

Returns clean JSON (limited to 5 rows per board during testing).  
This prevents repeated null values and makes the system flexible to schema changes.

### 5. LLM Plan

- Planning to use Claude as the LLM. - So I've used groq's open-ai oss model for this kinda works well.
- MCP tools will provide clean data to the LLM.
- LLM will generate analytics like pipeline summaries and revenue insights.

### 6. Hosting Plan

- Intend to deploy on Render.

## Current Status

- Boards connected -> Done
- API working -> Done
- MCP tools created -> Done
- Data normalized -> Done
- LLM integration -> Progressing
- Deployment -> pending
