import streamlit as st
import requests

st.set_page_config(layout='centered', page_title="ER Patient Priority Sorter", page_icon="🏥")

st.markdown("""
<style>
/* Expander boxes (Problem / Solution) */
[data-testid="stExpander"] {
    background-color: #241414;
    border-radius: 14px;
    border: 1px solid #B0000844;
}
[data-testid="stExpander"] summary {
    background-color: #5C0F0F !important;
    border-radius: 14px 14px 0 0 !important;
}
[data-testid="stExpander"] li::marker {
    color: #D91E1E;
}
[data-testid="stExpander"] details[open] > div {
    min-height: 340px;
}

/* Divider under subheaders */
hr {
    border-color: #B00008 !important;
}

/* ESI tab cards */
[class*="st-key-esi_card_1"] {
    background-color: #241414;
    border-radius: 16px;
    border-left: 5px solid #B33A3A;
    padding: 20px;
}
[class*="st-key-esi_card_2"] {
    background-color: #241414;
    border-radius: 16px;
    border-left: 5px solid #C96450;
    padding: 20px;
}
[class*="st-key-esi_card_3"] {
    background-color: #241414;
    border-radius: 16px;
    border-left: 5px solid #D98D6F;
    padding: 20px;
}
[class*="st-key-esi_card_4"] {
    background-color: #241414;
    border-radius: 16px;
    border-left: 5px solid #E5AE8F;
    padding: 20px;
}
[class*="st-key-esi_card_5"] {
    background-color: #241414;
    border-radius: 16px;
    border-left: 5px solid #e9bc79;
    padding: 20px;
}

/* ESI metric label colors, matched per card */
[class*="st-key-esi_card_1"] [data-testid="stMetricLabel"] { color: #B33A3A; }
[class*="st-key-esi_card_2"] [data-testid="stMetricLabel"] { color: #C96450; }
[class*="st-key-esi_card_3"] [data-testid="stMetricLabel"] { color: #D98D6F; }
[class*="st-key-esi_card_4"] [data-testid="stMetricLabel"] { color: #E5AE8F; }
[class*="st-key-esi_card_5"] [data-testid="stMetricLabel"] { color: #e9bc79; }

/* Buttons */
.stButton button {
    background-color: #B00008;
    color: #FFFFFF;
    border: none;
    font-weight: 700;
    font-size: 18px;
    padding: 16px 40px;
    border-radius: 10px;
    width: 100%;
    transition: all 0.2s ease;
}
.stButton button:hover {
    background-color: #D91E1E;
    color: #FFFFFF;
    transform: scale(1.02);
}

/* Form submit button */
.stFormSubmitButton button {
    background-color: #B00008 !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700;
    font-size: 18px;
    padding: 16px 40px;
    border-radius: 10px;
    width: 100%;
}
.stFormSubmitButton button:hover {
    background-color: #D91E1E !important;
    color: #FFFFFF !important;
}

/* Preset buttons — compact style */
[class*="st-key-preset_"] button {
    font-size: 13px !important;
    padding: 8px 4px !important;
    white-space: nowrap !important;
    min-height: 40px;
}
[class*="st-key-preset_"] {
    display: flex;
    justify-content: center;
}

/* Model Details container (key-based, reliable) */
[class*="st-key-model_details"] {
    background-color: #241414;
    border-radius: 14px;
    border: 1px solid #B0000844;
}
[class*="st-key-model_details"] li::marker {
    color: #D91E1E;
}
[class*="st-key-model_details"] code {
    background-color: #331A1A !important;
    color: #FF8A7A !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #241414;
    border-right: 1px solid #B0000844;
}
[data-testid="stSidebarNav"] a {
    color: #FFFFFF !important;
    font-size: 20px !important;
    font-weight: 700;
    padding: 20px 16px !important;
    margin: 8px 0;
    display: block;
    border-radius: 10px;
}
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background-color: #B00008 !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebarNav"] a:hover {
    background-color: #331A1A;
    border-radius: 8px;
}

/* Input field backgrounds (text, number, select) — merged into one rule */
input[type="number"], input[type="text"],
[data-baseweb="select"] > div {
    background-color: #331A1A !important;
    color: #FFFFFF !important;
    border: 1px solid #B0000844 !important;
}
[data-testid="stHorizontalBlock"] {
    display: flex;
    justify-content: center;
    gap: 12px;
}
[data-testid="stHorizontalBlock"] > div {
    flex: 0 0 auto !important;
    width: auto !important;
}
</style>
""", unsafe_allow_html=True)

