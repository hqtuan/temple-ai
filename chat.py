import bcrypt
import streamlit as st
from openai import OpenAI

st.set_page_config(
   page_title="Template AI",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded"
)

# Store the initial value of widgets in session state
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False
    
if "models" not in st.session_state:
    st.session_state.models = "gpt-3.5-turbo"

# Sidebar 
st.sidebar.title("Temple AI")

if st.session_state.is_authenticated:
    st.sidebar.success("You have successfully logged in")
    st.session_state.models = st.sidebar.selectbox("Select your model",("gpt-3.5-turbo", "gpt-4.0"))
    
    # Chat with GPT
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    st.title(st.session_state.models)
    
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in  st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your question..."):
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
else:
    st.sidebar.error("You are not logged in")
    password = st.sidebar.text_input("Password",type='password')
    login = st.sidebar.button("Login", type='secondary')
    if login:
        # hashed = bcrypt.hashpw("my=password".encode('utf-8'), bcrypt.gensalt())
        if bcrypt.checkpw(password.encode('utf-8'), b'$2b$12$TNba.gndNgsMxHeDg97dfuwUuHLLFYzkCiCd0nibJjPJ4tLSsiVqC'):
            st.session_state.is_authenticated = True
            
        else:
            st.sidebar.error("Invalid password")