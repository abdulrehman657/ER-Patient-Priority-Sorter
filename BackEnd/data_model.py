from typing import Literal
from pydantic import BaseModel,Field

class Input_Variables(BaseModel):
    age : int = Field(ge=1, le=95)
    gender : Literal['Male', 'Female', 'Other']
    arrival_mode : Literal['Walk-in','Ambulance','Police','Transfer']
    heart_rate : int = Field(ge=30,le=180)
    systolic_bp : int = Field(ge=60,le=220) 
    diastolic_bp : int = Field(ge=40,le=130)
    respiratory_rate : int = Field(ge=8,le=40)
    spo2 : float = Field(ge=70.0,le =100.0) 
    temperature_c : float = Field(ge=34.0,le=40.5) 
    pain_score : int = Field(ge=0,le=10)
    gcs_total : int = Field(ge=3,le=15)
    consciousness_level : Literal['Alert','Unresponsive','Pain','Voice']
    chief_complaint : Literal['Chest Pain','Shortness of Breath','Laceration','Fever','Abdominal Pain','Stroke Symptoms','Prescription Refill','Severe Trauma']
    num_comorbidities : int = Field(ge=0,le=5)
    is_immunocompromised : int = Field(ge=0,le=1) 
    num_prior_ed_visits_12m : int = Field(ge=0,le=10)