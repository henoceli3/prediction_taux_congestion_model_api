from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import joblib
import pandas as pd

model = joblib.load("model/model.joblib")
colonnes_attendues = joblib.load("model/columns.joblib")

class InputData(BaseModel):
    heure: int
    jour_semaine: str
    type_jour: str
    meteo: str
    evenement: str
    nb_voitures: int
    commune: str
    latitude: float
    longitude: float

class BatchInputData(BaseModel):
    items: List[InputData]

app = FastAPI()

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
    input_dfs = [pd.DataFrame([item.dict()]) for item in data.items]
    input_df = pd.concat(input_dfs, ignore_index=True)
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=colonnes_attendues, fill_value=0)
    predictions = model.predict(input_encoded)
    return {"taux_congestions": [float(pred) for pred in predictions]}
