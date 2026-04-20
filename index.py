import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Heart Disease Analyzer",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PREMIUM UI & CSS ----------
st.markdown("""
<style>
    /* Hide Default Elements */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display:none;}

    /* Deep Premium Background */
    .stApp {
        background-color: #080c16;
        background-image: 
            radial-gradient(circle at 15% 20%, #152c55 0%, transparent 40%),
            radial-gradient(circle at 85% 80%, #30101b 0%, transparent 40%);
        color: white;
        font-family: 'Inter', sans-serif;
    }

    /* Main Title Styling */
    .main-title {
        font-size: 65px;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        letter-spacing: -1px;
        line-height: 1.1;
    }

    /* Sub-title Styling */
    .sub-title {
        font-size: 20px;
        font-weight: 300;
        color: #a0aec0;
        margin-top: 15px;
        line-height: 1.5;
    }

    /* Glass Cards for Features */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 16px;
        padding: 30px;
        text-align: left; /* Changed to left for cleaner look */
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        border-color: #ff4b4b;
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px rgba(255, 75, 75, 0.15);
    }

    /* Modern Button Styling */
    div.stButton > button {
        background: #ff4b4b;
        color: white;
        border: none;
        padding: 10px 35px; /* Adjust height */
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        height: 65px; /* Match title height nicely */
        width: 100%;
        transition: all 0.3s;
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.4);
    }

    div.stButton > button:hover {
        transform: scale(1.05);
        background: #ff3333;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.6);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ---------- HERO SECTION (TITLE & BUTTON IN SAME LINE) ----------
st.write("")
st.write("")
st.write("")
st.write("") # Top spacing

# Using columns to put Title and Button face-to-face
hero_col1, hero_col2, hero_col3 = st.columns([3.5, 0.5, 1.5])

with hero_col1:
    st.markdown('<h1 class="main-title">Heart Disease<br>Risk Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Check your heart health in seconds using our advanced AI. Fast, secure, and highly accurate.</p>", unsafe_allow_html=True)

with hero_col3:
    # Button ko title ke aage (right side) center karne ke liye thodi space daali hai
    st.markdown("<br><br>", unsafe_allow_html=True) 
    if st.button("🚀 Get Started"):
        st.switch_page("pages/login.py")

st.write("")
st.write("---")
st.write("")

# ---------- HOW IT WORKS SECTION ----------
st.markdown("<h2 style='font-weight: 700; margin-bottom: 30px; color: #ffffff;'>How It Works</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="glass-card">
        <h2 style='font-size: 35px; margin-bottom: 5px; color: #ff4b4b;'>01.</h2>
        <h3 style='font-size: 22px; color: #ffffff;'>Simple Input</h3>
        <p style='font-size: 15px; color: #a0aec0; margin-top: 10px;'>Enter basic health details like your age, blood pressure, and cholesterol levels.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="glass-card">
        <h2 style='font-size: 35px; margin-bottom: 5px; color: #ff4b4b;'>02.</h2>
        <h3 style='font-size: 22px; color: #ffffff;'>AI Analysis</h3>
        <p style='font-size: 15px; color: #a0aec0; margin-top: 10px;'>Our smart system securely analyzes your data to detect any early signs of risk.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="glass-card">
        <h2 style='font-size: 35px; margin-bottom: 5px; color: #ff4b4b;'>03.</h2>
        <h3 style='font-size: 22px; color: #ffffff;'>Instant Report</h3>
        <p style='font-size: 15px; color: #a0aec0; margin-top: 10px;'>Get a complete and easy-to-read health report instantly on your screen.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------- FOOTER ----------
st.markdown("""
<div style='text-align: center; color: #4a5568; font-size: 14px; padding-top: 80px; padding-bottom: 20px;'>
    Built with ❤️ for a healthier future | © 2026 Heart Disease Risk Analyzer
</div>
""", unsafe_allow_html=True)