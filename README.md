# Guide d'utilisation de l'API de Prédiction du Taux de Congestion

## Installation et Configuration

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. Créer un environnement virtuel :

```bash
python -m venv venv
```

2. Activer l'environnement virtuel :

- Sous Windows :

```bash
venv\Scripts\activate
```

- Sous Linux/MacOS :

```bash
source venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancer l'API :

```bash
uvicorn main:app --reload
```

L'API sera accessible à l'adresse : http://localhost:8000

## Points de terminaison (Endpoints)

### 1. Vérification de l'API

- **URL** : `/`
- **Méthode** : GET
- **Réponse** : Message confirmant que l'API est active

### 2. Prédiction unique

- **URL** : `/predict`
- **Méthode** : POST
- **Format des données d'entrée** :

```json
{
    "commune": "string",
    "meteo": "string",
    "evenement": "string",
    "chantier": "string",
    "type_jour": "string",
    "affluence": integer,
    "heure_num": integer,
    "latitude": float,
    "longitude": float,
    "date_timestamp": integer
}
```

### 3. Prédiction par lots

- **URL** : `/predict_batch`
- **Méthode** : POST
- **Format des données d'entrée** :

```json
{
    "items": [
        {
            "commune": "string",
            "meteo": "string",
            "evenement": "string",
            "chantier": "string",
            "type_jour": "string",
            "affluence": integer,
            "heure_num": integer,
            "latitude": float,
            "longitude": float,
            "date_timestamp": integer
        }
    ]
}
```

## Exemples d'utilisation

### Exemple de requête unique (avec curl)

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
           "commune": "Bordeaux",
           "meteo": "Ensoleillé",
           "evenement": "Aucun",
           "chantier": "Non",
           "type_jour": "Semaine",
           "affluence": 2,
           "heure_num": 14,
           "latitude": 44.837789,
           "longitude": -0.57918,
           "date_timestamp": 1700000000
         }'
```

### Exemple de requête par lots (avec curl)

```bash
curl -X POST "http://localhost:8000/predict_batch" \
     -H "Content-Type: application/json" \
     -d '{
           "items": [
             {
               "commune": "Bordeaux",
               "meteo": "Ensoleillé",
               "evenement": "Aucun",
               "chantier": "Non",
               "type_jour": "Semaine",
               "affluence": 2,
               "heure_num": 14,
               "latitude": 44.837789,
               "longitude": -0.57918,
               "date_timestamp": 1700000000
             }
           ]
         }'
```
