# Image Classification Streamlit App

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

## Mask Detection Webpage Demo

A new static demo page is included for the mask detection UI:

- `index.html` — demo page with webcam capture and mask check UI.
- `styles.css` — interface styling.
- `script.js` — webcam controls and placeholder analysis logic.
- `requirements.md` — requirements and usage details for the demo.

Open `index.html` in a modern browser, allow camera access, capture a photo, and click `Check Mask`.
