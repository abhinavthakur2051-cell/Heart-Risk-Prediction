import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import base64

# -------- PAGE CONFIG --------
st.set_page_config(page_title="Heart AI Pro", layout="wide", initial_sidebar_state="expanded")

# -------- BACKGROUND IMAGE SETUP --------
# User Instruction: Download any health-related background image (PNG/JPG).
# Rename it to "health_bg.png" and keep it in the same folder as this script.
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/{"png"};base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Adding a slight dark overlay to make text readable on the background */
            .main .block-container {{
                background-color: rgba(14, 17, 23, 0.85); /* Adjust opacity here */
                border-radius: 10px;
                padding: 2rem;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        # If the image is not found, it simply ignores and runs the default theme.
        pass

# Call the background function (Requires 'health_bg.png' in the folder to work)
add_bg_from_local('health_bg.png')


# -------- CUSTOM CSS --------
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .reportview-container .main .block-container { padding-top: 1rem; }
        .guide-card {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #ff4b4b;
            margin-bottom: 10px;
        }
        .text-blue { color: #5dade2; }
        .text-green { color: #58d68d; }
        .text-red { color: #ec7063; }
        .text-yellow { color: #f4d03f; }
        
        /* Custom Classes for Chatbot Suggestions */
        .suggestion-box {
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid #444;
            padding: 15px;
            border-radius: 10px;
            margin-top: 10px;
        }
        .suggestion-title {
            color: #f4d03f;
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# -------- SESSION CHECK --------
if "user" not in st.session_state:
    st.warning("⚠️ Login required")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

# -------- SIDEBAR --------
with st.sidebar:
    try:
        st.image("profile.png", width=80)
    except:
        st.write("👤")
    st.markdown(f"### {st.session_state.user}")
    st.caption("Active Health Session")
    
    st.markdown("---")
    st.title("Dashboard")
    menu = st.radio("Navigation", ["Health Analysis", "History", "India Statistics", "Global Trends"])
    
    st.markdown("---")
    st.subheader("🩺 Clinical Guide")
    st.markdown("""
    <div class="guide-card">
        <b>🩸 Blood Pressure</b><br>
        <span class="text-blue">Low: < 90/60</span><br>
        <span class="text-green">Normal: 90–120</span><br>
        <span class="text-red">High: > 140</span>
    </div>
    <div class="guide-card">
        <b>❤️ Heart Rate (BPM)</b><br>
        <span class="text-blue">Low: < 60</span><br>
        <span class="text-green">Normal: 60–100</span><br>
        <span class="text-red">High: > 100</span>
    </div>
    <div class="guide-card">
        <b>🧪 Cholesterol</b><br>
        <span class="text-green">Normal: < 200</span><br>
        <span class="text-yellow">Borderline: 200–239</span><br>
        <span class="text-red">High: 240+</span>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# -------- LOAD ASSETS --------
@st.cache_resource
def load_assets():
    try:
        m = pickle.load(open("model.pkl", "rb"))
        s = pickle.load(open("scaler.pkl", "rb"))
        return m, s
    except:
        return None, None

model, scaler = load_assets()

# -------- MAIN UI LOGIC --------
if menu == "Health Analysis":
    st.title("❤️ Heart Disease Prediction")
    st.subheader("🔍 Enter Patient Details")

    # Checkbox for users who don't know their vitals
    no_report = st.checkbox("I don't know my BP/Cholesterol levels (Use Average Values)")

    with st.form("health_form"):
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age", 1, 100, 25)
        gender = c2.selectbox("Gender", ["Male", "Female"])
        
        # Logic: If checkbox is ticked, disable the input and set default values
        if no_report:
            bp = c3.number_input("Systolic Blood Pressure", value=120, disabled=True)
        else:
            bp = c3.number_input("Systolic Blood Pressure", 80, 200, 120)

        c4, c5, c6 = st.columns(3)
        if no_report:
            chol = c4.number_input("Cholesterol", value=200, disabled=True)
        else:
            chol = c4.number_input("Cholesterol", 100, 400, 200)
            
        hr = c5.number_input("Heart Rate", 60, 200, 90)
        sugar = c6.selectbox("Fasting Sugar > 120mg/dL", ["No", "Yes"])

        st.write("---")
        c7, c8 = st.columns(2)
        symptoms = c7.selectbox("Symptoms", [
            "None ✅", "Chest Pain 😖", "Shortness of Breath 😮‍💨", "Dizziness 😵‍💫", "Fatigue 😴"
        ])
        smoking = c8.selectbox("Smoking History", ["Never", "Former Smoker", "Current Smoker"])

        submit = st.form_submit_button("Analyze Heart Health")

    if submit:
        if no_report:
            st.warning("⚠️ Using average values (BP: 120, Chol: 200) for the analysis.")
        
        if bp < 90: st.info("ℹ️ Low Blood Pressure Detected")
        elif bp <= 120: st.success("✅ Normal Blood Pressure")
        else: st.error("⚠️ High Blood Pressure Detected")

        if model and scaler:
            g_val = 1 if gender == "Male" else 0
            sym_val = 1 if symptoms in ["Chest Pain 😖", "Shortness of Breath 😮‍💨"] else 0
            features = np.array([[age, g_val, bp, chol, hr, sym_val]])
            prob = model.predict_proba(scaler.transform(features))[0][1] * 100

            if smoking == "Current Smoker": prob += 15
            elif smoking == "Former Smoker": prob += 5
            if sugar == "Yes": prob += 10
            
            prob = min(prob, 100)

            st.markdown("---")
            st.subheader("📊 Diagnostic Result")
            res_col1, res_col2 = st.columns(2)

            with res_col1:
                st.write(f"**Risk Probability Score:** {prob:.2f}%")
                st.progress(prob/100)
                if prob < 30:
                    st.success("🟢 CONDITION: LOW RISK")
                    risk_status = "Low"
                elif prob < 70:
                    st.warning("🟡 CONDITION: MODERATE RISK")
                    risk_status = "Moderate"
                else:
                    st.error("🔴 CONDITION: HIGH RISK")
                    risk_status = "High"

            with res_col2:
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.barplot(x=["BP", "Cholesterol"], y=[bp, chol], palette="magma")
                ax.set_title("Vitals Comparison")
                st.pyplot(fig)

            st.session_state.history.append({
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "User": st.session_state.user,
                "BP": bp,
                "Risk %": round(prob, 2),
                "Status": risk_status
            })

    # -------- CHATBOT (NOW MOVED INSIDE "HEALTH ANALYSIS" ONLY) --------
    st.markdown("---")
    st.subheader("🤖 AI Health Companion")
    chat_query = st.text_input("Type your question / Describe your symptoms here:", key="chat")

    def get_bot_response(q):
        q = q.lower()
        
        # --- HEART & CHEST PAIN ---
        if any(word in q for word in ["pain", "chest", "heart", "attack"]):
            return "🚨 **Urgent:** Chest pain can be serious. Please rest immediately, take deep breaths, and consult a doctor without delay. It could be heart-related or severe acidity."
        
        # --- FEVER / TEMPERATURE ---
        elif any(word in q for word in ["fever", "temperature", "hot", "warm"]):
            return "🌡️ **Fever:** Normal body temperature is **98.6°F (37°C)**. If your fever is above 101°F, apply cold compresses and you may take Paracetamol. If it persists for more than 2-3 days, consult a doctor."

        # --- COLD / COUGH / BLOCKED NOSE ---
        elif any(word in q for word in ["cold", "cough", "nose", "flu", "sneeze"]):
            return "🤧 **Cold/Cough:** Inhale steam with warm water, gargle with salt water, and drink ginger-basil tea. This provides excellent relief for a blocked nose and sore throat."

        # --- HEADACHE ---
        elif any(word in q for word in ["headache", "head", "migraine"]):
            return "🤕 **Headache:** Stress, lack of sleep, or acidity can cause headaches. Try to rest, drink plenty of water, and reduce your screen time. If the pain is chronic and severe, it might be a migraine."

        # --- STOMACH ISSUES ---
        elif any(word in q for word in ["stomach", "gas", "digestion", "acidity", "belly"]):
            return "🤢 **Stomach Ache/Gas:** Eat a light diet like oatmeal or porridge. Drinking mint water or carom seeds (ajwain) boiled in water helps relieve gas and acidity. Avoid fast food."

        # --- BLOOD PRESSURE ---
        elif "bp" in q or "blood pressure" in q:
            return "🩺 **Blood Pressure:** Normal BP is **120/80**. If you have High BP, reduce your salt intake immediately. For Low BP (under 90/60), drink a salt-sugar solution or ORS."

        # --- SUGAR / DIABETES ---
        elif "sugar" in q or "diabetes" in q:
            return "🍬 **Blood Sugar:** Fasting sugar levels are normally **70-100 mg/dL**. If your sugar is high, strictly avoid sweets, white rice, and refined carbs, and begin a daily walking routine."
            
        # --- DENGUE / MALARIA ---
        elif any(word in q for word in ["dengue", "malaria", "mosquito", "platelets"]):
            return "🦟 **Dengue/Malaria:** If you have a high fever with joint pain and chills, get a blood test done (CBC, NS1) immediately. Stay hydrated with coconut water or papaya leaf juice, and see a doctor."
            
        # --- ASTHMA / BREATHING ---
        elif any(word in q for word in ["asthma", "breathing", "breath", "lungs"]):
            return "😮‍💨 **Breathing Issues:** Difficulty breathing can indicate asthma or heart issues. Avoid pollution and dust. Use your prescribed inhaler if you have one, and visit a clinic."

        # --- WEAKNESS / FATIGUE ---
        elif any(word in q for word in ["weakness", "fatigue", "tired", "dizzy"]):
            return "🥱 **Weakness/Fatigue:** This could be due to low hemoglobin (iron), a Vitamin B12/D deficiency, or a poor diet. Include green vegetables, fruits, and nuts in your diet, and consider a routine blood test."

        # --- BODY PAIN / BACK PAIN ---
        elif any(word in q for word in ["back pain", "body pain", "muscle", "joint"]):
            return "🦴 **Body/Back Pain:** Poor posture or lifting heavy items often causes this. Use a hot water bag or heating pad for relief and avoid heavy lifting. Ensure you consume calcium-rich foods."

        # --- SKIN INFECTION / ALLERGY ---
        elif any(word in q for word in ["rash", "allergy", "itch", "skin", "acne"]):
            return "🔴 **Skin Allergy:** Apply pure aloe vera gel or coconut oil for rashes or itching. It might be a mild reaction to a new soap or clothing material. Consult a dermatologist if it persists."

        # --- EYE INFECTION ---
        elif any(word in q for word in ["eye", "red eye", "vision"]):
            return "👁️ **Eye Infection:** If your eyes are red or itchy, avoid touching them and gently wash them with cold water. Reduce your screen time and ask a doctor before using any medical eye drops."

        # --- GREETINGS ---
        elif any(word in q for word in ["hi", "hello", "hey", "good morning"]):
            return "👋 Hello! I am your AI Health Companion. You can ask me for basic information, symptom analysis, and home remedies regarding any health issue for you or your family."

        # --- DEFAULT RESPONSE ---
        return "💡 I didn't completely understand your problem. Please describe your symptoms in a bit more detail (e.g., 'I have had a severe headache since last night' or 'I am having trouble breathing'). For emergencies, please contact a doctor directly."

    if st.button("Get AI Advice"):
        if chat_query:
            st.info(get_bot_response(chat_query))

    # UI: CHATBOT SUGGESTIONS (ENGLISH)
    st.markdown("""
        <div class="suggestion-box">
            <div class="suggestion-title">💡 What can you ask the AI? (Examples)</div>
            <ul>
                <li><b>Symptoms Check:</b> "I have a severe headache and fever since last night, what should I do?"</li>
                <li><b>Heart & BP Issues:</b> "What is a normal blood pressure reading?" or "I am feeling a burning sensation in my chest."</li>
                <li><b>Diet & Health Advice:</b> "What should a diabetic person eat?" or "I am feeling very tired and weak lately."</li>
                <li><b>Home Remedies:</b> "What are some home remedies for a blocked nose and cough?"</li>
                <li><b>General Illnesses:</b> "How can I increase my platelets during Dengue?"</li>
            </ul>
            <i style="color: gray; font-size: 13px;">Simply type your question or symptoms in the input box above and click 'Get AI Advice'.</i>
        </div>
    """, unsafe_allow_html=True)


elif menu == "History":
    st.title("📜 Prediction History")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
        st.download_button("📥 Download All Records", df.to_csv(index=False), "History.csv")
    else:
        st.info("No records found in this session.")

elif menu == "India Statistics":
    st.title("🇮🇳 Indian Cardiac Trends")
    st.line_chart(pd.DataFrame({"Cases (Millions)": [60, 75, 88]}, index=[2020, 2022, 2024]))
    
    # Detailed Indian Statistics Text in English
    st.markdown("""
    ### 📈 Detailed Insights (India)
    * **Current Scenario:** Heart disease cases are rising rapidly in India. By 2024, approximately **88 Million (8.8 Crore)** cases have been officially reported.
    * **Most Affected Age Group:** The highest risk is now seen in young and middle-aged adults (**35 to 50 years**). Previously, it was mostly common in the 60+ age group.
    * **Main Reasons:** Poor lifestyle choices, high stress, excessive junk food consumption, smoking, and rising pollution are the primary causes.
    * **Prevention:** A minimum of 30 minutes of daily exercise, a balanced healthy diet, and regular BP/Sugar checkups are essential for prevention.
    """)

elif menu == "Global Trends":
    st.title("🌍 Global Health Data")
    st.bar_chart(pd.DataFrame({"Risk Level": [35, 30, 22]}, index=["Asia", "USA", "Europe"]))
    
    # Detailed Global Statistics Text in English
    st.markdown("""
    ### 🌎 Detailed Insights (Global)
    * **Highest Risk Zone:** The Asia region (especially South Asia) has the highest risk level globally (**35%**). Genetic factors, along with regional diet, play a major role in this statistic.
    * **Comparison:** In the USA (**30%**) and Europe (**22%**), the risk levels are relatively controlled due to widespread medical awareness and stricter food quality regulations.
    * **Global Demographics:** Globally, the **50+ age group** still accounts for the majority of cardiac cases, but the rate of increase among younger generations is becoming alarming worldwide.
    """)

# -------- MEDICAL DISCLAIMER (Kept safely at the bottom of the app) --------
st.markdown("""
    <div style="font-size: 11px; color: gray; border-top: 1px solid #444; margin-top: 50px; padding-top: 10px;">
        <b>⚠️ MEDICAL DISCLAIMER:</b> This tool provides estimates based on AI models and general health logic. 
        It is NOT a medical diagnosis. In case of a medical emergency, please consult a real doctor or visit a hospital immediately.
    </div>
""", unsafe_allow_html=True)