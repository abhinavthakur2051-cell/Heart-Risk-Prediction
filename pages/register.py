import streamlit as st
import sqlite3
import requests
import re
from streamlit_lottie import st_lottie

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Register | Heart AI", 
    page_icon="❤️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ---------- PREMIUM UI & CSS ----------
st.markdown("""
    <style>
        /* Hide Everything Unnecessary & Fix Top Box Issue */
        [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display: none;}
        
        /* Remove Top White Space/Box */
        .block-container {
            padding-top: 2rem !important;
            max-width: 500px !important;
        }
        
        /* Background Styling - Same as Login */
        .stApp {
            background-color: #0b0f19;
            background-image: 
                radial-gradient(circle at 50% 0%, #1a365d 0%, transparent 50%),
                radial-gradient(circle at 80% 100%, #2d132c 0%, transparent 50%);
            color: white;
        }

        /* Input Styling */
        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.07) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            height: 48px;
            font-size: 16px;
        }

        /* Button Styling */
        div.stButton > button {
            background: linear-gradient(90deg, #ff4b4b, #d91e18);
            color: white;
            border: none;
            padding: 10px 15px;
            font-size: 16px;
            font-weight: 700;
            border-radius: 10px;
            width: 100%;
            height: 45px;
            transition: 0.3s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
        }

        .title-text {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #ff4b4b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Logic: Database Setup ---
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, email TEXT, password TEXT)")
conn.commit()

# --- Logic: Lottie Animation ---
def load_lottieurl(url):
    try: return requests.get(url).json()
    except: return None

lottie_reg = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_m6cu9scz.json")

# ---------- MAIN CONTENT ----------
st.write("<br>", unsafe_allow_html=True)

if lottie_reg:
    st_lottie(lottie_reg, height=150, key="reg_anim")

st.markdown('<p class="title-text">Create Account</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 16px;'>Join Heart AI to monitor your health</p>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# --- Input Fields ---
new_email = st.text_input("📧 Gmail Address", placeholder="e.g. example@gmail.com")
new_user = st.text_input("👤 Choose Username", placeholder="e.g. aryan123")
new_pass = st.text_input("🔑 Create Password", type="password", placeholder="At least 8 characters")
confirm_pass = st.text_input("🔄 Confirm Password", type="password", placeholder="Repeat your password")

st.write("<br>", unsafe_allow_html=True)

# --- Buttons ---
col1, col2 = st.columns(2)

with col1:
    if st.button("📝 Register"):
        # Validation Logic
        if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
            st.error("Please enter a valid Gmail address!")
        elif len(new_pass) < 8:
            st.error("Password must be at least 8 characters long.")
        elif new_pass != confirm_pass:
            st.error("Passwords do not match!")
        elif new_user == "" or new_email == "":
            st.warning("All fields are mandatory.")
        else:
            try:
                c.execute("INSERT INTO users (username, email, password) VALUES (?,?,?)", (new_user, new_email, new_pass))
                conn.commit()
                st.success("Account created! Please Login.")
                st.balloons()
            except sqlite3.IntegrityError:
                st.error("Username already taken. Try another one.")

with col2:
    if st.button("⏪ Back"):
        st.switch_page("pages/login.py")

st.write("<br>", unsafe_allow_html=True)
st.divider()

st.markdown("<p style='text-align: center; color: #888;'>Already have an account?</p>", unsafe_allow_html=True)
if st.button("🚀 Go to Login"):
    st.switch_page("pages/login.py")