import streamlit as st
import sqlite3
import requests
import re
from streamlit_lottie import st_lottie

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Login | Heart AI", 
    page_icon="❤️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# ---------- PREMIUM UI & CSS ----------
st.markdown("""
    <style>
        /* Hide Everything Unnecessary & Fix Top Box Issue */
        [data-testid="stSidebar"], [data-testid="collapsedControl"], header {display: none;}
        
        /* Remove Top White Space/Box and unwanted lines */
        .block-container {
            padding-top: 2rem !important;
            max-width: 500px !important;
        }
        
        /* Background Styling */
        .stApp {
            background-color: #0b0f19;
            background-image: 
                radial-gradient(circle at 50% 0%, #1a365d 0%, transparent 50%),
                radial-gradient(circle at 80% 100%, #2d132c 0%, transparent 50%);
            color: white;
        }

        /* Input Styling - Minimal & Clean */
        .stTextInput > div > div > input {
            background-color: rgba(255, 255, 255, 0.07) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            height: 48px;
            font-size: 16px;
        }

        /* Button Styling - Fixed Alignment */
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

lottie_heart = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_m6cu9scz.json")

# ---------- MAIN CONTENT ----------
st.write("<br>", unsafe_allow_html=True)

if lottie_heart:
    st_lottie(lottie_heart, height=150, key="heart_anim")

st.markdown('<p class="title-text">Secure Login</p>', unsafe_allow_html=True)
# Simple English Line
st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 16px;'>Please login to check your heart health report</p>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# --- Input Fields ---
email = st.text_input("📧 Email Address", placeholder="Enter your gmail")
username = st.text_input("👤 Username", placeholder="Enter your username")
password = st.text_input("🔑 Password", type="password", placeholder="At least 8 characters")

st.write("<br>", unsafe_allow_html=True)

# --- Buttons Position Fixed ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Login"):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.error("Please enter a valid email!")
        elif len(password) < 8:
            st.error("Password must be 8 characters or more.")
        elif username == "" or password == "":
            st.warning("All fields are required!")
        else:
            c.execute("SELECT * FROM users WHERE (username=? OR email=?) AND password=?", (username, email, password))
            user = c.fetchone()
            if user:
                st.session_state.user = username
                st.success("Login Successful!")
                st.switch_page("pages/home.py")
            else:
                st.error("Invalid Login Details.")

with col2:
    if st.button("⏪ Back"):
        st.switch_page("index.py")

st.write("<br>", unsafe_allow_html=True)
st.divider()

# --- Register Link ---
st.markdown("<p style='text-align: center; color: #888;'>Don't have an account?</p>", unsafe_allow_html=True)
if st.button("📝 Create New Account"):
    st.switch_page("pages/register.py")