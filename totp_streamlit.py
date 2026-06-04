import streamlit as st
import pyotp
import time
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

# Read secret from environment
TOTP_SECRET = os.getenv("TOTP_SECRET")

if not TOTP_SECRET:
    st.error("❌ TOTP_SECRET not found in .env file")
    st.stop()

# Create TOTP object
totp = pyotp.TOTP(TOTP_SECRET)

# ==============================
# PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="TOTP Generator",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================
# CUSTOM CSS FOR BEAUTIFUL STYLING
# ==============================
st.markdown("""
    <style>
    /* Main background - Modern Gradient */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        min-height: 100vh;
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
    }
    
    /* Title styling */
    .title-text {
        text-align: center;
        font-size: 2.8em;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 4px 15px rgba(102, 126, 234, 0.6), 0 0 20px rgba(240, 147, 251, 0.4);
        margin-bottom: 10px;
        letter-spacing: 2px;
    }
    
    /* OTP Display Container */
    .otp-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 30px;
        padding: 50px;
        text-align: center;
        box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3), 0 0 40px rgba(102, 126, 234, 0.4);
        border: 3px solid rgba(240, 147, 251, 0.5);
        backdrop-filter: blur(15px);
        margin: 30px auto;
        max-width: 100%;
        width: 100%;
    }
    
    /* OTP Code */
    .otp-code {
        font-size: 5em;
        font-weight: 900;
        font-family: 'Courier New', monospace;
        letter-spacing: 18px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
        margin: 30px 0;
        font-variant-numeric: tabular-nums;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        word-break: break-all;
        overflow-wrap: break-word;
    }
    
    /* Timer section */
    .timer-section {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 25px;
        margin-top: 30px;
        flex-wrap: wrap;
    }
    
    .timer-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(240, 147, 251, 0.1) 100%);
        border-radius: 20px;
        padding: 20px 35px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.15);
    }
    
    .timer-label {
        font-size: 0.95em;
        color: #764ba2;
        margin-bottom: 8px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .timer-value {
        font-size: 2.2em;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Progress bar styling - Enhanced */
    .progress-container {
        margin-top: 40px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 20px;
        border: 2px solid rgba(102, 126, 234, 0.2);
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .progress-label {
        font-size: 1.1em;
        font-weight: 800;
        color: #764ba2;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .progress-bar-wrapper {
        background: rgba(200, 200, 200, 0.3);
        height: 40px;
        border-radius: 15px;
        overflow: hidden;
        border: 2px solid rgba(102, 126, 234, 0.3);
    }
    
    .status-badge {
        display: inline-block;
        padding: 12px 28px;
        border-radius: 30px;
        font-weight: 900;
        color: white;
        margin-top: 25px;
        font-size: 1.1em;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
        letter-spacing: 1px;
    }
    
    .status-active {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .status-critical {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================
# STREAMLIT STATE FOR AUTO-REFRESH
# ==============================
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# Force refresh every second
placeholder = st.empty()

# ==============================
# MAIN DISPLAY
# ==============================
with placeholder.container():
    # Title
    st.markdown('<div class="title-text">🔐 TOTP Generator Dashboard</div>', unsafe_allow_html=True)
    
    # Get current OTP and calculate remaining time
    current_otp = totp.now()
    current_time = time.time()
    remaining_seconds = totp.interval - int(current_time) % totp.interval
    percentage = (remaining_seconds / totp.interval) * 100
    
    # Determine status color and progress bar gradient
    if remaining_seconds <= 5:
        status_class = "status-critical"
        status_text = "⚠️ EXPIRING SOON"
        otp_color_gradient = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)"
        progress_gradient = "linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)"
    elif remaining_seconds <= 10:
        status_class = "status-warning"
        status_text = "⏰ EXPIRES SOON"
        otp_color_gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
        progress_gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
    else:
        status_class = "status-active"
        status_text = "✅ ACTIVE"
        otp_color_gradient = "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)"
        progress_gradient = "linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)"
    
    # OTP Display Container
    st.markdown(f'''
        <div class="otp-container">
            <div style="color: #764ba2; font-size: 1.3em; margin-bottom: 15px; font-weight: 700; letter-spacing: 1px;">CURRENT TOKEN</div>
            <div class="otp-code">{current_otp}</div>
        </div>
    ''', unsafe_allow_html=True)
        
        # Timer section with Streamlit components
    timer_col1, timer_col2 = st.columns(2)
    
    with timer_col1:
        st.metric(label="⏱️ Expires In", value=f"{remaining_seconds}s")
    
    with timer_col2:
        st.metric(label="🕐 Current Time", value=datetime.now().strftime('%H:%M:%S'))
    
    # Progress bar
    st.markdown('<div class="progress-container"><div class="progress-label">TOKEN EXPIRATION PROGRESS</div></div>', unsafe_allow_html=True)
    st.progress(percentage / 100)
    
    # Status Badge
    st.markdown(f'<div style="text-align: center;"><div class="status-badge {status_class}">{status_text}</div></div>', unsafe_allow_html=True)
    
    # Additional Info
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.metric(label="🔑 Token Lifetime", value="30s")
    
    with info_col2:
        st.metric(label="📊 Fill %", value=f"{int(percentage)}%")
    
    with info_col3:
        st.metric(label="⏳ Seconds Left", value=f"{remaining_seconds}s")
        
    # Footer Info
    st.markdown("""
        ---
        <div style="text-align: center; color: rgba(102, 126, 234, 0.8); font-size: 0.95em; padding: 15px;">
            <p style="font-weight: 700;">🔄 Dashboard auto-updates every second</p>
            <p>🔒 Token refreshes every 30 seconds</p>
            <p style="color: rgba(240, 147, 251, 0.7); font-size: 0.85em;">✨ Beautiful Real-time TOTP Generator</p>
        </div>
    """, unsafe_allow_html=True)
# Auto-refresh the page every 1 second
time.sleep(1)
st.rerun()