presets = {
    "🚔 Gunshot Victim": {
        'age_input': 29, 'gender_input': 'Male', 'arrival_mode_input': 'Police',
        'heart_rate_input': 158, 'systolic_bp_input': 70, 'diastolic_bp_input': 42,
        'respiratory_rate_input': 35, 'spo2_input': 75.0, 'temperature_c_input': 37.0,
        'pain_score_input': 9, 'gcs_total_input': 7, 'consciousness_level_input': 'Pain',
        'chief_complaint_input': 'Severe Trauma', 'comorbidities_input': 0,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 0,
    },
    "❤️ Heart Attack": {
    'age_input': 63, 'gender_input': 'Male', 'arrival_mode_input': 'Ambulance',
    'heart_rate_input': 122, 'systolic_bp_input': 89, 'diastolic_bp_input': 56,
    'respiratory_rate_input': 25, 'spo2_input': 92.0, 'temperature_c_input': 37.0,
    'pain_score_input': 8, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
    'chief_complaint_input': 'Chest Pain', 'comorbidities_input': 2,
    'immunocompromised_input': 'No', 'prior_ed_visits_input': 1,
    },
    "🧠 Stroke Symptoms": {
    'age_input': 74, 'gender_input': 'Female', 'arrival_mode_input': 'Ambulance',
    'heart_rate_input': 108, 'systolic_bp_input': 182, 'diastolic_bp_input': 104,
    'respiratory_rate_input': 22, 'spo2_input': 93.0, 'temperature_c_input': 37.0,
    'pain_score_input': 2, 'gcs_total_input': 14, 'consciousness_level_input': 'Alert',
    'chief_complaint_input': 'Stroke Symptoms', 'comorbidities_input': 3,
    'immunocompromised_input': 'No', 'prior_ed_visits_input': 2,
    },
    "😵 Unresponsive Patient": {
        'age_input': 45, 'gender_input': 'Male', 'arrival_mode_input': 'Ambulance',
        'heart_rate_input': 38, 'systolic_bp_input': 68, 'diastolic_bp_input': 42,
        'respiratory_rate_input': 8, 'spo2_input': 74.0, 'temperature_c_input': 34.5,
        'pain_score_input': 0, 'gcs_total_input': 4, 'consciousness_level_input': 'Unresponsive',
        'chief_complaint_input': 'Severe Trauma', 'comorbidities_input': 1,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 0,
    },
    "🫁 Asthma Attack": {
    'age_input': 19, 'gender_input': 'Female', 'arrival_mode_input': 'Ambulance',
    'heart_rate_input': 118, 'systolic_bp_input': 90, 'diastolic_bp_input': 62,
    'respiratory_rate_input': 27, 'spo2_input': 91.0, 'temperature_c_input': 37.0,
    'pain_score_input': 5, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
    'chief_complaint_input': 'Shortness of Breath', 'comorbidities_input': 1,
    'immunocompromised_input': 'No', 'prior_ed_visits_input': 3,
    },
    "🙍‍♀️ Abdominal Pain": {
        'age_input': 40, 'gender_input': 'Female', 'arrival_mode_input': 'Walk-in',
        'heart_rate_input': 84, 'systolic_bp_input': 122, 'diastolic_bp_input': 78,
        'respiratory_rate_input': 17, 'spo2_input': 97.5, 'temperature_c_input': 37.4,
        'pain_score_input': 6, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
        'chief_complaint_input': 'Abdominal Pain', 'comorbidities_input': 1,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 1,
    },
    "🤒 High Fever": {
        'age_input': 6, 'gender_input': 'Male', 'arrival_mode_input': 'Walk-in',
        'heart_rate_input': 100, 'systolic_bp_input': 108, 'diastolic_bp_input': 68,
        'respiratory_rate_input': 20, 'spo2_input': 97.0, 'temperature_c_input': 39.4,
        'pain_score_input': 3, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
        'chief_complaint_input': 'Fever', 'comorbidities_input': 0,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 0,
    },
    "🤕 Minor Cut": {
        'age_input': 25, 'gender_input': 'Female', 'arrival_mode_input': 'Walk-in',
        'heart_rate_input': 80, 'systolic_bp_input': 122, 'diastolic_bp_input': 78,
        'respiratory_rate_input': 16, 'spo2_input': 98.0, 'temperature_c_input': 36.9,
        'pain_score_input': 4, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
        'chief_complaint_input': 'Laceration', 'comorbidities_input': 0,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 0,
    },
    "🧓 Elderly Fall": {
        'age_input': 81, 'gender_input': 'Female', 'arrival_mode_input': 'Walk-in',
        'heart_rate_input': 82, 'systolic_bp_input': 128, 'diastolic_bp_input': 80,
        'respiratory_rate_input': 17, 'spo2_input': 96.5, 'temperature_c_input': 36.6,
        'pain_score_input': 4, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
        'chief_complaint_input': 'Laceration', 'comorbidities_input': 2,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 1,
    },
    "💊 Prescription Refill": {
        'age_input': 30, 'gender_input': 'Other', 'arrival_mode_input': 'Walk-in',
        'heart_rate_input': 74, 'systolic_bp_input': 118, 'diastolic_bp_input': 76,
        'respiratory_rate_input': 15, 'spo2_input': 98.5, 'temperature_c_input': 36.9,
        'pain_score_input': 0, 'gcs_total_input': 15, 'consciousness_level_input': 'Alert',
        'chief_complaint_input': 'Prescription Refill', 'comorbidities_input': 0,
        'immunocompromised_input': 'No', 'prior_ed_visits_input': 4,
    },
}

