from claude_agent import run_claude_agent

while True:
    query = input("\nAsk BI Agent: ")

    if query.lower() == "exit":
        break

    result = run_claude_agent(query)
    print("\n📊 Answer:\n")
    print(result)