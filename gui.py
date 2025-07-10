import streamlit as st
import requests

# Page Setup
st.set_page_config(page_title="Chatter Box", page_icon="💬", layout="centered")

# ---- CSS Styling ----
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
    
    body {
        background: linear-gradient(135deg, rgba(245, 247, 250, 0.9) 0%, rgba(195, 207, 226, 0.9) 100%);
        color: #2d3436;
        font-family: 'Poppins', sans-serif;
        background-image: url('https://images.unsplash.com/photo-1544551763-46a013bb70d5?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80');
        background-blend-mode: overlay;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
        background-attachment: fixed;
    }

    .stTextInput > div > div > input {
        border-radius: 1.5rem;
        padding: 1rem 1.2rem;
        background-color: rgba(255, 255, 255, 0.95);
        color: #2d3436;
        border: 2px solid #a8e6cf;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(163, 218, 255, 0.3);
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .stTextInput > div > div > input:focus {
        border: 2px solid #74b9ff;
        box-shadow: 0 0 15px rgba(116, 185, 255, 0.5);
        outline: none;
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
        backdrop-filter: blur(6px);
        background-color: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255,255,255,0.3);
    }

    .user-bubble {
        background: linear-gradient(135deg, rgba(116, 185, 255, 0.9) 0%, rgba(9, 132, 227, 0.9) 100%);
        color: white;
        align-self: flex-end;
        margin-left: auto;
        border-bottom-right-radius: 0.5rem;
    }

    .bot-bubble {
        background: linear-gradient(135deg, rgba(168, 230, 207, 0.9) 0%, rgba(220, 237, 193, 0.9) 100%);
        color: #2d3436;
        align-self: flex-start;
        margin-right: auto;
        border-bottom-left-radius: 0.5rem;
    }

    .stButton > button {
        border-radius: 1.5rem;
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa3a3 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
        transition: all 0.3s ease;
        margin: 0.2rem;
        width: 100%;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
    }

    .stButton > button:focus {
        outline: none;
    }

    .header-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(245,245,245,0.95) 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.4);
    }
    
    .typing-indicator {
        display: inline-block;
        padding: 12px 18px;
        background: rgba(240, 240, 240, 0.9);
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .typing-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #74b9ff;
        margin: 0 3px;
        animation: typingAnimation 1.4s infinite ease-in-out;
    }
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typingAnimation {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }

    /* Make all buttons clearly visible */
    div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div > button {
        opacity: 1 !important;
        visibility: visible !important;
        transform: scale(1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Header with improved styling
st.markdown("""
<div class="header-container">
    <h1 style='text-align: center; color: #2d3436; margin-bottom: 0.5rem;'>🌿 HR GreenBot</h1>
    <p style='text-align: center; color: #636e72; font-size: 1.1rem;'>Your eco-friendly HR assistant, here to help with all your questions!</p>
</div>
""", unsafe_allow_html=True)

# ---- Session State Initialization ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "bot_thinking" not in st.session_state:
    st.session_state.bot_thinking = False

# ---- Function to get response from Ollama ----
def get_response(prompt):
    res = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': 'mistral', 'prompt': prompt, 'stream': False}
    )
    return res.json()['response'].strip()

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
    with st.form(key="chat_form_unique"):  # Ensure the form key is unique
        user_input = st.text_input("Your message:", value=st.session_state.user_input, placeholder="Type something...")
        submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.chat_history.append(("user", user_input.strip()))
        st.session_state.user_input = user_input.strip()
        st.session_state.bot_thinking = True
        st.rerun()

# ---- Bot Response Handling ----
if st.session_state.bot_thinking:
    with st.spinner("🤖 Generating response..."):
        response = get_response(st.session_state.user_input)
    st.session_state.chat_history.append(("bot", response))
    st.session_state.user_input = ""
    st.session_state.bot_thinking = False
    st.rerun()