st.title("**ER Patient Priority Sorter**", text_alignment="center")
st.caption('**A machine learning model that predicts Emergency Severity Index (ESI) — built end-to-end, from data to deployment.**', text_alignment='center')
st.space(size='xsmall')

st.header('Try The Model ↓', text_alignment="center")
st.space(size='xsmall')

with st.expander("**Quick Fill A Scenario**", expanded=False):
    col1, col2, col3, col4, col5 = st.columns(5)

    if col1.button("🚔 Shooting", help="29yo male, gunshot wound, low BP and SpO2 — expect ESI 1, High deterioration risk, High admission likelihood", key="preset_1"):
        for key, value in presets["🚔 Gunshot Victim"].items():
            st.session_state[key] = value
        st.rerun()

    if col2.button("❤️ Cardiac", help="63yo male, chest pain, low BP/SpO2 — expect ESI 2, High deterioration risk, Moderate admission likelihood", key="preset_2"):
        for key, value in presets["❤️ Heart Attack"].items():
            st.session_state[key] = value
        st.rerun()

    if col3.button("🧠 Stroke", help="74yo female, stroke symptoms, high BP, reduced consciousness — expect ESI 2, Medium deterioration risk, High admission likelihood", key="preset_3"):
        for key, value in presets["🧠 Stroke Symptoms"].items():
            st.session_state[key] = value
        st.rerun()

    if col4.button("😵 Critical", help="45yo male, unresponsive, very low vitals across the board — expect ESI 1, High deterioration risk, High admission likelihood", key="preset_4"):
        for key, value in presets["😵 Unresponsive Patient"].items():
            st.session_state[key] = value
        st.rerun()

    if col5.button("🫁 Asthma", help="19yo female, shortness of breath, low SpO2, elevated heart rate — expect ESI 2, High deterioration risk, High admission likelihood", key="preset_5"):
        for key, value in presets["🫁 Asthma Attack"].items():
            st.session_state[key] = value
        st.rerun()

    col6, col7, col8, col9, col10 = st.columns(5)

    if col6.button("🙍‍♀️ Abdominal", help="40yo female, abdominal pain, mild fever, stable vitals — expect ESI 3, Low deterioration risk, Low admission likelihood", key="preset_6"):
        for key, value in presets["🙍‍♀️ Abdominal Pain"].items():
            st.session_state[key] = value
        st.rerun()

    if col7.button("🤒 Fever", help="6yo male, high fever, elevated heart rate, otherwise stable — expect ESI 3, Medium deterioration risk, Low admission likelihood", key="preset_7"):
        for key, value in presets["🤒 High Fever"].items():
            st.session_state[key] = value
        st.rerun()

    if col8.button("🤕 Cut", help="25yo female, minor laceration, all vitals normal — expect ESI 4, Low deterioration risk, Low admission likelihood", key="preset_8"):
        for key, value in presets["🤕 Minor Cut"].items():
            st.session_state[key] = value
        st.rerun()

    if col9.button("🧓 Fall", help="81yo female, fall injury, multiple comorbidities — expect ESI 3, Low deterioration risk, Moderate admission likelihood", key="preset_9"):
        for key, value in presets["🧓 Elderly Fall"].items():
            st.session_state[key] = value
        st.rerun()

    if col10.button("💊 Refill", help="30yo, routine prescription refill, all vitals normal — expect ESI 5, Low deterioration risk, Low admission likelihood", key="preset_10"):
        for key, value in presets["💊 Prescription Refill"].items():
            st.session_state[key] = value
        st.rerun()
    st.space(size = "small")
    st.markdown('''
    Each scenario fills in **all 16 fields** the model uses — realistic vitals, symptoms, and history for that kind of case.

    Click any button above to **instantly load a scenario**, then scroll down to review and adjust before submitting. Prefer to build your own patient from scratch? Just start typing into the fields below and skip the presets entirely.
    ''')
