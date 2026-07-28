# Diabetes Predictor Streamlit App

## Overview
This project is a local Streamlit app that predicts diabetes risk using a pre-trained machine learning model and saved encoders.

## Files
- `model.py` - Streamlit application.
- `model.save` - Saved classifier model.
- `scaler.save` - Saved feature scaler.
- `gender.save` - Saved gender encoder.
- `smoking.save` - Saved smoking history encoder.
- `diabetes.jfif` - Optional illustration image.
- `requirements.txt` - Python dependencies.

## Setup
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run model.py
   ```

## Testing
- Run the sample prediction script to validate model/scaler/encoders:

```bash
python sample_test.py
```

## Notes on compatibility
- The model artifacts were trained and pickled with scikit-learn 1.8.x; they will load in newer scikit-learn versions but may show `InconsistentVersionWarning` about estimator versions. The app suppresses these harmless warnings for a cleaner UI.
- If you prefer exact reproducibility, create a virtual environment and install `scikit-learn==1.8.0`.

## Project Summary

This repository contains a Streamlit web app (`model.py`) that loads pre-saved ML artifacts and returns a simple binary diabetes risk prediction. The artifacts were generated from an exploratory notebook (`Untitled20.ipynb`) where data preprocessing, encoding, scaling, and model training were done. The saved artifacts are:

- `model.save`  — trained classifier (GradientBoostingClassifier)
- `scaler.save` — fitted `MinMaxScaler`
- `gender.save` — fitted `LabelEncoder` for `gender`
- `smoking.save` — fitted `LabelEncoder` for `smoking_history`

The app implements several hardening features:

- A small compatibility shim that injects the legacy sklearn `_loss` module when loading older pickles (fixes ModuleNotFoundError). 
- Input validation for numeric fields (age, BMI, HbA1c, blood glucose).
- Suppression of harmless sklearn warnings (`InconsistentVersionWarning` and feature-name warnings) to avoid confusing end users.
- Safe transform/predict helpers that try to use feature names when available to reduce validation warnings.

## Tech Stack

- Python 3.11+ (tested on Python 3.13 in this environment)
- Streamlit — UI and app hosting
- scikit-learn — model and preprocessing (GradientBoostingClassifier, LabelEncoder, MinMaxScaler)
- XGBoost — available in the training notebook if used
- pandas / numpy — data manipulation
- Pillow — image handling for the app icon

Dependencies are pinned in `requirements.txt` for reproducible installs.

## How the artifacts were created (summary)

1. Data was loaded and cleaned in `Untitled20.ipynb` (imputation, outlier handling, encoding).
2. Categorical labels (`gender`, `smoking_history`) were encoded with `LabelEncoder` and saved.
3. Numerical features were scaled with `MinMaxScaler` and saved.
4. A tree-based model (GradientBoostingClassifier) was trained and saved as `model.save`.
5. The notebook contains the `pickle.dump(...)` calls that produced the `.save` files.

## Running and testing locally

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows PowerShell: .venv\Scripts\Activate.ps1
```

2. Install pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Start the Streamlit app:

```bash
streamlit run model.py
```

4. Optionally run the sample test script to validate predictions without the UI:

```bash
python sample_test.py
```

## Security and reproducibility notes

- Pickle files are Python-specific and can execute arbitrary code if tampered with — only load artifacts you trust.
- If you need exact matching of training/runtime behavior, pin `scikit-learn==1.8.0` (the training environment) in a `requirements.txt` or in a container image.

## Troubleshooting

- `ModuleNotFoundError: No module named '_loss'`: fixed by the compatibility shim; ensure scikit-learn is installed.
- `InconsistentVersionWarning`: benign when loading older pickles into newer scikit-learn versions; consider matching scikit-learn versions to remove the warning.
- If predictions fail with feature-name validation warnings, the app attempts a fallback to array-based `transform`/`predict`.

## Next steps and suggestions

- Add a `Dockerfile` for reproducible deployment.
- Add CI that runs `sample_test.py` and starts the Streamlit app for smoke tests.
- Retrain and re-save model artifacts using the exact scikit-learn version you will use in production to avoid compatibility layers.

## Contact / Credits

This project scaffolds a simple demonstration app for local diabetes risk estimation. Use responsibly and consult clinical experts before relying on the output.

## Notes
- Keep the saved model files in the same folder as `model.py`.
- The app is for informational purposes and not a medical diagnosis.
