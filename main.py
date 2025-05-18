from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd

model = joblib.load("model/model.joblib")
colonnes_attendues = joblib.load("model/columns.joblib")

class InputData(BaseModel):
    commune: str
    meteo: str
    evenement: str
    chantier: str
    type_jour: str
    affluence: int
    heure_num: int
    latitude: float
    longitude: float
    date_timestamp: int

class BatchInputData(BaseModel):
    items: List[InputData]

app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def root():
    return {"message": "API de prédiction de congestion active."}

@app.post("/predict")
def predict(data: InputData):
    input_df = pd.DataFrame([data.dict()])
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=colonnes_attendues, fill_value=0)
    prediction = model.predict(input_encoded)[0]
    return {"taux_congestion": float(prediction)}

@app.post("/predict_batch")
def predict_batch(data: BatchInputData):
    if not data.items:
        return {"taux_congestions": []}
    input_dfs = [pd.DataFrame([item.dict()]) for item in data.items]
    input_df = pd.concat(input_dfs, ignore_index=True)
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=colonnes_attendues, fill_value=0)
    predictions = model.predict(input_encoded)
    return {"taux_congestions": [float(pred) for pred in predictions]}
