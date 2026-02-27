import json
from groq_client import call_llm

def parse_intent(question, memory_context=""):

    system_prompt = """
Return ONLY valid JSON:

{
  "boards": ["deals" | "work_orders"],
  "aggregation": "sum" | "count",
  "field": "amount_in_rupees_(incl_of_gst)_(masked)",
  "filters": {},
  "clarification_needed": false
}
"""

    response = call_llm([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:{memory_context}\nQuestion:{question}"}
    ])

    return json.loads(response)