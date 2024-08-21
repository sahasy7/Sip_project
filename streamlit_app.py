import streamlit as st
from openai import OpenAI
import time


st.set_page_config(
    page_title="Kanha Shanti Vanam",
    page_icon="🤖",  # Changed page icon to a robot emoji
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None)

st.title("Welcome To Kanha Shanti Vanam")


if "messages" not in st.session_state.keys():
    # Initialize the chat messages history
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Need Info? Ask Me Questions about Kanha Shanti Vanam "
        }
    ]




def get_latest_message(user_input):
    # Create a thread with the user input as the message content.
    ASSISTANT_ID = st.secrets.assitant_id
    api_key  = st.secrets.openai_key
    client = OpenAI(api_key= api_key)
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)

    # Wait for the run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(1)

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Return the latest message content.
    if messages:
        latest_message = messages[0]
        return latest_message.content[0].text.value
    else:
        return "No response received."
    

if prompt := st.chat_input("Your question"):
  # Prompt for user input and save to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})


for message in st.session_state.messages:
  # Display the prior chat messages
  with st.chat_message(message["role"]):
    st.write(message["content"])

if st.session_state.messages[-1]["role"] != "assistant":
  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      response = get_latest_message(prompt)
      st.write(response)
      message = {"role": "assistant", "content": response}
      st.session_state.messages.append(
          message)  # Add response to message history

