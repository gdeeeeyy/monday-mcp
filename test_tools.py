import json
from mcp_server import fetch_deals

result = fetch_deals()
#a bit cleaned up output for easier reading
print("META:")
print(json.dumps(result["meta"], indent=2))

print("\nSAMPLE ROWS:")
print(json.dumps(result["rows"][:2], indent=2))