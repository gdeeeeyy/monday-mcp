memory_store = {}

def get_memory(session_id):
    return memory_store.get(session_id, "")

def update_memory(session_id, user_input):
    existing = memory_store.get(session_id, "")
    memory_store[session_id] = existing + "\nUser: " + user_input