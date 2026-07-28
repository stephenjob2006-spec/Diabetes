import os
import pickle
import sys
import warnings
import logging
from typing import Any

import streamlit as st
from PIL import Image
from sklearn.exceptions import InconsistentVersionWarning
import pandas as pd
import numpy as np

MODEL_FILE = "model.save"
SCALER_FILE = "scaler.save"
GENDER_ENCODER_FILE = "gender.save"
SMOKING_ENCODER_FILE = "smoking.save"
APP_IMAGE_FILE = "diabetes.jfif"

SMOKING_HISTORY_OPTIONS = [
    "never",
    "no info",
    "current",
    "former",
    "ever",
    "not current",
]


def ensure_legacy_sklearn_loss_module() -> None:
    """Inject compatibility module for pickled legacy sklearn estimators."""
    if "_loss" not in sys.modules:
        try:
            import sklearn._loss._loss as loss_mod  # type: ignore
            sys.modules["_loss"] = loss_mod
        except Exception:
            pass


def load_pickle(path: str) -> Any:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found: {path}")
    ensure_legacy_sklearn_loss_module()
    with open(path, "rb") as file:
        return pickle.load(file)


@st.cache_resource
def load_model_resources() -> tuple[Any, Any, Any, Any]:
    model = load_pickle(MODEL_FILE)
    scaler = load_pickle(SCALER_FILE)
    gender_encoder = load_pickle(GENDER_ENCODER_FILE)
    smoking_encoder = load_pickle(SMOKING_ENCODER_FILE)
    return model, scaler, gender_encoder, smoking_encoder


def load_app_image():
    if not os.path.exists(APP_IMAGE_FILE):
        return None

    try:
        return Image.open(APP_IMAGE_FILE)
    except Exception:
        return None


def encode_label(encoder: Any, value: str, label_name: str) -> int:
    if not hasattr(encoder, "classes_"):
        raise ValueError(f"Invalid encoder for {label_name}")
    if value not in encoder.classes_:
        raise ValueError(
            f"Unknown {label_name} value '{value}'. Allowed values: {', '.join(map(str, encoder.classes_))}"
        )
    return int(encoder.transform([value])[0])


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


def validate_inputs(
    age: int,
    bmi: float,
    hba1c: float,
    blood_glucose: float,
) -> None:
    if not 0 <= age <= 120:
        raise ValueError("Age must be between 0 and 120.")
    if not 0.0 <= bmi <= 100.0:
        raise ValueError("BMI must be between 0.0 and 100.0.")
    if not 0.0 <= hba1c <= 15.0:
        raise ValueError("HbA1c must be between 0.0 and 15.0.")
    if not 0.0 <= blood_glucose <= 500.0:
        raise ValueError("Blood glucose must be between 0.0 and 500.0.")


def build_feature_vector(
    gender: str,
    age: int,
    hypertension: int,
    heart_disease: int,
    smoking_history: str,
    bmi: float,
    hba1c: float,
    blood_glucose: float,
    gender_encoder: Any,
    smoking_encoder: Any,
) -> list[float]:
    validate_inputs(age, bmi, hba1c, blood_glucose)
    return [
        encode_label(gender_encoder, gender, "gender"),
        int(age),
        int(hypertension),
        int(heart_disease),
        encode_label(smoking_encoder, smoking_history, "smoking history"),
        float(bmi),
        float(hba1c),
        float(blood_glucose),
    ]


def app_styles() -> str:
    return """
    <style>
    .stApp { background: #f0f6ff; }
    .block-container { padding: 32px 40px; background: #ffffff; border-radius: 20px; }
    .form-section { background: #f7fbff; border-radius: 18px; padding: 24px; box-shadow: 0 16px 40px rgba(0, 0, 0, 0.05); }
    .stButton > button { border-radius: 14px !important; }
    .hero-title { font-size: 42px !important; color: #003e6b !important; }
    .hero-subtitle { font-size: 18px !important; color: #264653 !important; }
    </style>
    """


