# 🏥 ER Patient Priority Sorter

A machine learning system that predicts **Emergency Severity Index (ESI)**, **deterioration risk**, and **admission likelihood** for ER patients — built end-to-end, from synthetic data generation to a live interactive interface.

> ⚠️ **This is a demonstration project.** It is trained on synthetic data, not real hospital records, and has no human-override mechanism. It is not a clinical tool and should never be used to make real triage decisions.

---

## Table of Contents

- [Overview](#overview)
- [What It Predicts](#what-it-predicts)
- [Live Demo](#live-demo)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Models & Performance](#models--performance)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Known Limitations](#known-limitations)
- [Future Work](#future-work)

---

## Overview

Traditional ER triage relies entirely on manual staff evaluation — judging not just how urgent a patient is, but how they might deteriorate and whether they'll need admission. That judgment gets harder to sustain as patient volume rises and staff fatigue sets in.

This project is a **decision-support layer, not a replacement for clinicians**. It predicts three things at once from a patient's vitals, symptoms, and history, giving staff a fuller picture in a single pass. The model suggests — the clinician always decides.

## What It Predicts

| Prediction | Scale | What it means |
|---|---|---|
| **ESI Level** | `1`–`5` | Emergency Severity Index — from immediate resuscitation (1) to non-urgent (5) |
| **Deterioration Risk** | `Low` / `Medium` / `High` | How likely the patient's condition is to worsen while waiting |
| **Admission Likelihood** | `Low` / `Moderate` / `High` | How likely the patient is to be admitted vs. discharged same-day |

## Live Demo

- **Frontend:** _[add your deployed Streamlit URL here]_
- **API:** _[add your deployed FastAPI URL here]_

## Architecture

```
┌─────────────────┐        ┌──────────────────┐        ┌─────────────────┐
│   Streamlit      │──POST─▶│   FastAPI          │──────▶│  3× RandomForest │
│   Frontend        │◀──────│   Backend           │◀──────│  (.pkl models)   │
│   (2 pages)        │  JSON │   /input · /queue    │       └─────────────────┘
└─────────────────┘        └──────────────────┘
```

- **Frontend** — two-page Streamlit app: a landing page explaining the project with live example predictions, and a "Try It Yourself" page with a full intake form (16 fields) and one-click preset scenarios.
- **Backend** — FastAPI server that validates incoming patient data, runs it through all three trained models, and returns predictions. Also maintains a live, sortable in-memory patient queue.
- **Models** — three independently trained `RandomForestClassifier` models, sharing the same 16 input features.

## Dataset

- **5,000 synthetic patient records**, generated with clinically-grounded logic (not random noise)
- Hard clinical rules enforced during generation — e.g. GCS < 8 or unresponsive → always ESI 1
- Realistic class imbalance across all three targets, mirroring real-world ER distributions
- Light, intentional label noise to simulate genuine real-world disagreement (not perfect, not random either)
- 16 input features: demographics, vital signs, clinical assessment, and patient history

<details>
<summary><strong>Full feature list</strong></summary>

| Category | Features |
|---|---|
| Demographics | `age`, `gender`, `arrival_mode` |
| Vitals | `heart_rate`, `systolic_bp`, `diastolic_bp`, `respiratory_rate`, `spo2`, `temperature_c` |
| Clinical Assessment | `pain_score`, `gcs_total`, `consciousness_level`, `chief_complaint` |
| History | `num_comorbidities`, `is_immunocompromised`, `num_prior_ed_visits_12m` |

</details>

## Models & Performance

Three separate `RandomForestClassifier` models, trained with `class_weight='balanced'` to handle class imbalance, each evaluated on a held-out 20% test split.

| Model | Accuracy | Balanced Accuracy |
|---|:---:|:---:|
| ESI Level | **90%** | 92% |
| Deterioration Risk | **83%** | 83% |
| Admission Likelihood | **85%** | 79% |

**ESI recall on the critical classes:**

| Class | Recall |
|---|:---:|
| ESI 1 (Immediate) | 98% |
| ESI 2 (Emergent) | 91% |

> Recall on the most critical classes was the priority metric — in triage, missing a real emergency is a far worse outcome than over-flagging a stable patient.

## Tech Stack

- **Language:** Python
- **ML:** scikit-learn (`RandomForestClassifier`), pandas, numpy, joblib
- **Backend:** FastAPI, Pydantic, uvicorn
- **Frontend:** Streamlit
- **Data generation:** custom rule-based synthetic data generator

## Getting Started

### Prerequisites

```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib streamlit requests
```

### Run the backend

```bash
cd Model_Training
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000` — interactive docs at `http://127.0.0.1:8000/docs`.

### Run the frontend

```bash
cd Frontend
streamlit run app.py
```

> Both the backend and frontend need to be running simultaneously — the frontend calls the backend over HTTP.

## API Reference

### `POST /input`

Submit a patient and receive predictions.

**Request body:**
```json
{
  "age": 68,
  "gender": "Male",
  "arrival_mode": "Ambulance",
  "heart_rate": 145,
  "systolic_bp": 78,
  "diastolic_bp": 48,
  "respiratory_rate": 32,
  "spo2": 84.0,
  "temperature_c": 38.9,
  "pain_score": 9,
  "gcs_total": 9,
  "consciousness_level": "Pain",
  "chief_complaint": "Severe Trauma",
  "num_comorbidities": 3,
  "is_immunocompromised": 0,
  "num_prior_ed_visits_12m": 2
}
```

**Response:**
```json
{
  "esi_level": 1,
  "confidence": 0.97,
  "deterioration_risk": "High",
  "admission_likelihood": "High"
}
```

### `GET /queue`

Returns the current patient queue, sorted by urgency.

## Project Structure

```
Patient-ER-Status/
├── Model_Training/
│   ├── main.py              # FastAPI app
│   ├── data_model.py        # Pydantic input schema
│   ├── esi_model.pkl
│   ├── deterioration_model.pkl
│   └── admission_model.pkl
├── Frontend/
│   ├── app.py                # Router / navigation entry point
│   ├── intro.py               # Landing page
│   ├── test.py                 # "Try It Yourself" page
│   └── .streamlit/
│       └── config.toml         # Theme
└── er_triage_v3.csv          # Synthetic dataset
```

## Known Limitations

- [ ] Trained on **synthetic data**, not real hospital records — not clinically validated
- [ ] **No human-override mechanism** yet — a real deployment would need one before any prediction could be acted on directly
- [ ] Patient queue is **in-memory only** — resets on server restart
- [ ] Deterioration risk and admission likelihood labels were generated using rule-based clinical logic (e.g. a qSOFA-style scoring approach), not from real outcome data

## Future Work

- [ ] Human-in-the-loop review step for low-confidence predictions
- [ ] Persistent storage (database) for the patient queue
- [ ] Department/specialty routing based on chief complaint
- [ ] Real-world validation against actual triage outcomes

---

<p align="center">Built end-to-end — dataset, models, API, and interface, all from scratch.</p>
