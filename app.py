
import tensorflow as tf
import numpy as np
from PIL import Image

# ==========================================
# PAGE CONFIG
# ==========================================


import streamlit as st
import pickle

st.write("App Started")

try:
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)

    st.success("Model Loaded Successfully")

except Exception as e:
    st.error(f"Model Loading Error: {e}")
    st.stop()


st.set_page_config(
    page_title="Face Mask Detection",
    page_icon="😷",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main{
    background-color:#0E1117;
}

.title{
    text-align:center;
    font-size:3rem;
    font-weight:700;
    color:white;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:20px;
}

[data-testid="stCameraInput"]{
    max-width:450px;
    margin:auto;
}

[data-testid="stImage"] img{
    border-radius:15px;
}

.result-success{
    background:#198754;
    padding:15px;
    border-radius:10px;
    color:white;
    text-align:center;
}

.result-danger{
    background:#dc3545;
    padding:15px;
    border-radius:10px;
    color:white;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL
# ==========================================

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

# ==========================================
# SETTINGS
# ==========================================

IMG_SIZE = 128  # CHANGE IF NEEDED

# ==========================================
# PREPROCESS
# ==========================================

def preprocess_image(image):

    image = image.convert("RGB")

    image = image.resize((IMG_SIZE, IMG_SIZE))

    image = np.array(image)

    image = image.astype("float32") / 255.0

    image = np.expand_dims(image, axis=0)

    return image

# ==========================================
# PREDICT
# ==========================================

def predict_mask(image):

    processed = preprocess_image(image)

    prediction = model.predict(processed, verbose=0)

    # For debugging
    st.write("Prediction:", prediction)

    if prediction.shape[-1] == 1:

        score = float(prediction[0][0])

        if score > 0.5:
            label = "Mask"
            confidence = score
        else:
            label = "No Mask"
            confidence = 1 - score

    else:

        pred_class = np.argmax(prediction)

        confidence = float(np.max(prediction))

        # CHANGE THESE IF REVERSED
        if pred_class == 0:
            label = "Mask"
        else:
            label = "No Mask"

    return label, confidence

# ==========================================
# HEADER
# ==========================================

st.markdown(
    "<div class='title'>😷 Face Mask Detection</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Upload an image or capture one using your webcam</div>",
    unsafe_allow_html=True
)

# ==========================================
# TABS
# ==========================================

tab1, tab2 = st.tabs(
    ["📁 Upload Image", "📷 Webcam"]
)

# ==========================================
# IMAGE UPLOAD
# ==========================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                image,
                caption="Uploaded Image",
                use_container_width=True
            )

        with col2:

            if st.button("Predict"):

                label, confidence = predict_mask(image)

                if label == "Mask":

                    st.markdown(
                        f"""
                        <div class='result-success'>
                        <h2>✅ MASK DETECTED</h2>
                        <h3>{confidence:.2%}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        f"""
                        <div class='result-danger'>
                        <h2>❌ NO MASK DETECTED</h2>
                        <h3>{confidence:.2%}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# ==========================================
# WEBCAM
# ==========================================

with tab2:

    st.markdown(
        "<h4 style='text-align:center;'>Capture Face</h4>",
        unsafe_allow_html=True
    )

    camera_image = st.camera_input("")

    if camera_image:

        image = Image.open(camera_image)

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                image,
                caption="Captured Image",
                use_container_width=True
            )

        with col2:

            label, confidence = predict_mask(image)

            if label == "Mask":

                st.markdown(
                    f"""
                    <div class='result-success'>
                    <h2>✅ MASK DETECTED</h2>
                    <h3>{confidence:.2%}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class='result-danger'>
                    <h2>❌ NO MASK DETECTED</h2>
                    <h3>{confidence:.2%}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
    """
    <center>
    Built with ❤️ using Streamlit & TensorFlow
    </center>
    """,
    unsafe_allow_html=True
)