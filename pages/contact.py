import streamlit as st
import urllib.parse

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Contact Us",
    page_icon="✉️",
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

st.markdown("<h1 style='text-align: center; color: #ffffff;'>Contact Us</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0;'>Have a question? We would love to hear from you. Send us a message below.</p>", unsafe_allow_html=True)
st.write("---")

# Contact Form Layout
cont_col1, cont_col2 = st.columns([1.5, 1])

with cont_col1:
    with st.form("contact_form"):
        user_name = st.text_input("Your Name")
        user_subject = st.text_input("Subject")
        user_message = st.text_area("Your Message", height=200)
        
        submit_contact = st.form_submit_button("Send Message ✉️")
        
        if submit_contact:
            if user_name and user_message:
                subject_encoded = urllib.parse.quote(f"{user_subject} - From {user_name}")
                body_encoded = urllib.parse.quote(user_message)
                mailto_link = f"mailto:bmw41887@gmail.com?subject={subject_encoded}&body={body_encoded}"
                
                st.success("Form verified! Click the button below to send your email.")
                st.markdown(f"""
                <a href="{mailto_link}" target="_blank">
                    <button style="background-color:#58d68d; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
                        Open Email App to Send
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.error("Please fill in your name and message before submitting.")

with cont_col2:
    st.markdown("""
    <div style='padding-left: 30px; background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.1);'>
        <h3 style='color: #ff4b4b; margin-top: 0;'>Reach out directly</h3>
        <p style='color: #a0aec0; line-height: 2;'>
            📍 <strong>Address:</strong><br> AI Health Hub, New Delhi, India<br><br>
            📞 <strong>Phone:</strong><br> +91 98765 43210<br><br>
            ✉️ <strong>Email:</strong><br> bmw41887@gmail.com<br>
        </p>
    </div>
    """, unsafe_allow_html=True)