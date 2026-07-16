import streamlit as st
import requests
import uuid

# Configuration
# Note: Since the webhook is not yet activated/published in n8n, 
# you might need to use /webhook-test/chat for testing if it's inactive,
# or /webhook/chat if you have clicked "Active" in the n8n UI.
WEBHOOK_URL = "https://laurel-fraternal-subsonic.ngrok-free.dev/webhook/chat"
# If testing without activating, uncomment below:
# WEBHOOK_URL = "https://laurel-fraternal-subsonic.ngrok-free.dev/webhook-test/chat"

st.set_page_config(page_title="Sales Assistant AI", page_icon="📈")
st.title("📈 Sales Data Assistant")
st.markdown("Ask me anything about Matriderm and Natrox sales, or specific employee performance!")

# Initialize session state for memory
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask about sales data..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Prepare payload for n8n Webhook
    payload = {
        "sessionId": st.session_state.session_id,
        "chatInput": prompt
    }

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        try:
            # Send request to n8n
            response = requests.post(WEBHOOK_URL, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                # The 'Respond to Webhook' node returns {"output": "..."}
                ai_response = data.get("output", "Sorry, I didn't receive a valid response from the AI.")
            else:
                ai_response = f"Error: n8n returned status code {response.status_code}. (Did you activate the workflow?)"
                
        except requests.exceptions.Timeout:
            ai_response = "Error: The request timed out. The AI agent took too long to respond."
        except Exception as e:
            ai_response = f"Error: Failed to connect to n8n webhook. Details: {str(e)}"
            
        message_placeholder.markdown(ai_response)
        
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
