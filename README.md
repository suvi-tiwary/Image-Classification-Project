# Mak Detection system 

This workspace contains a simple Streamlit web app for image classification.

Files added:

- `app.py`: Streamlit application entry point.
- `model.py`: ModelWrapper class to load a Keras model or use MobileNetV2 fallback.
- `utils.py`: Image preprocessing helpers.

Quick start:

1. Create and activate a Python virtualenv (optional but recommended).

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run "app.py"
```

Usage notes:
- You can upload a Keras model file (.h5). If none is provided the app uses MobileNetV2 pretrained on ImageNet.
- Optionally upload a labels file (one class name per line) to map prediction indices to names.

## Streamlit Mask Detection App

A Streamlit demo app is now available for live webcam mask detection.

- `app.py` — Streamlit application entry point.
- `requirements.txt` — Python dependencies.
- `requirements.md` — app requirements and usage information.

### Run locally

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app:

```powershell
streamlit run app.py
```

Then open the local URL shown by Streamlit in your browser.

### Notes

- The app uses `st.camera_input` for webcam capture.
- This demo currently uses a simple brightness-based heuristic to decide mask status.
- Replace the analysis code in `app.py` with a trained mask detection model for better accuracy.
