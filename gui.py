import streamlit as st
import requests

# Page Setup
st.set_page_config(page_title="Chatter Box", page_icon="💬", layout="centered")


# ---- CSS Styling ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

    body {
        background: linear-gradient(135deg, #fffaf0 0%, #fce3c1 100%);
        color: #3e2f2f;
        font-family: 'Poppins', sans-serif;
    }

    .stTextInput > div > div > input {
        border-radius: 1.5rem;
        padding: 1rem 1.2rem;
        background-color: #fff;
        color: #2d3436;
        border: 2px solid #f8c291;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(250, 177, 160, 0.3);
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 0.8rem;
        padding: 1rem 0;
    }

    .chat-bubble {
        padding: 1.2rem 1.5rem;
        border-radius: 1.8rem;
        max-width: 80%;
        font-size: 15px;
        line-height: 1.6;
        word-wrap: break-word;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
        position: relative;
        background-color: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255,255,255,0.3);
    }

    .user-bubble {
        background: linear-gradient(135deg, #f6d365, #fda085);
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }

    .bot-bubble {
        background: linear-gradient(135deg, #c3cfe2, #e2e2e2);
        color: #2d3436;
        align-self: flex-start;
        margin-right: auto;
    }

    .header-container {
        background: linear-gradient(135deg, #fffefb, #f5f5f5);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <h1 style='text-align: center; color: #2d3436;'>🌿 HR GreenBot</h1>
    <p style='text-align: center; color: #636e72;'>Your eco-friendly HR assistant, here to help with all your questions!</p>
</div>
""", unsafe_allow_html=True)


# ---- Session State Initialization ----
for key in ["chat_history", "user_input", "bot_thinking"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "chat_history" else "" if key == "user_input" else False

# ---- Function to get response from Ollama ----
def get_response(prompt):
    try:
        res = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'mistral', 'prompt': prompt, 'stream': False}
        )
        res.raise_for_status()
        return res.json().get('response', '').strip()
    except Exception as e:
        return f"Error: {e}"

# ---- Chat History Display ----
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for role, msg in st.session_state.chat_history:
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# ---- Chat Input Area ----
if st.session_state.bot_thinking:
    st.info("🤖 Bot is thinking... Please wait.")

else:
    with st.form(key="chat_form_unique"):
        user_input = st.text_input("Your message:", value=st.session_state.user_input, placeholder="Type something...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.chat_history.append(("user", user_input.strip()))
        st.session_state.user_input = user_input.strip()
        st.session_state.bot_thinking = True
        st.rerun()

# ---- Bot Response Handling ----
if st.session_state.bot_thinking:
    with st.spinner("Generating response..."):
        response = get_response(st.session_state.user_input)
    st.session_state.chat_history.append(("bot", response))
    st.session_state.user_input = ""
    st.session_state.bot_thinking = False
    st.rerun()
