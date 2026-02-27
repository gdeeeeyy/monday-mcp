import streamlit as st
import requests
import uuid

BACKEND = "https://your-backend.onrender.com/query/stream"

st.title("⚡ Live AI BI Agent")

if "session" not in st.session_state:
    st.session_state.session = str(uuid.uuid4())

prompt = st.chat_input("Ask about revenue, pipeline, sectors...")

if prompt:
    with st.chat_message("assistant"):
        placeholder = st.empty()
        response_text = ""

        with requests.post(
            BACKEND,
            json={
                "session_id": st.session_state.session,
                "question": prompt
            },
            stream=True
        ) as r:

            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    response_text += chunk.decode()
                    placeholder.markdown(response_text)