import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import cv2
import io
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Image Classification",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🖼️ Image Classification Tool")
st.markdown("""
    Upload an image to classify whether it contains a **mask** or **no mask**.
    The model will analyze your image and provide confidence scores.
""")

# Sidebar
st.sidebar.header("⚙️ Settings")
confidence_threshold = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.05
)

model_type = st.sidebar.selectbox(
    "Model Type",
    ["MobileNetV2 Transfer Learning", "Custom CNN"]
)

# Helper functions
@st.cache_resource
def load_model():
    """Load or create the image classification model"""
    model_path = "image_classification_model.h5"
    
    try:
        # Try to load existing model
        model = keras.models.load_model(model_path)
        return model, True
    except:
        # Create a simple model for demonstration
        model = keras.Sequential([
            keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.MaxPooling2D((2, 2)),
            keras.layers.Conv2D(64, (3, 3), activation='relu'),
            keras.layers.Flatten(),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(1, activation='sigmoid')
        ])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model, False

def preprocess_image(image):
    """Preprocess image for model prediction"""
    # Resize to 128x128
    img = image.resize((128, 128))
    img = img.convert('RGB')
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def make_prediction(model, image_array):
    """Make prediction on image"""
    prediction = model.predict(image_array, verbose=0)
    confidence = float(prediction[0][0])
    return confidence

# Main content area
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📤 Upload Image")
    
    # Upload option
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png", "bmp", "webp"]
    )
    
    # Or capture with camera
    camera_image = st.camera_input("Or take a photo")
    
    # Determine which image to process
    image_to_process = None
    image_source = None
    
    if camera_image is not None:
        image_to_process = Image.open(camera_image)
        image_source = "camera"
    elif uploaded_file is not None:
        image_to_process = Image.open(uploaded_file)
        image_source = "upload"
    
    if image_to_process:
        st.image(image_to_process, caption="Input Image", use_container_width=True)

with col2:
    st.subheader("📊 Prediction Result")
    
    if image_to_process:
        with st.spinner("🔄 Analyzing image..."):
            # Load model
            model, model_loaded = load_model()
            
            # Preprocess
            processed_image = preprocess_image(image_to_process)
            
            # Make prediction
            confidence = make_prediction(model, processed_image)
            
            # Determine class
            is_mask = confidence > 0.5
            class_name = "With Mask" if is_mask else "Without Mask"
            confidence_percentage = confidence * 100 if is_mask else (1 - confidence) * 100
        
        # Display results
        st.success("✅ Analysis Complete!")
        
        # Main prediction
        col_pred1, col_pred2 = st.columns([1, 1])
        with col_pred1:
            st.metric(
                label="Classification",
                value=class_name,
                delta="✓ High Confidence" if confidence_percentage > confidence_threshold * 100 else "⚠ Low Confidence"
            )
        with col_pred2:
            st.metric(
                label="Confidence Score",
                value=f"{confidence_percentage:.1f}%"
            )
        
        # Detailed breakdown
        st.divider()
        st.write("**Detailed Predictions:**")
        
        col_with, col_without = st.columns(2)
        with col_with:
            st.write("🔵 With Mask")
            st.progress(confidence)
            st.text(f"{confidence*100:.2f}%")
        
        with col_without:
            st.write("🔴 Without Mask")
            st.progress(1 - confidence)
            st.text(f"{(1-confidence)*100:.2f}%")
        
        # Warning if below threshold
        if confidence_percentage < confidence_threshold * 100:
            st.warning(f"⚠️ Confidence is below threshold ({confidence_threshold*100:.0f}%)")
        
        # Model info
        if not model_loaded:
            st.info("ℹ️ Using demo model. Train and save your model as 'image_classification_model.h5' for better results.")
    else:
        st.info("👆 Upload or capture an image to get started")

# Footer
st.divider()
st.markdown("""
    ---
    **How to use:**
    1. Upload an image or take a photo
    2. The model will classify if it contains a mask or not
    3. Adjust the confidence threshold in settings for stricter/lenient classification
    
    **Model Info:** The current model uses a CNN architecture optimized for image classification tasks.
""")

# Download predictions
if image_to_process:
    st.sidebar.divider()
    st.sidebar.header("💾 Export")
    
    # Create a simple report
    report = f"""
Image Classification Report
============================
Classification: {class_name}
Confidence: {confidence_percentage:.2f}%
Threshold: {confidence_threshold*100:.0f}%
Status: {"PASS" if confidence_percentage > confidence_threshold * 100 else "FAIL"}
"""
    
    st.sidebar.download_button(
        label="📥 Download Report",
        data=report,
        file_name="classification_report.txt",
        mime="text/plain"
    )



