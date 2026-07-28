import pickle
import sys
import warnings
from pathlib import Path
from sklearn.exceptions import InconsistentVersionWarning

MODEL_FILE = "model.save"
SCALER_FILE = "scaler.save"
GENDER_ENCODER_FILE = "gender.save"
SMOKING_ENCODER_FILE = "smoking.save"

SAMPLE_INPUTS = [
    {
        "label": "Low-risk healthy adult",
        "gender": "Female",
        "age": 28,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 22.0,
        "hba1c": 5.2,
        "blood_glucose": 90.0,
    },
    {
        "label": "Higher-risk senior",
        "gender": "Male",
        "age": 65,
        "hypertension": 1,
        "heart_disease": 1,
        "smoking_history": "ever",
        "bmi": 31.0,
        "hba1c": 8.1,
        "blood_glucose": 185.0,
    },
    {
        "label": "Borderline metabolic risk",
        "gender": "Female",
        "age": 52,
        "hypertension": 1,
        "heart_disease": 0,
        "smoking_history": "former",
        "bmi": 28.5,
        "hba1c": 6.7,
        "blood_glucose": 140.0,
    },
]


def ensure_legacy_sklearn_loss_module() -> None:
    if "_loss" not in sys.modules:
        try:
            import sklearn._loss._loss as loss_mod  # type: ignore
            sys.modules["_loss"] = loss_mod
        except Exception:
            pass


def load_pickle(path: str):
    ensure_legacy_sklearn_loss_module()
    with open(path, "rb") as f:
        return pickle.load(f)


def main() -> None:
    # suppress harmless sklearn warnings during scripted tests
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
    warnings.filterwarnings("ignore", message="X does not have valid feature names")
    if not Path(MODEL_FILE).exists():
        raise FileNotFoundError(MODEL_FILE)
    if not Path(SCALER_FILE).exists():
        raise FileNotFoundError(SCALER_FILE)
    if not Path(GENDER_ENCODER_FILE).exists():
        raise FileNotFoundError(GENDER_ENCODER_FILE)
    if not Path(SMOKING_ENCODER_FILE).exists():
        raise FileNotFoundError(SMOKING_ENCODER_FILE)

    model = load_pickle(MODEL_FILE)
    scaler = load_pickle(SCALER_FILE)
    gender_encoder = load_pickle(GENDER_ENCODER_FILE)
    smoking_encoder = load_pickle(SMOKING_ENCODER_FILE)

    for case in SAMPLE_INPUTS:
        gender = gender_encoder.transform([case["gender"]])[0]
        smoking = smoking_encoder.transform([case["smoking_history"]])[0]
        features = [
            gender,
            case["age"],
            case["hypertension"],
            case["heart_disease"],
            smoking,
            case["bmi"],
            case["hba1c"],
            case["blood_glucose"],
        ]
        scaled = scaler.transform([features])
        pred = model.predict(scaled)[0]
        print(f"{case['label']}: prediction={pred}")


if __name__ == "__main__":
    main()
