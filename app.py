import streamlit as st
import time
import base64
import os
from utils import generate_response
from PIL import Image

def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

# Pre-load logo
logo_base64 = get_image_base64("logo.png")
logo_html_main = f'<img src="data:image/png;base64,{logo_base64}" width="50" style="object-fit: contain;">' if logo_base64 else '<div style="font-size: 30px;">🏛️</div>'
logo_html_sidebar = f'<img src="data:image/png;base64,{logo_base64}" width="100" style="object-fit: contain; margin-bottom: 10px;">' if logo_base64 else '<div style="font-size: 50px;">🏛️</div>'


# Page Configuration
st.set_page_config(
    page_title="විශ්‍රාම වැටුප් දෙපාර්තමේන්තුව",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Sinhala:wght@400;600;700&display=swap');
        
        * {
            font-family: 'Noto Sans Sinhala', sans-serif;
        }

        /* Main background */
        .stApp {
            background-color: #f8f9fa;
        }

        /* Reduce Streamlit default padding to make it more compact */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 100% !important;
        }
        
        /* Header styling */
        .header-container {
            background-color: #ffffff;
            padding: 10px 15px;
            border-radius: 12px;
            color: #1a1a1a;
            margin-top: 20px;
            margin-bottom: 5px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            display: flex;
            align-items: center;
            gap: 10px;
            border: 2px solid #000000;
        }
        
        .header-title-container {
            flex-grow: 1;
        }
        
        .header-title {
            font-size: 1.5em;
            font-weight: 700;
            margin: 0;
            color: #0056b3;
        }
        
        .header-subtitle {
            font-size: 0.9em;
            color: #555555;
            margin-top: 4px;
            font-weight: 400;
        }
        
        /* Message Layouts */
        .chat-row-user {
            display: flex;
            justify-content: flex-end;
            margin: 5px 0;
        }
        
        .chat-bubble-user {
            background-color: #0056b3;
            color: white;
            padding: 10px 15px;
            border-radius: 20px 20px 4px 20px;
            max-width: 80%;
            box-shadow: 0 3px 10px rgba(0, 86, 179, 0.2);
            font-size: 14px;
            line-height: 1.4;
        }
        
        .chat-row-assistant {
            display: flex;
            justify-content: flex-start;
            margin: 5px 0;
        }
        
        .chat-bubble-assistant {
            background-color: #ffffff;
            color: #2b2b2b;
            padding: 10px 15px;
            border-radius: 20px 20px 20px 4px;
            max-width: 80%;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            font-size: 14px;
            line-height: 1.4;
            border: 1px solid #e9ecef;
        }
        
        .role-label {
            font-size: 11px;
            opacity: 0.8;
            margin-bottom: 3px;
            display: block;
            font-weight: 600;
        }
        
        /* Info box styling */
        .info-box {
            background-color: #e8f4fd;
            padding: 10px 15px;
            border-radius: 12px;
            border-left: 5px solid #0056b3;
            margin: 5px 0;
            color: #004085;
            font-size: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        }
        
        .info-box h3 {
            margin-top: 0;
            color: #0056b3;
            font-weight: 700;
            font-size: 1.2em;
            margin-bottom: 5px;
        }
        
        /* Empty state styling */
        .empty-state {
            text-align: center;
            color: #888;
            padding: 80px 20px;
            background: #fff;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
            border: 2px dashed #000000;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #666;
            padding: 25px 15px;
            font-size: 0.9em;
            margin-top: 50px;
            border-top: 1px solid #eaedf1;
            background-color: #ffffff;
            border-radius: 16px;
        }
        
        /* Message container */
        .message-container {
            background: transparent;
            padding: 10px 0;
            border-radius: 15px;
            margin: 10px 0;
        }
        
        /* Main Button Override */
        .stButton>button {
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }

        /* Spinner text color */
        [data-testid="stSpinner"] p {
            color: #000000 !important;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Header with custom design
st.markdown(f"""
    <div class="header-container">
        <div style="margin-right: 10px; display: flex; align-items: center;">
            {logo_html_main}
        </div>
        <div class="header-title-container">
            <div class="header-title">ශ්‍රී ලංකා විශ්‍රාම වැටුප් දෙපාර්තමේන්තුව</div>
            <div class="header-subtitle">විශ්‍රාම වැටුප්, අනත්දරු දීමනා සහ සමාජ ආරක්ෂණ සේවා සහායක</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Info Section
if not st.session_state["messages"]:
    st.markdown("""
        <div class="info-box">
            <h3>ආයුබෝවන්!</h3>
            <p>ඔබගේ විශ්‍රාම වැටුප්, අනත්දරු දීමනා, සහ සමාජ ආරක්ෂණ සේවා පිළිබඳ ඕනෑම ගැටලුවක් මෙහි යොමු කරන්න. 
            අපි ඔබට කඩිනමින් පිළිතුරු ලබා දෙන්නෙමු.</p>
        </div>
    """, unsafe_allow_html=True)

# Display Chat History
st.markdown("<div class='message-container'>", unsafe_allow_html=True)

if st.session_state["messages"]:
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"""
                <div class="chat-row-user">
                    <div class="chat-bubble-user">
                        <span class="role-label">ඔබ</span>
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-row-assistant">
                    <div class="chat-bubble-assistant">
                        <span class="role-label">සහායක</span>
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="empty-state">
            <div style="font-size: 40px; margin-bottom: 10px;">💬</div>
            <h3 style="margin-bottom: 5px; color: #444;">ඔබගේ සංවාදය අරඹන්න</h3>
            <p style="margin: 0; font-size: 14px;">පහතින් ඇති කොටුවෙහි ඔබගේ ප්‍රශ්නය ඇතුලත් කර යවන්න</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if st.session_state["messages"] and st.session_state["messages"][-1]["role"] == "user":
    user_msg = st.session_state["messages"][-1]["content"]
    with st.spinner(" පිළිතුර සකස් කරමින්..."):
        response = generate_response(user_msg)
        
    placeholder = st.empty()
    full_response = ""
    for word in response.split(" "):
        full_response += word + " "
        placeholder.markdown(f"""
            <div class="chat-row-assistant">
                <div class="chat-bubble-assistant">
                    <span class="role-label">සහායක</span>
                    {full_response}
                </div>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.05)
        
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.rerun()

# Input Section
user_input = st.chat_input("ඔබගේ ප්‍රශ්නය මෙහි ටයිප් කරන්න...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.rerun()

# Footer and Controls moved to Sidebar
with st.sidebar:
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            {logo_html_sidebar}
            <h3 style="color: #0056b3; margin-top: 10px; font-weight: 700;">විශ්‍රාම වැටුප් දෙපාර්තමේන්තුව</h3>
            <p style="color: #666; font-size: 14px;">ශ්‍රී ලංකා රජයේ සේවය</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("සංවාදය මකා දමන්න", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()
        
    st.markdown("---")
    
    st.markdown("""
        <div style="background-color: #e8f4fd; padding: 15px; border-radius: 10px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 5px;">📞</div>
            <strong style="color: #004085;">අපගේ සහාය සඳහා:</strong><br>
            <span style="font-size: 14px; color: #555;">pensions@gov.lk</span><br>
            <span style="font-size: 12px; color: #777;">පෙ.ව. 8:30 සිට ප.ව. 4:30 දක්වා</span>
        </div>
    """, unsafe_allow_html=True)
