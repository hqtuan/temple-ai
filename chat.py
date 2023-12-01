import time
import streamlit as st
from openai import OpenAI


st.set_page_config(
   page_title="Template AI",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded"
)

st.title("ChatGPT 3.5")

# Sidebar
with st.sidebar:
    add_title = st.title("Temple AI",)
    add_logo = st.image('logo.png', width=180)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in  st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hãy nhập vào yêu cầu?"):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        full_res = ""
        holder = st.empty()

        for response in client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_res += (response.choices[0].delta.content or "")
            holder.markdown(full_res + "▌")
            holder.markdown(full_res)
        holder.markdown(full_res)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_res
        }
    )