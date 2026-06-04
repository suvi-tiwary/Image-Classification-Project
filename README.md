# Image Classification Web Application

An interactive Streamlit web application for classifying images as "With Mask" or "Without Mask" using deep learning.

## Features

✨ **Interactive Web Interface**
- Upload images or capture photos with your camera
- Real-time predictions with confidence scores
- Adjustable confidence threshold for classification
- Beautiful, user-friendly dashboard

📊 **Model Capabilities**
- Binary image classification (Mask / No Mask)
- High-accuracy predictions
- Support for multiple image formats (JPG, PNG, BMP, WebP)
- Confidence visualization with progress bars

💾 **Export Results**
- Download classification reports
- Detailed prediction breakdown

## Installation

1. **Clone or download this project**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the web app**
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Using the Interactive App

1. **Upload an Image**
   - Click "Choose an image file" to select from your computer
   - OR click the camera button to capture a photo

2. **View Results**
   - The app will analyze the image and show:
     - Classification result (With Mask / Without Mask)
     - Confidence percentage
     - Detailed prediction breakdown

3. **Adjust Settings** (Optional)
   - Use the sidebar to adjust the confidence threshold
   - Lower threshold = more lenient, Higher threshold = stricter

4. **Download Report**
   - Click the download button to save classification results

## Training Your Own Model

If you want to train a custom model with your dataset, use the `train_model.py` script:

```bash
python train_model.py
```

This script will:
1. Load images from your dataset
2. Train a CNN model
3. Save the model as `image_classification_model.h5`

Then restart the Streamlit app to use your trained model.

## Project Structure

```
├── app.py                           # Main Streamlit application
├── train_model.py                   # Model training script
├── requirements.txt                 # Python dependencies
├── image_classification_model.h5    # Trained model (generated after training)
└── README.md                        # This file
```

## Model Architecture

The application uses a Convolutional Neural Network (CNN) with:
- 3 Convolutional layers with ReLU activation
- MaxPooling layers for dimensionality reduction
- Flatten layer to convert to 1D
- Dense layers with dropout for regularization
- Sigmoid output for binary classification

## Performance

Expected accuracy: 95%+ (when properly trained)
Input image size: 128x128 pixels
Supported formats: JPG, JPEG, PNG, BMP, WebP

## Troubleshooting

**"Model not found" error:**
- Train your model using `train_model.py`
- Or use the demo model that comes built-in

**Poor prediction accuracy:**
- Ensure images are clear and well-lit
- Make sure model is properly trained on your dataset
- Try adjusting the confidence threshold

**Slow predictions:**
- This is normal for the first prediction (model loading)
- Subsequent predictions will be faster due to caching

## System Requirements

- Python 3.7+
- 2GB RAM minimum (4GB+ recommended)
- GPU optional but recommended for faster processing

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the Streamlit documentation:
https://docs.streamlit.io/
