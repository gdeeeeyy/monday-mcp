from langchain_agent import run_agent

while True:
    q = input("\nAsk BI Agent: ")
    if q.lower() == "exit":
        break

    print("\n📊 Answer:\n")
    print(run_agent(q))