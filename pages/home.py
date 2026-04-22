import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import base64
import plotly.graph_objects as go

# ==========================================
# -------- PAGE CONFIGURATION --------
# ==========================================
# Updated for 2026 Standards
st.set_page_config(
    page_title="Heart AI Pro | Diagnostic Dashboard",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# -------- CUSTOM STYLING (CSS) --------
# ==========================================
st.markdown("""
    <style>
        /* Modern Dark Theme Overlays */
        .main .block-container {
            background-color: rgba(14, 17, 23, 0.85);
            border-radius: 15px;
            padding: 2.5rem;
            margin-top: 10px;
        }
        
        [data-testid="stSidebarNav"] {display: none;}
        
        /* Clinical Guide Styling */
        .guide-card {
            background-color: rgba(255, 255, 255, 0.07);
            padding: 12px;
            border-radius: 10px;
            border-left: 5px solid #ff4b4b;
            margin-bottom: 12px;
            transition: transform 0.3s;
        }
        .guide-card:hover {
            transform: translateX(5px);
            background-color: rgba(255, 255, 255, 0.1);
        }
        
        .text-blue { color: #5dade2; font-weight: bold; }
        .text-green { color: #58d68d; font-weight: bold; }
        .text-red { color: #ec7063; font-weight: bold; }
        .text-yellow { color: #f4d03f; font-weight: bold; }
        
        /* Suggestion Box for AI Chatbot */
        .suggestion-box {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #3d3d3d;
            padding: 20px;
            border-radius: 12px;
            margin-top: 15px;
        }
        .suggestion-title {
            color: #f4d03f;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# -------- SESSION & STATE MGMT --------
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = "Guest Patient"

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# -------- SIDEBAR & NAVIGATION --------
# ==========================================
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center;'>❤️ Heart AI</h2>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'>Welcome, {st.session_state.user}</h4>", unsafe_allow_html=True)
    st.caption("<div style='text-align: center;'>Secure Health Monitoring Session</div>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.title("🎛️ Dashboard")
    menu = st.radio(
        "Navigate Application", 
        ["Health Analysis", "History", "India Statistics", "Global Trends"]
    )
    
    st.markdown("---")
    st.subheader("🩺 Clinical Reference")
    st.markdown("""
    <div class="guide-card">
        <b>🩸 Blood Pressure (Systolic)</b><br>
        <span class="text-blue">Low: < 90</span><br>
        <span class="text-green">Ideal: 90–120</span><br>
        <span class="text-red">High: > 140</span>
    </div>
    <div class="guide-card">
        <b>❤️ Resting BPM</b><br>
        <span class="text-blue">Athletic: < 60</span><br>
        <span class="text-green">Normal: 60–100</span><br>
        <span class="text-red">Tachycardia: > 100</span>
    </div>
    <div class="guide-card">
        <b>🧪 Serum Cholesterol</b><br>
        <span class="text-green">Healthy: < 200</span><br>
        <span class="text-yellow">Borderline: 200–239</span><br>
        <span class="text-red">High Risk: 240+</span>
    </div>
    """, unsafe_allow_html=True)

  # Updated logout button
    if st.button("Logout", width='stretch'):
        st.session_state.clear() # Ye purana data aur session delete kar dega
        st.switch_page("pages/login.py") # Ye direct login page par le jayega

# ==========================================
# -------- MACHINE LEARNING ASSETS --------
# ==========================================
@st.cache_resource
def load_clinical_assets():
    """Load the trained model and scaler with error handling."""
    try:
        m = pickle.load(open("model.pkl", "rb"))
        s = pickle.load(open("scaler.pkl", "rb"))
        return m, s
    except Exception:
        return None, None

model, scaler = load_clinical_assets()

# ==========================================
# -------- MAIN INTERFACE LOGIC --------
# ==========================================

if menu == "Health Analysis":
    st.title("📊Heart Risk Analyzer")
    st.markdown("Provide your clinical parameters below for an AI-driven risk assessment.")

    # Option for missing reports
    no_report = st.checkbox("I do not have my latest BP/Cholesterol lab reports (Use Population Averages)")

    with st.form("diagnostic_form"):
        st.subheader("📋 Patient Information")
        c1, c2, c3 = st.columns(3)
        age = c1.number_input("Age (Years)", 1, 110, 30)
        gender = c2.selectbox("Gender at Birth", ["Male", "Female"])
        
        # Disabled logic for missing reports
        if no_report:
            bp = c3.number_input("Systolic Blood Pressure", value=120, disabled=True)
        else:
            bp = c3.number_input("Systolic Blood Pressure (mmHg)", 80, 220, 120)

        c4, c5, c6 = st.columns(3)
        if no_report:
            chol = c4.number_input("Cholesterol Level", value=195, disabled=True)
        else:
            chol = c4.number_input("Cholesterol (mg/dL)", 100, 500, 195)
            
        hr = c5.number_input("Resting Heart Rate", 40, 220, 75)
        sugar = c6.selectbox("Fasting Sugar > 120mg/dL", ["No", "Yes"])

        st.markdown("---")
        st.subheader("🚬 Lifestyle & History")
        c7, c8 = st.columns(2)
        symptoms = c7.selectbox("Primary Symptoms", [
            "None ✅", "Chest Pain 😖", "Shortness of Breath 😮‍💨", "Dizziness 😵‍💫", "Extreme Fatigue 😴"
        ])
        smoking = c8.selectbox("Smoking Status", ["Non-Smoker", "Occasional Smoker", "Regular Smoker"])

        # Updated form submit with 2026 width standard
        submit = st.form_submit_button("Evaluate Heart Health Status", width='stretch')

    if submit:
        st.markdown("---")
        st.subheader("🧪 Assessment Results")
        
        if no_report:
            st.warning("⚠️ Baseline population averages (BP: 120, Chol: 195) are being used for this prediction.")
        
        # Prediction Logic
        prob = 0.0
        if model and scaler:
            g_idx = 1 if gender == "Male" else 0
            sym_idx = 1 if symptoms in ["Chest Pain 😖", "Shortness of Breath 😮‍💨"] else 0
            features = np.array([[age, g_idx, bp, chol, hr, sym_idx]])
            prob = model.predict_proba(scaler.transform(features))[0][1] * 100
        else:
            # Robust Fallback Logic
            prob = 10.0 + (age * 0.2)
            if bp > 140: prob += 20
            if chol > 240: prob += 15
            if symptoms != "None ✅": prob += 25
            if smoking == "Regular Smoker": prob += 15

        # Cap probability for realism
        prob = max(5.0, min(prob, 99.0))

        # Result Column Visualization
        res_col1, res_col2 = st.columns([1.2, 1])

        with res_col1:
            # Linear Percentage Meter using Plotly Gauge
            st.markdown(f"####  Risk of Heart Disease: **{prob:.1f}%**")
            
            # Risk color logic
            if prob < 30: r_color, status = "#58d68d", "LOW RISK"
            elif prob < 70: r_color, status = "#f4d03f", "MODERATE RISK"
            else: r_color, status = "#ff0000", "HIGH RISK"

            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob,
                number = {'suffix': "%", 'font': {'color': "white", 'size': 50}},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'bar': {'color': r_color},
                    'bgcolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 30], 'color': "rgba(88, 214, 141, 0.2)"},
                        {'range': [30, 70], 'color': "rgba(244, 208, 63, 0.2)"},
                        {'range': [70, 100], 'color': "rgba(236, 112, 99, 0.2)"}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': prob
                    }
                }
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font={'color': "white", 'family': "Arial"}, height=350)
            st.plotly_chart(fig_gauge, width='stretch')

        with res_col2:
            st.markdown(f"### Assessment: <span style='color:{r_color};'>{status}</span>", unsafe_allow_html=True)
            
            # Fixed Seaborn Barplot (2026 Future-Proof)
            fig_bar, ax = plt.subplots(figsize=(6, 4))
            fig_bar.patch.set_facecolor('none')
            ax.set_facecolor('none')
            
            # Data for comparison
            data_viz = pd.DataFrame({
                'Metric': ["BP", "Ideal BP", "Chol", "Ideal Chol"],
                'Value': [bp, 120, chol, 200]
            })
            
            # Fixed: Assigning Metric to Hue to avoid FutureWarning
            sns.barplot(data=data_viz, x='Metric', y='Value', hue='Metric', palette="magma", ax=ax, legend=False)
            
            ax.set_title("Vitals vs Optimal Baseline", color="white", weight='bold')
            ax.tick_params(colors='white')
            for spine in ax.spines.values(): spine.set_edgecolor('white')
            st.pyplot(fig_bar)

        # Logging to history
        st.session_state.history.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Age": age,
            "Risk %": f"{prob:.1f}%",
            "Category": status
        })

    # ==========================================
    # -------- AI HEALTH COMPANION --------
    # ==========================================
    st.markdown("---")
    st.subheader("🤖 Smart Health Assistant")
    st.write("Describe your symptoms or ask about specific conditions for immediate guidance.")
    
    chat_input = st.text_input("Enter query (e.g., 'What are the symptoms of high BP?'):")
    
    def handle_ai_response(query):
        q = query.lower()
        if any(w in q for w in ["chest", "pain", "attack", "heart"]):
            return "🚨 **Urgent:** Chest discomfort can be life-threatening. Stop all activity, sit down, and call emergency services immediately."
        elif "bp" in q or "blood pressure" in q:
            return "🩺 **Blood Pressure:** A reading above 140/90 is considered hypertension. Reduce salt intake, stay hydrated, and consult a doctor for a formal diagnosis."
        elif "fever" in q:
            return "🌡️ **Fever:** Normal body temperature is **98.6°F**. If it exceeds 101°F, use cool compresses and rest. Seek help if it persists for more than 48 hours."
        elif "weak" in q or "tired" in q:
            return "🥱 **Fatigue:** This could be linked to iron deficiency, poor sleep, or cardiac strain. Ensure you are getting 7-9 hours of sleep and eating iron-rich greens."
        elif any(w in q for w in ["hi", "hello", "hey"]):
            return "👋 Hello! I am your AI Health Assistant. How can I help you understand your cardiac health today?"
        return "💡 Interesting question. For specific medical advice, I recommend discussing this with a cardiologist. Generally, a balanced diet and 30 minutes of walking daily are best for heart health."

    if st.button("Analyze Query", width='content'):
        if chat_input:
            st.info(handle_ai_response(chat_input))
        else:
            st.warning("Please enter a question first.")

    # UI Guidance Suggestions
    st.markdown("""
        <div class="suggestion-box">
            <div class="suggestion-title">💡 Things you can ask:</div>
            <ul>
                <li>"What should I do if I feel sudden chest tightness?"</li>
                <li>"How can I lower my cholesterol naturally through diet?"</li>
                <li>"What is the difference between Systolic and Diastolic pressure?"</li>
                <li>"Is a heart rate of 110 BPM normal while resting?"</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# -------- HISTORY MODULE --------
# ==========================================
elif menu == "History":
    st.title("📜 Assessment Logs")
    if st.session_state.history:
        h_df = pd.DataFrame(st.session_state.history)
        st.table(h_df)
        
        # Download functionality
        csv_data = h_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Clinical History",
            data=csv_data,
            file_name=f"Health_Report_{st.session_state.user}.csv",
            mime='text/csv',
            width='stretch'
        )
    else:
        st.info("No assessments have been performed in this session yet.")

# ==========================================
# -------- INDIA STATISTICS --------
# ==========================================
elif menu == "India Statistics":
    st.title("🇮🇳 Indian Cardiac Landscape (2026)")
    
    # Yearly trend data
    years = [2022, 2023, 2024, 2025, 2026]
    cases = [65, 72, 80, 89, 98] # Mock millions
    
    st.line_chart(pd.DataFrame({"Projected Cases (Millions)": cases}, index=years))
    
    st.markdown("""
    ### 📈 Critical National Observations
    1. **Early Onset:** Cardiovascular disease in India is appearing **one decade earlier** than in Western countries.
    2. **Urban Risk:** High-density cities like Mumbai and Delhi show 12% higher hypertension rates due to air quality and stress.
    3. **Lifestyle Impact:** 1 in 4 adults in India now suffers from high blood pressure, with sedentary work being the primary driver.
    4. **Dietary Trends:** Excessive use of refined oils and high sodium in street food are major contributors to lipid imbalances.
    """)

# ==========================================
# -------- GLOBAL TRENDS --------
# ==========================================
elif menu == "Global Trends":
    st.title("🌍 Global Cardiovascular Trends")
    
    # Regional Risk Bar Chart
    regions = ["South Asia", "North America", "Europe", "East Asia", "Africa"]
    risk_lvls = [38, 31, 24, 20, 15]
    
    st.bar_chart(pd.DataFrame({"Relative Risk %": risk_lvls}, index=regions))
    
    st.markdown("""
    ### 🌎 Global Health Summary
    * **South Asia (Highest Risk):** Genetics combined with high-carbohydrate diets result in the world's highest cardiac risk profile.
    * **Western Trends:** While smoking rates are down, obesity-related heart failure is rising in the US and UK.
    * **Mediterranean Effect:** Countries like Italy and Greece maintain lower risk levels through high consumption of olive oils and fresh vegetables.
    * **Digital Health:** 2026 has seen a 40% increase in the use of AI tools like this for early detection.
    """)

# ==========================================
# -------- FOOTER & DISCLAIMER --------
# ==========================================
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style="font-size: 11px; color: #888; border-top: 1px solid #444; padding-top: 15px; text-align: center;">
        <b>⚠️ MEDICAL DISCLAIMER:</b> This platform provides AI-generated estimates and general health logic only. 
        It is NOT a clinical diagnosis or medical prescription. In case of severe symptoms or emergency, 
        please consult a licensed healthcare professional or visit a hospital immediately. 
        Calculations are based on statistical probability models.
    </div>
""", unsafe_allow_html=True)
