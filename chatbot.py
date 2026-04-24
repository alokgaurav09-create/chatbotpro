import streamlit as st
from groq import Groq

# Guardrail lists
blocked_inputs = ["ignore", "system prompt", "api key", "jailbreak", "bypass"]
blocked_outputs = ["secret", "api key", "system instructions"]

st.title("Secure Chatbot with Guardrails")

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("You:")

if user_input:
    # Input guardrail check
    if any(word in user_input.lower() for word in blocked_inputs):
        st.error("⚠️ Unsafe input detected. Not allowed.")
    else:
        st.session_state["messages"].append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state["messages"]
        )

        bot_reply = response.choices[0].message.content

        # Output guardrail check
        if any(word in bot_reply.lower() for word in blocked_outputs):
            st.error("⚠️ Unsafe output blocked.")
        else:
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
            st.write("Bot:", bot_reply)