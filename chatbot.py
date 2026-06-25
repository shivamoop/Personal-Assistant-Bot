import streamlit as st
import requests
import json
import uuid

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


# ------------------------------
# Streamlit Page Config
# ------------------------------
st.set_page_config(
    page_title="Personal AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Personal AI Assistant")

# ------------------------------
# n8n Webhook URL
# ------------------------------
N8N_WEBHOOK_URL = "https://edae-2401-4900-1c0b-7a70-2c-37b9-5e48-dd89.ngrok-free.app/webhook/98fa7ae4-59aa-4da3-adf2-df486cdb0cd5"

# ------------------------------
# Chat History
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------
# Chat Input
# ------------------------------
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                payload = {
                    "chatInput": user_prompt,
                    "sessionId": st.session_state.session_id
                }

                response = requests.post(
                    N8N_WEBHOOK_URL,
                    json=payload,
                    timeout=120
                )

                # Debug output
                st.write("Status Code:", response.status_code)
                st.write("Raw Response:")
                st.code(response.text)

                if response.status_code != 200:

                    bot_reply = (
                        f"❌ n8n returned HTTP {response.status_code}\n\n"
                        f"{response.text}"
                    )

                else:

                    try:

                        data = response.json()

                        if isinstance(data, dict):

                            bot_reply = (
                                data.get("response")
                                or data.get("output")
                                or data.get("text")
                                or data.get("message")
                                or json.dumps(data, indent=2)
                            )

                        else:

                            bot_reply = str(data)

                    except Exception:

                        bot_reply = response.text

            except Exception as e:

                bot_reply = f"❌ Python Error:\n\n{str(e)}"

        st.markdown(bot_reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )
