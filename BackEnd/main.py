# import uvicorn
# from pydantic import BaseModel
from pandas.core.interchange import dataframe
from fastapi import FastAPI
from data_model import Input_Variables
import joblib
import pandas as pd

patient_queue = [
    {
        "age": 68, "gender": "Male", "arrival_mode": "Ambulance",
        "heart_rate": 145, "systolic_bp": 78, "diastolic_bp": 48,
        "respiratory_rate": 32, "spo2": 84, "temperature_c": 38.9,
        "pain_score": 9, "gcs_total": 9, "consciousness_level": "Pain",
        "chief_complaint": "Severe Trauma", "num_comorbidities": 3,
        "is_immunocompromised": 0, "num_prior_ed_visits_12m": 2,
        "id": 1, "esi_level": 1, "deterioration_risk": "High", "admission_likelihood": "High"
    },
    {
        "age": 55, "gender": "Female", "arrival_mode": "Ambulance",
        "heart_rate": 118, "systolic_bp": 92, "diastolic_bp": 60,
        "respiratory_rate": 24, "spo2": 91, "temperature_c": 37.2,
        "pain_score": 8, "gcs_total": 15, "consciousness_level": "Alert",
        "chief_complaint": "Chest Pain", "num_comorbidities": 2,
        "is_immunocompromised": 0, "num_prior_ed_visits_12m": 1,
        "id": 2, "esi_level": 2, "deterioration_risk": "Medium", "admission_likelihood": "High"
    },
    {
        "age": 40, "gender": "Male", "arrival_mode": "Walk-in",
        "heart_rate": 92, "systolic_bp": 128, "diastolic_bp": 82,
        "respiratory_rate": 18, "spo2": 97, "temperature_c": 38.4,
        "pain_score": 6, "gcs_total": 15, "consciousness_level": "Alert",
        "chief_complaint": "Abdominal Pain", "num_comorbidities": 1,
        "is_immunocompromised": 0, "num_prior_ed_visits_12m": 1,
        "id": 3, "esi_level": 3, "deterioration_risk": "Low", "admission_likelihood": "Low"
    },
    {
        "age": 25, "gender": "Female", "arrival_mode": "Walk-in",
        "heart_rate": 78, "systolic_bp": 118, "diastolic_bp": 76,
        "respiratory_rate": 16, "spo2": 99, "temperature_c": 37.0,
        "pain_score": 4, "gcs_total": 15, "consciousness_level": "Alert",
        "chief_complaint": "Laceration", "num_comorbidities": 0,
        "is_immunocompromised": 0, "num_prior_ed_visits_12m": 0,
        "id": 4, "esi_level": 4, "deterioration_risk": "Low", "admission_likelihood": "Low"
    },
    {
        "age": 31, "gender": "Male", "arrival_mode": "Walk-in",
        "heart_rate": 72, "systolic_bp": 116, "diastolic_bp": 74,
        "respiratory_rate": 14, "spo2": 99, "temperature_c": 36.8,
        "pain_score": 1, "gcs_total": 15, "consciousness_level": "Alert",
        "chief_complaint": "Prescription Refill", "num_comorbidities": 0,
        "is_immunocompromised": 0, "num_prior_ed_visits_12m": 0,
        "id": 5, "esi_level": 5, "deterioration_risk": "Low", "admission_likelihood": "Low"
    },
]
patient_id_counter = 5


esi_model = joblib.load('esi_level.pkl')
deterioration_model = joblib.load('deterioration_risk.pkl')
admission_model = joblib.load('admission_likelihood.pkl')

app = FastAPI()


@app.get('/')
def greet():
    return "Hello Welcome To The Website :)"

@app.get('/queue')
def queue():
    return patient_queue

@app.get('/queue/{id}')
def queue_with_id(id: int):
    for i in patient_queue:
        if i['id'] == id:
            return i
    else:
        return 'product not found'
    
@app.post('/input')
def input(input: Input_Variables):
    global patient_id_counter

    gender_map = {'Male': 0, "Female": 1, "Other": 2}
    arrival_mode_map = {'Walk-in': 0, 'Ambulance': 1, 'Police': 2, "Transfer": 3}
    consciousness_level_map = {'Alert': 0, 'Unresponsive': 1, 'Pain': 2, 'Voice': 3}
    chief_complaint_map = {'Chest Pain': 0, 'Shortness of Breath': 1, 'Laceration': 2, 'Fever': 3, 'Abdominal Pain': 4, 'Stroke Symptoms': 5, 'Prescription Refill': 6, 'Severe Trauma': 7}

    gender_encoded = gender_map[input.gender]
    arrival_mode_encoded = arrival_mode_map[input.arrival_mode]
    consciousness_level_encoded = consciousness_level_map[input.consciousness_level]
    chief_complaint_encoded = chief_complaint_map[input.chief_complaint]

    df = pd.DataFrame([{
        'age': input.age,
        'gender': gender_encoded,
        'arrival_mode': arrival_mode_encoded,
        'heart_rate': input.heart_rate,
        'systolic_bp': input.systolic_bp,
        'diastolic_bp': input.diastolic_bp,
        'respiratory_rate': input.respiratory_rate,
        'spo2': input.spo2,
        'temperature_c': input.temperature_c,
        'pain_score': input.pain_score,
        'gcs_total': input.gcs_total,
        'consciousness_level': consciousness_level_encoded,
        'chief_complaint': chief_complaint_encoded,
        'num_comorbidities': input.num_comorbidities,
        'is_immunocompromised': input.is_immunocompromised,
        'num_prior_ed_visits_12m': input.num_prior_ed_visits_12m,
    }])

    esi_prediction = esi_model.predict(df)
    deterioration_prediction = deterioration_model.predict(df)
    admission_prediction = admission_model.predict(df)

    probabilities = esi_model.predict_proba(df)[0]
    record = input.model_dump()
    record['id'] = patient_id_counter + 1
    record['esi_level'] = int(esi_prediction[0])
    record['deterioration_risk'] = str(deterioration_prediction[0])
    record['admission_likelihood'] = str(admission_prediction[0])

    patient_queue.append(record)
    patient_id_counter += 1

    return {
        "esi_level": int(esi_prediction[0]),
        "confidence": float(max(probabilities)),
        "deterioration_risk": str(deterioration_prediction[0]),
        "admission_likelihood": str(admission_prediction[0]),
    }