import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Heart Disease Analyzer",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- PREMIUM UI & ADVANCED CSS ANIMATIONS ----------
st.markdown("""
<style>
    /* Hide Default Elements */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display:none;}

    /* Deep Premium Background (HEART REMOVED) */
    .stApp {
        background-color: #050810;
        background-image: 
            radial-gradient(circle at 15% 0%, rgba(255, 75, 75, 0.15) 0%, transparent 40%),
            radial-gradient(circle at 85% 100%, rgba(21, 44, 85, 0.5) 0%, transparent 40%);
        color: white;
        font-family: 'Inter', sans-serif;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* HERO SECTION (HEART REMOVED) */
    .hero-container {
        position: relative;
        text-align: center;
        padding-top: 80px;
        padding-bottom: 40px;
        z-index: 1;
        animation: fadeInUp 1s ease-out forwards;
    }

    /* Main Title */
    .hero-title {
        font-size: 85px;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        letter-spacing: -2px;
        line-height: 1.1;
        text-shadow: 0px 10px 30px rgba(0,0,0,0.5);
    }

    /* Subtitle */
    .hero-subtitle {
        font-size: 22px;
        font-weight: 300;
        text-align: center;
        color: #a0aec0;
        margin-bottom: 40px;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 40px 30px;
        text-align: center; 
        transition: all 0.4s ease;
        height: 100%;
        animation: fadeInUp 1.2s ease-out forwards;
    }
    
    .glass-card:hover {
        transform: translateY(-10px);
        border-color: rgba(255, 75, 75, 0.5);
        background: rgba(255, 255, 255, 0.05);
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.2);
    }

    /* RED BUTTON */
    button[kind="primary"] {
        background: linear-gradient(135deg, #ff4b4b 0%, #cc0000 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 800 !important;
        font-size: 20px !important;
        border-radius: 50px !important;
        padding: 10px 40px !important;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.4) !important;
    }

    button[kind="primary"]:hover {
        transform: scale(1.08) translateY(-2px) !important;
        box-shadow: 0 15px 35px rgba(255, 75, 75, 0.6) !important;
    }

    /* Navbar Buttons */
    .nav-btn > div > button[kind="secondary"] {
        background: transparent !important;
        color: #a0aec0 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }

    .nav-btn > div > button[kind="secondary"]:hover {
        background: rgba(255,255,255,0.1) !important;
        color: #ffffff !important;
        border-color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
nav1, nav2, nav3, nav4, nav5 = st.columns([4.5, 1, 1, 1, 1])

with nav1:
    st.markdown("<h3 style='margin-top: 5px; color: #ffffff;'>✨ Heart AI</h3>", unsafe_allow_html=True)

with nav2:
    if st.button("About Us", key="nav_about", use_container_width=True):
        st.switch_page("pages/content.py")   # ✅ working

with nav3:
    if st.button("Contact Us", key="nav_contact", use_container_width=True):
        st.switch_page("pages/contact.py")   # ✅ fixed

with nav4:
    if st.button("Login", key="nav_login", use_container_width=True):
        st.switch_page("pages/login.py")

with nav5:
    if st.button("Register", key="nav_register", use_container_width=True):
        st.switch_page("pages/register.py")

# ---------- HERO ----------
st.markdown("""
<div class="hero-container">
    <h1 class="hero-title">Your heart health,<br>simplified.</h1>
    <p class="hero-subtitle">Check your cardiovascular risk in seconds using advanced AI.<br>Fast, secure, and completely reliable.</p>
</div>
""", unsafe_allow_html=True)

btn_col1, btn_col2, btn_col3 = st.columns([1.5, 1, 1.5])
with btn_col2:
    if st.button("❤️ Get Started Now", type="primary", key="hero_get_started", use_container_width=True):
        st.switch_page("pages/login.py")

st.write("<br><br><br>", unsafe_allow_html=True)
st.write("---")
st.write("<br>", unsafe_allow_html=True)

# ---------- HOW IT WORKS ----------
st.markdown("<h2 style='text-align: center; font-weight: 800; margin-bottom: 50px; color: #ffffff;'>How It Works</h2>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""<div class="glass-card">
    <h1 style='font-size: 50px; color: #ff4b4b;'>1</h1>
    <h3>Simple Input</h3>
    <p>Enter basic health details like age, BP, cholesterol.</p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""<div class="glass-card">
    <h1 style='font-size: 50px; color: #ff4b4b;'>2</h1>
    <h3>AI Analysis</h3>
    <p>System analyzes your data securely.</p>
    </div>""", unsafe_allow_html=True)

with c3:
    st.markdown("""<div class="glass-card">
    <h1 style='font-size: 50px; color: #ff4b4b;'>3</h1>
    <h3>Instant Report</h3>
    <p>Get health report instantly.</p>
    </div>""", unsafe_allow_html=True)

# ---------- FOOTER ----------
st.markdown("<hr>", unsafe_allow_html=True)

f1, f2, f3 = st.columns([1,1.5,1])

with f1:
    st.write("© 2026 Heart AI")

with f2:
    st.page_link("pages/content.py", label="Terms & Conditions")
    st.page_link("pages/content.py", label="Privacy Policy")

with f3:
    st.write("Built with ❤️")