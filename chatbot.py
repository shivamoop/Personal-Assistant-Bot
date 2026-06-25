import streamlit as st
import requests

st.set_page_config(page_title="Local n8n AI Chat", page_icon="💻")
st.title("💻 Local Chat Client -> Local n8n")

# Pointing directly to your local n8n test webhook endpoint
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/9f9ef009-70b3-40b7-a448-44b0f78b5fa6"

# Initialize Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_prompt := st.chat_input("Type something to send to n8n..."):
    # Render user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Send request to local n8n
    with st.chat_message("assistant"):
        with st.spinner("Waiting for local n8n execution..."):
            try:
                payload = {"chatInput": user_prompt}
                
                # Direct local POST request
                response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
                response.raise_for_status()
                
                # Parse JSON payload from n8n response
                raw_data = response.json()
                
                # If your n8n Respond to Webhook node uses a different key than "response",
                # it will show the raw JSON data so we can see exactly what n8n returned.
                bot_reply = raw_data.get("response", f"Received data: {raw_data}")
                
            except requests.exceptions.RequestException as e:
                bot_reply = f"💥 Could not connect to n8n: {str(e)}"

            st.markdown(bot_reply)
            
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})