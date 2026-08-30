from ast import alias
from ast import Pass
from matplotlib.pyplot import text
from fastapi.datastructures import Default
import streamlit as st 
import requests

st.set_page_config(layout= 'wide', page_title="ER Patient Priority Sorter", page_icon="🏥")

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
    min-height: 420px;
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
[class*="st-key-esi_card_1"] [data-testid="stMetricLabel"] {
    color: #B33A3A;
}
[class*="st-key-esi_card_2"] [data-testid="stMetricLabel"] {
    color: #C96450;
}
[class*="st-key-esi_card_3"] [data-testid="stMetricLabel"] {
    color: #D98D6F;
}
[class*="st-key-esi_card_4"] [data-testid="stMetricLabel"] {
    color: #E5AE8F;
}
[class*="st-key-esi_card_5"] [data-testid="stMetricLabel"] {
    color: #e9bc79;
}

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

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #241414;
    border-right: 1px solid #B0000844;
}

/* Sidebar nav links */
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
    background-color: #5C0F0F;
}
</style>
""", unsafe_allow_html=True)



st.title("**ER Patient Priority Sorter**", text_alignment = "center")
st.caption('**A machine learning model that predicts Emergency Severity Index (ESI) — built end-to-end, from data to deployment.**' , text_alignment = 'center')
st.space(size = 'medium')




col1 , col2  = st.columns(spec = 2 , vertical_alignment = 'top', gap = 'large')

with col1:
    with st.expander(label = 'The Problem ⛔', expanded = True):
        st.markdown('''***Manual triage has a <span style='color:#D91E1E;'>real cost</span>.***

Traditional ER triage relies entirely on manual staff evaluation — not just to gauge urgency, but to judge how a patient might deteriorate and whether they'll need admission. That judgment grows harder to sustain as patient volume rises, staff fatigue sets in, and the margin for error shrinks during peak hours.

- Inconsistent assessment speeds under pressure
- **Under-triaging** delays life-saving care
- **Over-triaging** wastes limited resources
- Deterioration risk and admission needs are often assessed only after urgency, not alongside it

Speed and accuracy both suffer when triage depends on judgment alone.''',unsafe_allow_html=True)

with col2:
    with st.expander(label = 'The Solution ✅', expanded = True):
        st.markdown('''***A <span style='color:#D91E1E;'>decision-support layer</span>, not a replacement for clinicians.***

This system predicts three things at once from a patient's vitals, symptoms, and history: their **Emergency Severity Index (ESI)** — from 1 (immediate resuscitation) to 5 (non-urgent) — their **deterioration risk**, and their **likelihood of hospital admission**. Instead of assessing each of these separately, the model surfaces all three together the moment a patient's information is entered, giving staff a fuller picture in a single pass.

- Fast, consistent first-pass priority across all three predictions
- A human always stays in control of the final call
- Designed to catch critical cases quickly, and flag who might need closer watching or a longer stay

The model suggests, the clinician decides''',unsafe_allow_html=True)





st.space(size = 'medium')

st.header('**The Details** **⬇**' , text_alignment= "center")

st.space(size  = 'small')

with st.container(border = True, key = "model_details"):
    st.markdown('''
***Built end-to-end — dataset, model, API, and interface, all from scratch.***

**<span style='color:#FF8A7A;'>Dataset</span>**
- 5,000 synthetic patient records, three target labels: ESI level, deterioration risk, and admission likelihood
- Hard clinical rules enforced (e.g. GCS < 8 → always ESI 1)
- Realistic class imbalance across all three targets, mirroring real-world distributions
- Light label noise to simulate real-world disagreement, tuned so accuracy reflects genuine difficulty, not memorization

**<span style='color:#FF8A7A;'>Model</span>**
- Three separate `RandomForestClassifier` models, same 16 input features, each trained on a different target
- `class_weight='balanced'` for rare critical cases across all three
- <span style='color:#D91E1E; font-weight:700;'>90%</span> accuracy on ESI level · <span style='color:#D91E1E; font-weight:700;'>82%</span> on deterioration risk · <span style='color:#D91E1E; font-weight:700;'>85%</span> on admission likelihood

**<span style='color:#FF8A7A;'>Backend</span>**
- FastAPI serving a `/input` prediction endpoint and a live `/queue` endpoint
- All three models loaded once at startup and run together on every request
- Categorical fields validated with strict typing, numeric fields bounded to realistic clinical ranges
- Patient records — including all three predictions — stored and served from a live, sortable queue

**<span style='color:#FF8A7A;'>Frontend</span>**
- Built entirely in Streamlit — this interface, and the "Try It Yourself" prediction page
- Native multi-page navigation with a custom sidebar
- All three predictions displayed together for every patient, not just urgency

**<span style='color:#FF8A7A;'>Notes</span>**
- Synthetic data, not real hospital records
- No human-override step yet — a demo, not a clinical tool''',unsafe_allow_html=True)
st.space(size = 'medium')



st.header ('See It In Action ▼', text_alignment="center")

response = requests.get('http://127.0.0.1:8000/queue')
queue = response.json()
esi_labels = {1: "Immediate", 2: "Emergent", 3: "Urgent", 4: "Less Urgent", 5: "Non-Urgent"}
esi_colors = {1: "#B33A3A", 2: "#C96450",3: "#D98D6F",4: "#E5AE8F",5: "#e9bc79"}
deterioration_colors = {"Low": "#e9bc79", "Medium": "#C96450", "High": "#B33A3A"}
admission_colors = {"Low": "#e9bc79", "Moderate": "#C96450", "High": "#B33A3A"}
tab1 , tab2 , tab3 , tab4 , tab5 = st.tabs(['**ESI 1**','**ESI 2**','**ESI 3**','**ESI 4**','**ESI 5**'], width = 1000)

with tab1:
    for i in queue:
        if i['id'] == 1:
            esi1 = i

    with st.container(border=True, key="esi_card_1"):
        st.markdown(
            f"<span style='background:{esi_colors[esi1['esi_level']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"ESI {esi1['esi_level']} — {esi_labels[esi1['esi_level']].upper()}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{deterioration_colors[esi1['deterioration_risk']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Deterioration Risk: {esi1['deterioration_risk']}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{admission_colors[esi1['admission_likelihood']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Admission: {esi1['admission_likelihood']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {esi1['age']}-year-old {esi1['gender'].lower()}")
        st.markdown(f"Arrived by {esi1['arrival_mode']} · *{esi1['chief_complaint']}*")

        st.write("")

        a, b, c, d = st.columns(4, gap="medium")
        a.metric(label='HEART RATE', value=f"{esi1['heart_rate']} bpm")
        b.metric(label='SPO2', value=f"{esi1['spo2']}%")
        c.metric(label='GCS', value=f"{esi1['gcs_total']}/15")
        d.metric(label='PAIN', value=f"{esi1['pain_score']}/10")

        st.caption(f"Consciousness: {esi1['consciousness_level']} · Systolic BP {esi1['systolic_bp']} · Comorbidities: {esi1['num_comorbidities']}")

with tab2:
    for i in queue:
        if i['id'] == 2:
            esi2 = i

    with st.container(border=True, key="esi_card_2"):
        st.markdown(
            f"<span style='background:{esi_colors[esi2['esi_level']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"ESI {esi2['esi_level']} — {esi_labels[esi2['esi_level']].upper()}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{deterioration_colors[esi2['deterioration_risk']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Deterioration Risk: {esi2['deterioration_risk']}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{admission_colors[esi2['admission_likelihood']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Admission: {esi2['admission_likelihood']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {esi2['age']}-year-old {esi2['gender'].lower()}")
        st.markdown(f"Arrived by {esi2['arrival_mode']} · *{esi2['chief_complaint']}*")

        st.write("")

        a, b, c, d = st.columns(4, gap="medium")
        a.metric(label='HEART RATE', value=f"{esi2['heart_rate']} bpm")
        b.metric(label='SPO2', value=f"{esi2['spo2']}%")
        c.metric(label='GCS', value=f"{esi2['gcs_total']}/15")
        d.metric(label='PAIN', value=f"{esi2['pain_score']}/10")

        st.caption(f"Consciousness: {esi2['consciousness_level']} · Systolic BP {esi2['systolic_bp']} · Comorbidities: {esi2['num_comorbidities']}")


with tab3:
    for i in queue:
        if i['id'] == 3:
            esi3 = i

    with st.container(border=True, key="esi_card_3"):
        st.markdown(
            f"<span style='background:{esi_colors[esi3['esi_level']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"ESI {esi3['esi_level']} — {esi_labels[esi3['esi_level']].upper()}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{deterioration_colors[esi3['deterioration_risk']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Deterioration Risk: {esi3['deterioration_risk']}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{admission_colors[esi3['admission_likelihood']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Admission: {esi3['admission_likelihood']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {esi3['age']}-year-old {esi3['gender'].lower()}")
        st.markdown(f"Arrived by {esi3['arrival_mode']} · *{esi3['chief_complaint']}*")

        st.write("")

        a, b, c, d = st.columns(4, gap="medium")
        a.metric(label='HEART RATE', value=f"{esi3['heart_rate']} bpm")
        b.metric(label='SPO2', value=f"{esi3['spo2']}%")
        c.metric(label='GCS', value=f"{esi3['gcs_total']}/15")
        d.metric(label='PAIN', value=f"{esi3['pain_score']}/10")

        st.caption(f"Consciousness: {esi3['consciousness_level']} · Systolic BP {esi3['systolic_bp']} · Comorbidities: {esi3['num_comorbidities']}")

with tab4:
    for i in queue:
        if i['id'] == 4:
            esi4 = i

    with st.container(border=True, key="esi_card_4"):
        st.markdown(
            f"<span style='background:{esi_colors[esi4['esi_level']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"ESI {esi4['esi_level']} — {esi_labels[esi4['esi_level']].upper()}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{deterioration_colors[esi4['deterioration_risk']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Deterioration Risk: {esi4['deterioration_risk']}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{admission_colors[esi4['admission_likelihood']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Admission: {esi4['admission_likelihood']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {esi4['age']}-year-old {esi4['gender'].lower()}")
        st.markdown(f"Arrived by {esi4['arrival_mode']} · *{esi4['chief_complaint']}*")

        st.write("")

        a, b, c, d = st.columns(4, gap="medium")
        a.metric(label='HEART RATE', value=f"{esi4['heart_rate']} bpm")
        b.metric(label='SPO2', value=f"{esi4['spo2']}%")
        c.metric(label='GCS', value=f"{esi4['gcs_total']}/15")
        d.metric(label='PAIN', value=f"{esi4['pain_score']}/10")

        st.caption(f"Consciousness: {esi4['consciousness_level']} · Systolic BP {esi4['systolic_bp']} · Comorbidities: {esi4['num_comorbidities']}")

with tab5:
    for i in queue:
        if i['id'] == 5:
            esi5 = i

    with st.container(border=True, key="esi_card_5"):
        st.markdown(
            f"<span style='background:{esi_colors[esi5['esi_level']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"ESI {esi5['esi_level']} — {esi_labels[esi5['esi_level']].upper()}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{deterioration_colors[esi5['deterioration_risk']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Deterioration Risk: {esi5['deterioration_risk']}</span>"
            f"&nbsp;&nbsp;"
            f"<span style='background:{admission_colors[esi5['admission_likelihood']]}; color:#2A1A14; "
            f"font-weight:700; padding:6px 16px; border-radius:999px; font-size:13px;'>"
            f"Admission: {esi5['admission_likelihood']}</span>",
            unsafe_allow_html=True
        )

        st.markdown(f"### {esi5['age']}-year-old {esi5['gender'].lower()}")
        st.markdown(f"Arrived by {esi5['arrival_mode']} · *{esi5['chief_complaint']}*")

        st.write("")

        a, b, c, d = st.columns(4, gap="medium")
        a.metric(label='HEART RATE', value=f"{esi5['heart_rate']} bpm")
        b.metric(label='SPO2', value=f"{esi5['spo2']}%")
        c.metric(label='GCS', value=f"{esi5['gcs_total']}/15")
        d.metric(label='PAIN', value=f"{esi5['pain_score']}/10")

        st.caption(f"Consciousness: {esi5['consciousness_level']} · Systolic BP {esi5['systolic_bp']} · Comorbidities: {esi5['num_comorbidities']}")

st.space(size='xxsmall')

st.subheader('***Quick Reference***', text_alignment="center")
st.space(size = 'xsmall')
with st.expander(label='What do these terms mean?', expanded=True):
    st.markdown('''
The demo cards above show just 4 of the 16 parameters the model actually uses — heart rate, SpO2, GCS, and pain score — chosen because they're the fastest way to get a sense of a patient's condition at a glance. Whichever ESI level, deterioration risk, and admission likelihood got predicted, all three models actually looked at every one of the 16 inputs behind the scenes to get there.

**The 5 ESI Levels**

- 🔴 **ESI 1 — Immediate:** Life-threatening, needs resuscitation now
- 🟠 **ESI 2 — Emergent:** High-risk, can't safely wait
- 🟡 **ESI 3 — Urgent:** Needs real workup, but stable
- 🟤 **ESI 4 — Less Urgent:** One simple resource needed
- ⚪ **ESI 5 — Non-Urgent:** Doesn't need ER-level resources

**Deterioration Risk**

- 🟤 **Low:** Vitals are stable, unlikely to worsen while waiting
- 🟠 **Medium:** Some abnormal vitals, worth closer monitoring
- 🔴 **High:** Multiple vitals trending dangerously, needs prompt attention

**Admission Likelihood**

- 🟤 **Low:** Likely to be treated and discharged the same day
- 🟠 **Moderate:** Could go either way, depends on how they respond to treatment
- 🔴 **High:** Likely to be kept for further care or observation

**All 16 Parameters, Explained**

**<span style='color:#FF8A7A;'>Vitals</span>**
- **Heart Rate:** Beats per minute · normal range is 60–100
- **SpO2:** Blood oxygen saturation (%) · normal is 95–100%, below 90% is dangerous
- **Systolic / Diastolic BP:** Blood pressure, e.g. "120/80"
- **Respiratory Rate:** Breaths per minute · normal is 12–20
- **Temperature:** Body temperature in Celsius

**<span style='color:#FF8A7A;'>Clinical Assessment</span>**
- **GCS (Glasgow Coma Scale):** Measures alertness, 3–15 · below 8 signals severe impairment
- **Pain Score:** Self-reported, 0 (none) to 10 (worst imaginable)
- **Consciousness Level:** Alert → Voice → Pain → Unresponsive
- **Chief Complaint:** The primary reason for the visit

**<span style='color:#FF8A7A;'>Demographics & History</span>**
- **Age, Gender, Arrival Mode:** Basic patient and context info
- **Comorbidities:** Number of existing conditions
- **Immunocompromised:** Weakened immune system, yes/no
- **Prior ER Visits (12mo):** ER visit frequency in the past year
''',unsafe_allow_html=True)

st.space(size='medium')

st.header('Try The Model And See For Yourself!', text_alignment="center")
st.space(size = 'small')
if st.button("**Try It Yourself**",type = "primary",width=1500):
    st.switch_page("test.py")