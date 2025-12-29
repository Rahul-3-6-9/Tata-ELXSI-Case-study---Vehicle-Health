# Vehicle Health & Diagnostics System

### Case Study 2 — Automotive / Software Defined Vehicle (SDV)

---

## Overview

This project implements a **Vehicle Health & Diagnostics system** for a Software Defined Vehicle (SDV), focusing on **battery health monitoring**.

The solution demonstrates **responsible use of Generative AI during development**, combined with **deterministic, explainable runtime behavior** using traditional Machine Learning and rule-based logic—aligned with automotive safety expectations.

---

## Objectives

* Predict battery health using ML
* Classify diagnostic risk deterministically
* Ensure explainability and safety
* Demonstrate GenAI-assisted **development**, not runtime decision-making
* Follow Service-Oriented Architecture (SoA) principles suitable for SDVs

---

## System Architecture (High Level)

```
Offline (Development Time)
 ├── GenAI
 │    ├── Requirement structuring
 │    ├── Service design suggestions
 │    ├── Rule ideation
 │    ├── Test case generation
 │    └── Documentation support
 │
 └── ML Training (model.py)
      └── battery_model.pkl

Runtime (Deterministic)
 ┌───────────────────────────┐
 │ FastAPI Backend            │
 │  └── BatteryHealthService  │
 │       ├── Input validation │
 │       ├── ML inference     │
 │       ├── Rule evaluation  │
 │       ├── Explainability   │
 │       └── Confidence score │
 └─────────────▲─────────────┘
               │
        Streamlit Dashboard
```

> **Important:** GenAI is **not used at runtime**. All runtime behavior is deterministic and auditable.

---

## Role of GenAI

GenAI is used strictly as a **development-time co-engineer**, not as a runtime component.

### GenAI is used for:

* Structuring system and functional requirements
* Designing service boundaries and APIs
* Suggesting candidate diagnostic rules
* Generating unit test scenarios
* Assisting documentation and explanations

### GenAI is **not** used for:

* Runtime prediction
* Safety decisions
* Model training
* Vehicle execution logic

This mirrors real-world automotive constraints.

---

## Machine Learning Design

* **Model:** RandomForestRegressor
* **Training:** Offline only (`model.py`)
* **Data:** Physics-inspired synthetic battery data
* **Inference:** Runtime prediction of battery health score (0–100)

ML is used **only for continuous estimation**, never for final safety decisions.

---

## Rule-Based Diagnostics

Deterministic rules guard and override ML outputs:

| Condition            | Risk Level |
| -------------------- | ---------- |
| Temperature > 60°C   | HIGH       |
| Charge cycles > 4500 | HIGH       |
| Charge cycles > 3000 | MEDIUM     |
| Health score < 60    | MEDIUM     |
| Otherwise            | LOW        |

Each rule produces a **human-readable explanation**.

---

## Project Structure

```
TATA_ELXSI_CS2/
├── api/
│   └── main.py                         # FastAPI entry point
├── services/
│   ├── battery_health_service.py       # ML + rules + explainability
│   └── __init__.py
├── models/
│   └── train_model.py                  # Offline ML training
├── data/
│   ├── battery_data_generator.py
│   └── battery_data.csv                # Synthetic dataset
├── frontend/
│   └── dashboard.py                    # Streamlit dashboard
├── tests/
│   └── test_battery_health.py          # Unit tests
├── requirements.txt
└── README.md
```

---

## API Contract

### Endpoint

```
POST /battery/health
```

### Input

```json
{
  "soc": 55.0,
  "temperature": 45.0,
  "charge_cycles": 1200
}
```

### Output

```json
{
  "health_score": 58.2,
  "risk_level": "MEDIUM",
  "confidence": 0.73,
  "explanation": "Advanced battery aging detected (1200 charge cycles)"
}
```

---

## Testing Strategy

* Unit tests validate:

  * Normal operation
  * Safety overrides
  * Boundary conditions
  * Invalid input handling
* Tests enforce **conservative diagnostic behavior**
* All tests pass successfully (`pytest`)

---

## Dashboard

* Built using **Streamlit**
* Enables interactive testing of:

  * SoC
  * Temperature
  * Charge cycles
* Visual confirmation of:

  * Health score changes
  * Risk classification
  * Rule explanations

The dashboard is a **development & demo tool**, not an in-vehicle HMI.

---

## Installation & Run Instructions

### 1️⃣ Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Train ML model

```bash
python models/model.py
```

### 4️⃣ Start backend API

```bash
uvicorn api.main:app --reload
```

### 5️⃣ Run dashboard

```bash
streamlit run frontend/dashboard.py
```

