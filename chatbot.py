import streamlit as st
from groq import Groq

# Guardrail lists
blocked_inputs = ["ignore","credentials","password", "system prompt", "api key", "jailbreak", "bypass"]
blocked_outputs = ["secret", "api key", "system instructions"]

st.title("💬 Chatbot by Alok")

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Show conversation history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# New input box
user_input = st.chat_input("Type your message...")

if user_input:
    # Input guardrail check
    if any(word in user_input.lower() for word in blocked_inputs):
        st.error("⚠️ Unsafe input detected. Not allowed.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=st.session_state["messages"]
        )

        bot_reply = response.choices[0].message.content

        # Output guardrail check
        if any(word in bot_reply.lower() for word in blocked_outputs):
            st.error("⚠️ Unsafe output blocked.")
        else:
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.write(bot_reply)