def render_app() -> None:
    # suppress known sklearn harmless warnings that confuse users
    warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
    warnings.filterwarnings("ignore", message="X does not have valid feature names")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    st.set_page_config(page_title="Diabetes Predictor", page_icon="🩺", layout="wide")
    st.markdown(app_styles(), unsafe_allow_html=True)

    st.markdown(
        """
        <div style='padding: 48px 32px; background: linear-gradient(135deg, #0077b6 0%, #00b4d8 100%); border-radius: 24px; color: white; text-align: center;'>
            <h1 class='hero-title'>Diabetes Risk Predictor</h1>
            <p class='hero-subtitle'>Enter your medical and lifestyle information for a quick local diabetes risk estimate.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")

    app_image = load_app_image()
    if app_image is not None:
        st.sidebar.image(app_image, caption="Diabetes risk assessment", width=300)

    try:
        model, scaler, gender_encoder, smoking_encoder = load_model_resources()
    except FileNotFoundError as exc:
        st.error(str(exc))
        st.warning("Ensure model.save, scaler.save, gender.save, and smoking.save are present in the app folder.")
        return
    except Exception as exc:
        st.error("Unable to load model resources.")
        st.write(exc)
        return

    left, right = st.columns([3, 2])

    with left:
        st.markdown("<div class='form-section'>", unsafe_allow_html=True)
        st.subheader("👤 Personal Information")
        gender = st.radio("Gender", ["Female", "Male"], horizontal=True)
        age = st.slider("Age", min_value=0, max_value=100, value=30)

        st.subheader("❤️ Medical Conditions")
        hypertension = st.radio("Hypertension", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes", horizontal=True)
        heart_disease = st.radio("Heart disease", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes", horizontal=True)

        st.subheader("🚬 Smoking History")
        smoking_history = st.selectbox("Smoking history", SMOKING_HISTORY_OPTIONS)

        st.subheader("🔬 Health Metrics")
        bmi = st.number_input("Body Mass Index (BMI)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
        hba1c = st.number_input("HbA1c level", min_value=0.0, max_value=15.0, value=5.5, step=0.1)
        blood_glucose = st.number_input("Blood glucose level", min_value=0.0, max_value=500.0, value=100.0, step=1.0)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='form-section'>", unsafe_allow_html=True)
        st.subheader("How it works")
        st.write(
            "The app loads a pre-trained model and transformer from local files, so no data is sent externally. "
            "It then uses your inputs to estimate the diabetes risk." 
        )
        st.info("Required files: model.save, scaler.save, gender.save, smoking.save")
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Sample scenarios")
        sample_table = [
            {
                "Case": case["label"],
                "Gender": case["gender"],
                "Age": case["age"],
                "Smoker": case["smoking_history"],
                "BMI": case["bmi"],
                "HbA1c": case["hba1c"],
                "Glucose": case["blood_glucose"],
            }
            for case in SAMPLE_INPUTS
        ]
        st.table(sample_table)
        if app_image is not None:
            st.image(app_image, width=300)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🏥 Get Prediction", use_container_width=True):
        try:
            features = build_feature_vector(
                gender,
                age,
                hypertension,
                heart_disease,
                smoking_history,
                bmi,
                hba1c,
                blood_glucose,
                gender_encoder,
                smoking_encoder,
            )
            # Try to transform using feature names when available to avoid warnings
            def safe_transform(scaler, features_list):
                try:
                    if hasattr(scaler, "feature_names_in_"):
                        cols = list(getattr(scaler, "feature_names_in_"))
                        df = pd.DataFrame([features_list], columns=cols)
                        return scaler.transform(df)
                except Exception:
                    logger.exception("feature-name transform failed, falling back to array")
                return scaler.transform([features_list])

            def safe_predict(model, X):
                try:
                    # if model was trained with feature names, providing DataFrame helps
                    if isinstance(X, (pd.DataFrame,)):
                        return model.predict(X)[0]
                except Exception:
                    logger.exception("DataFrame predict failed, falling back to array")
                return model.predict(X)[0]

            scaled = safe_transform(scaler, features)
            prediction = safe_predict(model, scaled)

            if prediction == 1:
                st.error("⚠️ High diabetes risk detected. Please consult a healthcare professional.")
            else:
                st.success("✅ Low diabetes risk detected. Keep up a healthy lifestyle.")

            st.write("---")
            st.subheader("Health recommendation")
            st.write(
                "This prediction is for informational purposes only. Maintain a balanced diet, stay active, and consult your doctor for medical advice."
            )
        except ValueError as exc:
            st.error(str(exc))
        except Exception as exc:
            st.error("Prediction failed. Please verify your inputs and try again.")
            st.write(exc)


if __name__ == "__main__":
    render_app()
