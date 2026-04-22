import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Legal & Info",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- MATCHING CSS FOR DARK THEME ----------
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display:none;}
    .stApp {
        background-color: #080c16;
        background-image: 
            radial-gradient(circle at 15% 20%, #152c55 0%, transparent 40%),
            radial-gradient(circle at 85% 80%, #30101b 0%, transparent 40%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    /* Back button styling */
    div.stButton > button {
        background: transparent;
        color: #ff4b4b;
        border: 1px solid #ff4b4b;
        padding: 5px 20px;
        font-weight: bold;
        border-radius: 5px;
        transition: all 0.3s;
    }
    div.stButton > button:hover {
        background: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Navigation Back to Home
if st.button("← Back to Home"):
    st.switch_page("index.py") 

st.markdown("<h1 style='text-align: center; color: #ffffff;'>Legal & Company Information</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Organising content into clean tabs
tab1, tab2, tab3 = st.tabs(["🏢 About Us", "📜 Terms & Conditions", "🔒 Privacy Policy"])

with tab1:
    st.markdown("""
    ### About Heart Disease Risk Analyzer
    Welcome to the Heart Disease Risk Analyzer. Our mission is to empower individuals with early detection tools for cardiovascular health. 
    
   Advanced Artificial Intelligence and Machine Learning models, our platform provides quick, accessible, and secure health risk assessments. We believe that preventive healthcare should be available to everyone, everywhere.
    
    **Our Vision:**
    To reduce the global impact of heart disease through early awareness, lifestyle management, and predictive technology.
    
    *Note: Our tool is designed for informational purposes and should not replace professional medical diagnosis.*
    """)

with tab2:
    st.markdown("""
    ### Terms & Conditions
    **Last Updated: April 2026**
    
    By accessing or using the Heart Disease Risk Analyzer, you agree to be bound by these Terms and Conditions:
    
    1. **Not Medical Advice:** The results provided by this application are estimations based on statistical models. They do NOT constitute professional medical advice, diagnosis, or treatment.
    2. **User Responsibility:** You should always consult with a qualified healthcare provider regarding any medical conditions or health concerns. Do not disregard professional medical advice because of information provided by this app.
    3. **Accuracy of Information:** While we strive for high accuracy using advanced AI, we do not guarantee the completeness or absolute reliability of the risk predictions.
    4. **Usage Limitations:** You agree not to misuse the platform, attempt to breach security measures, or use the service for commercial diagnostic purposes without authorization.
    """)

with tab3:
    st.markdown("""
    ### Privacy Policy
    **Last Updated: April 2026**
    
    Your privacy and data security are our highest priorities.
    
    1. **Data Collection:** We only collect the health metrics (such as age, blood pressure, cholesterol) that you voluntarily input into the analyzer to generate your report.
    2. **Data Storage & Anonymity:** We do not store personally identifiable medical records. Any session data processed is transient and securely handled.
    3. **Third-Party Sharing:** We do not sell, trade, or otherwise transfer your health inputs to outside parties. 
    4. **Security Measures:** We implement a variety of security protocols to maintain the safety of your information when you enter, submit, or access your data.
    
    If you have any questions regarding how your data is handled, please use the contact email provided on our homepage.
    """)

# Minimal Footer for Content Page
st.write("---")
st.markdown("""
<div style='text-align: center; color: #a0aec0; font-size: 14px;'>
    For inquiries, email us at: <a href='mailto:bmw41887@gmail.com' style='color:#ff4b4b; text-decoration:none;'>bmw41887@gmail.com</a>
</div>
""", unsafe_allow_html=True)