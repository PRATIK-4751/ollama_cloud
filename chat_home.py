import streamlit as st
import ollama
import time
import os
from dotenv import load_dotenv

load_dotenv()

client = ollama.Client(
    host='https://ollama.com',
    headers={'Authorization': f'Bearer {os.getenv("OLLAMA_API_KEY")}'}
)

st.set_page_config(
    page_title="Pratik Cloud Chatbot",
    page_icon="◉",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    *{margin:0;padding:0;box-sizing:border-box;}
    html,body,[class*="css"]{font-family:'Space Grotesk',sans-serif;}
    .main-container{backdrop-filter:blur(10px);border-radius:20px;padding:2rem;margin:1rem;box-shadow:0 20px 40px rgba(0,0,0,0.1);border:1px solid rgba(128,128,128,0.2);}
    .custom-header{text-align:center;margin-bottom:2rem;padding:1.5rem;border-radius:15px;box-shadow:0 10px 30px rgba(0,0,0,0.1);}
    .custom-header h1{font-family:'Fira Code',monospace;font-size:2.5rem;font-weight:600;margin:0;text-shadow:2px 2px 4px rgba(0,0,0,0.1);}
    .custom-header p{font-size:1.1rem;margin-top:0.5rem;opacity:0.8;}
    .sidebar-content{backdrop-filter:blur(10px);border-radius:15px;padding:1.5rem;margin:1rem;border:1px solid rgba(128,128,128,0.2);}
    .sidebar-title{font-family:'Fira Code',monospace;font-size:1.3rem;font-weight:600;text-align:center;margin-bottom:1rem;text-shadow:1px 1px 2px rgba(0,0,0,0.1);}
    .stButton>button{border:none;border-radius:12px;padding:0.75rem 1.5rem;font-weight:600;font-family:'Space Grotesk',sans-serif;transition:all 0.3s ease;box-shadow:0 4px 15px rgba(0,0,0,0.1);}
    .stButton>button:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.2);}
    .stTextArea>div>div>textarea{border-radius:12px;border:2px solid rgba(128,128,128,0.3);padding:1rem;font-family:'Space Grotesk',sans-serif;backdrop-filter:blur(5px);transition:all 0.3s ease;}
    .stTextArea>div>div>textarea:focus{box-shadow:0 0 0 3px rgba(0,0,0,0.1);}
    .stSelectbox>div>div{border-radius:12px;border:2px solid rgba(128,128,128,0.3);}
    .user-message{padding:1rem 1.5rem;border-radius:18px 18px 5px 18px;margin:0.5rem 0;margin-left:20%;box-shadow:0 4px 15px rgba(0,0,0,0.1);border:2px solid rgba(128,128,128,0.2);}
    .assistant-message{padding:1rem 1.5rem;border-radius:18px 18px 18px 5px;margin:0.5rem 0;margin-right:20%;border:2px solid rgba(128,128,128,0.2);box-shadow:0 4px 15px rgba(0,0,0,0.1);}
    .ascii-emoji{font-family:'Fira Code',monospace;font-weight:bold;font-size:1.2em;}
    .history-item{border-radius:8px;padding:0.5rem;margin:0.3rem 0;border-left:3px solid rgba(128,128,128,0.5);font-size:0.85rem;border:1px solid rgba(128,128,128,0.2);}
    .loading-dots::after{content:'⋯';animation:loading 1.5s infinite;}
    @keyframes loading{0%{content:'⋯';}33%{content:'⋱';}66%{content:'⋰';}100%{content:'⋯';}}
    .scrollable{max-height:400px;overflow-y:auto;padding-right:10px;}
    .scrollable::-webkit-scrollbar{width:6px;}
    .scrollable::-webkit-scrollbar-track{background:rgba(128,128,128,0.1);border-radius:3px;}
    .scrollable::-webkit-scrollbar-thumb{background:rgba(128,128,128,0.3);border-radius:3px;}
    </style>
    """, unsafe_allow_html=True
)

EMOJIS = {
    "robot": "◉◡◉",
    "user": "◕‿◕",
    "chat": "◈◈◈",
    "model": "▣▣▣",
    "history": "◦◦◦",
    "arrow": "▶",
    "loading": "◌○◍",
    "spark": "✦"
}

models = [
    "gpt-oss:120b-cloud",
    "gpt-oss:20b-cloud", 
    "deepseek-v3.1:671b-cloud",
    "qwen3-coder:480b-cloud"
]

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown(f"""
<div class="custom-header">
    <h1><span class="ascii-emoji">{EMOJIS["robot"]}</span> PRATIK CLOUD</h1>
    <p>Advanced AI Chatbot Interface <span class="ascii-emoji">{EMOJIS["spark"]}</span></p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-content">
        <div class="sidebar-title">{EMOJIS["model"]} MODEL SELECTOR</div>
    """, unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Choose AI Model:",
        models,
        format_func=lambda x: f"{EMOJIS['arrow']} {x}"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sidebar-content">
        <div class="sidebar-title">{EMOJIS["history"]} CHAT HISTORY</div>
        <div class="scrollable">
    """, unsafe_allow_html=True)
    if st.session_state.messages:
        for i, msg in enumerate(st.session_state.messages[-10:]):
            role_emoji = EMOJIS["user"] if msg["role"] == "user" else EMOJIS["robot"]
            preview = msg["content"][:30] + "..." if len(msg["content"]) > 30 else msg["content"]
            st.markdown(f"""
            <div class="history-item">
                <span class="ascii-emoji">{role_emoji}</span> {preview}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="history-item">
            <span class="ascii-emoji">{EMOJIS["chat"]}</span> No messages yet...
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)
    if st.button(f"{EMOJIS['spark']} Clear History"):
        st.session_state.messages = []
        st.rerun()

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown(f"""
    ### {EMOJIS["chat"]} Chat Interface
    Select a model from the sidebar and start chatting with Pratik!
    """)
    user_input = st.text_area(
        f"{EMOJIS['user']} Your Message:",
        placeholder="Type your message here...",
        height=100,
        key="user_input"
    )
    send_button = st.button(f"{EMOJIS['arrow']} Send Message", use_container_width=True)
    st.markdown(f"### {EMOJIS['chat']} Conversation")
    if st.session_state.messages:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <strong><span class="ascii-emoji">{EMOJIS["user"]}</span> You:</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong><span class="ascii-emoji">{EMOJIS["robot"]}</span> Pratik:</strong><br>
                    {msg['content']}
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center;padding:2rem;opacity:0.6;">
            <span class="ascii-emoji" style="font-size:2rem;">{EMOJIS["robot"]}</span><br>
            Start a conversation with Pratik!
        </div>
        """, unsafe_allow_html=True)
    if send_button and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        messages = [
            {"role": "system", "content": "You are Pratik. Always introduce yourself as Pratik and respond according to your role."}
        ] + st.session_state.messages
        with st.spinner(f"{EMOJIS['loading']} Pratik is thinking..."):
            try:
                response = client.chat(
                    model=model_choice,
                    messages=messages
                )
                assistant_msg = response["message"]["content"]
                st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
                st.rerun()
            except Exception as e:
                st.error(f"{EMOJIS['spark']} Error calling model {model_choice}: {e}")
                st.info("Please check if the API key is valid and the model name is correct.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;margin-top:2rem;opacity:0.7;">
    <span class="ascii-emoji">{EMOJIS["spark"]}</span> Powered by Pratik Cloud AI <span class="ascii-emoji">{EMOJIS["spark"]}</span>
</div>
""", unsafe_allow_html=True)