with st.form(key="testing", enter_to_submit=False, border=True, clear_on_submit=False):

    st.subheader('Demographics', text_alignment='center')
    st.caption('Basic info about who the patient is and how they arrived.', text_alignment="center")
    Age = st.number_input('Age', value=None, placeholder='1 – 95', min_value=1, max_value=95, help="Patient's age in years. Range: 1–95.", key='age_input')
    Gender = st.selectbox('Gender', ['Male', 'Female', 'Other'], help="Patient's gender", key='gender_input')
    Arrival_Mode = st.selectbox('Arrival Mode', ['Ambulance', 'Walk-in', 'Police', 'Transfer'], help="How the patient arrived at the ER. Ambulance/Police arrivals often signal higher acuity.", key='arrival_mode_input')

    st.subheader('Vitals', text_alignment='center')
    st.caption('The core physiological numbers a nurse checks first.', text_alignment="center")
    Heart_Rate = st.number_input('Heart Rate', value=None, min_value=30, max_value=180, placeholder='30 – 180', help="Pulse, in beats per minute. Normal resting range: 60–100. Range: 30–180.", key='heart_rate_input')
    Systolic_BP = st.number_input('Systolic BP', value=None, min_value=60, max_value=220, placeholder="60 – 220", help="Top blood pressure number — pressure when the heart pumps. Range: 60–220.", key='systolic_bp_input')
    Diastolic_BP = st.number_input('Diastolic BP', value=None, min_value=40, max_value=130, placeholder="40 – 130", help="Bottom blood pressure number — pressure between heartbeats. Range: 40–130.", key='diastolic_bp_input')
    Respiratory_Rate = st.number_input('Respiratory Rate', value=None, min_value=8, max_value=40, placeholder="8 – 40", help="Breaths per minute. Normal range: 12–20. Range: 8–40.", key='respiratory_rate_input')
    SpO2 = st.number_input('SpO2', value=None, min_value=70.0, max_value=100.0, step=0.1, placeholder="70.0 – 100.0", help="Blood oxygen saturation (%). Normal: 95–100%. Below 90% is dangerous. Range: 70.0–100.0.", key='spo2_input')
    Temperature = st.number_input('Temperature (C)', value=None, min_value=34.0, max_value=40.5, step=0.1, placeholder='34.0 – 40.5', help='Body temperature in Celsius. Normal: 36.5–37.5°C. Range: 34.0–40.5.', key='temperature_c_input')

    st.space('xxsmall')
    st.subheader('Clinical Assessment', text_alignment='center')
    st.caption('How the patient is doing right now, in their own words and yours.', text_alignment="center")
    Pain_Score = st.slider('Pain Score', value=None, min_value=0, max_value=10, help="Self-reported pain level, 0 (none) to 10 (worst imaginable). Range: 0–10.", key='pain_score_input')
    GCS_Total = st.number_input('GCS Total', value=None, min_value=3, max_value=15, placeholder="3 – 15", help="Glasgow Coma Scale — measures alertness. Below 8 signals severe impairment. Range: 3–15.", key='gcs_total_input')
    Consciousness_Level = st.selectbox('Consciousness Level', ['Alert', 'Voice', 'Pain', 'Unresponsive'], help="AVPU scale, in order of decreasing responsiveness: Alert → Voice → Pain → Unresponsive.", key='consciousness_level_input')
    Chief_Complaint = st.selectbox('Chief Complaint', ['Chest Pain', 'Shortness of Breath', 'Laceration', 'Fever', 'Abdominal Pain', 'Stroke Symptoms', 'Prescription Refill', 'Severe Trauma'], help='The primary reason for the ER visit.', key='chief_complaint_input')

    st.subheader('History', text_alignment='center')
    st.caption('Background that shifts how risky this visit really is.', text_alignment="center")
    Comorbidities = st.number_input('Comorbidities', value=None, min_value=0, max_value=5, placeholder="0 – 5", help="Number of existing health conditions (diabetes, hypertension, asthma, etc.). Range: 0–5.", key='comorbidities_input')
    Immunocompromised = st.selectbox('Immunocompromised', ['No', 'Yes'], help="Whether the patient has a weakened immune system.", key='immunocompromised_input')
    Prior_ED_Visits = st.number_input('Prior ED Visits (12mo)', value=None, min_value=0, max_value=10, placeholder="0 – 10", help="Number of ER visits in the past 12 months. Range: 0–10.", key='prior_ed_visits_input')

    submitted = st.form_submit_button("Submit", width=1400)

    if submitted:
        if None in [Age, Heart_Rate, Systolic_BP, Diastolic_BP, Respiratory_Rate, SpO2, Temperature, GCS_Total, Comorbidities, Prior_ED_Visits]:
            st.error("Please fill in all fields before submitting.")
        else:
            with st.spinner('Predicting ESI level...'):
                is_immunocompromised_map = {"Yes": 1, "No": 0}
                is_immunocompromised_encoded = is_immunocompromised_map[Immunocompromised]

                dictionary = {
                    'age': Age,
                    'gender': Gender,
                    'arrival_mode': Arrival_Mode,
                    'heart_rate': Heart_Rate,
                    'systolic_bp': Systolic_BP,
                    'diastolic_bp': Diastolic_BP,
                    'respiratory_rate': Respiratory_Rate,
                    'spo2': SpO2,
                    'temperature_c': Temperature,
                    'pain_score': Pain_Score,
                    'gcs_total': GCS_Total,
                    'consciousness_level': Consciousness_Level,
                    'chief_complaint': Chief_Complaint,
                    'num_comorbidities': Comorbidities,
                    'is_immunocompromised': is_immunocompromised_encoded,
                    'num_prior_ed_visits_12m': Prior_ED_Visits,
                }
                response = requests.post('https://er-patient-priority-sorter.fastapicloud.dev/input', json=dictionary)
                result = response.json()
                predicted_esi = result['esi_level']
                confidence = result['confidence']
                deterioration_risk = result['deterioration_risk']
                admission_likelihood = result['admission_likelihood']

                esi_labels = {1: "Immediate", 2: "Emergent", 3: "Urgent", 4: "Less Urgent", 5: "Non-Urgent"}
                esi_colors = {1: "#B33A3A", 2: "#C96450", 3: "#D98D6F", 4: "#E5AE8F", 5: "#e9bc79"}
                deterioration_colors = {"Low": "#e9bc79", "Medium": "#C96450", "High": "#B33A3A"}
                admission_colors = {"Low": "#e9bc79", "Moderate": "#C96450", "High": "#B33A3A"}

                st.markdown(
                    f"<div style='background:#241414; border-radius:14px; border-left:5px solid {esi_colors[predicted_esi]}; "
                    f"padding:20px; margin-top:16px;'>"
                    f"<p style='color:{esi_colors[predicted_esi]}; font-size:13px; text-transform:uppercase; margin:0 0 6px; font-weight:700;'>Model Predicts</p>"
                    f"<p style='color:#FFFFFF; font-size:26px; font-weight:800; margin:0 0 8px;'>ESI {predicted_esi} — {esi_labels[predicted_esi]}</p>"
                    f"<p style='color:#C9BBA8; font-size:14px; margin:0 0 14px;'>Confidence: {confidence:.0%}</p>"
                    f"<span style='background:{deterioration_colors[deterioration_risk]}; color:#2A1A14; font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>Deterioration Risk: {deterioration_risk}</span>"
                    f"&nbsp;&nbsp;"
                    f"<span style='background:{admission_colors[admission_likelihood]}; color:#2A1A14; font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>Admission: {admission_likelihood}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )

if st.button("← Back"):
    st.switch_page("intro.py")
