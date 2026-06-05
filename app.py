import io
from typing import List, Tuple

import numpy as np
import streamlit as st
from PIL import Image

MODEL_PATH = "model.pkl"
TARGET_SIZE = (128, 128)


def load_classification_model():
    try:
        from keras.models import load_model
    except ModuleNotFoundError as exc:
        st.error(
            "Missing required package `keras`. Please install the dependencies from `requirements.txt`."
        )
        return None

    try:
        return load_model(MODEL_PATH)
    except Exception as exc:
        st.error(f"Failed to load model from `{MODEL_PATH}`: {exc}")
        return None


@st.cache_resource
def get_model():
    return load_classification_model()


def preprocess_image(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB").resize(TARGET_SIZE)
    array = np.asarray(image, dtype=np.float32) / 255.0
    if array.ndim == 3:
        array = np.expand_dims(array, 0)
    return array


def predict(image: Image.Image, model) -> np.ndarray:
    return model.predict(preprocess_image(image))


def format_predictions(preds: np.ndarray) -> List[Tuple[str, str]]:
    preds = np.asarray(preds)
    if preds.ndim == 1:
        preds = np.expand_dims(preds, 0)

    if preds.shape[-1] == 1:
        return [("Output value", f"{float(preds[0, 0]):.4f}")]

    sorted_indices = np.argsort(preds[0])[::-1]
    labels = [f"Class {idx}" for idx in sorted_indices]
    return [(label, f"{float(preds[0, idx]):.4f}") for label, idx in zip(labels, sorted_indices)]


st.set_page_config(
    page_title="Image Classification",
    page_icon="🖼️",
    layout="centered",
)

st.title("Image Classification Model")
st.write(
    "Upload an image to classify it with the saved model. The app resizes images to 128x128 and normalizes pixel values."
)

model = get_model()
if model is None:
    st.stop()

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file is not None:
    image = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(image, caption="Uploaded image", use_column_width=True)

    if st.button("Classify"):
        with st.spinner("Running model prediction..."):
            try:
                preds = predict(image, model)
            except Exception as exc:
                st.error(f"Prediction failed: {exc}")
            else:
                if preds.size == 0:
                    st.warning("Model did not return a prediction.")
                else:
                    st.subheader("Prediction result")
                    if preds.ndim == 2 and preds.shape[-1] > 1:
                        predicted_idx = int(np.argmax(preds[0]))
                        st.markdown(f"**Predicted class:** Class {predicted_idx}")
                    for label, score in format_predictions(preds)[:5]:
                        st.write(f"- **{label}**: {score}")
else:
    st.info("Upload an image file to get started.")
