import openai
import streamlit as st

st.title("Health_ChatBot")

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Initialize the model and messages in session state if not already present
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
prompt = st.chat_input("What is up?")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Use the correct method for creating a completion
    response = openai.ChatCompletion.create(
        model=st.session_state["openai_model"],
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
        stream=True,
    )

    # Display the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for r in response:
            full_response += r['choices'][0]['delta'].get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add the assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
