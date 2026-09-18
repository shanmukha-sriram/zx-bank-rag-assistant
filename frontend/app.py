import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/chat")

st.set_page_config(page_title="ZX Bank AI Knowledge Assistant", layout="centered")
st.title("ZX Bank AI Knowledge Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "citations" in message and message["citations"]:
            with st.expander("Sources & Citations"):
                for cite in message["citations"]:
                    st.write(f"- **Source:** {cite.get('source')} | **Section:** {cite.get('section')}")

# Chat input bar
if prompt := st.chat_input("Ask a question about ZX Bank..."):
    # Append user question to history
    user_message = {"role": "user", "content": prompt}
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend passing history payload
    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                # Include history in payload
                payload = {
                    "question": prompt,
                    "history": st.session_state.messages # Sends past turns
                }
                
                response = requests.post(API_URL, json=payload, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer generated.")
                    citations = data.get("citations", [])

                    st.markdown(answer)

                    if citations:
                        with st.expander("Sources & Citations"):
                            for cite in citations:
                                st.write(f"- **Source:** {cite.get('source')} | **Section:** {cite.get('section')}")

                    # Update history
                    st.session_state.messages.append(user_message)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "citations": citations
                    })
                else:
                    st.error(f"Error {response.status_code}: Could not retrieve response.")
            except Exception as e:
                st.error(f"Failed to connect to API server: {e}")