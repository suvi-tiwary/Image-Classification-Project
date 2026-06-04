# 🚀 Quick Start Guide

Get your Image Classification web app running in 3 simple steps!

## Step 1: Install Dependencies

Open a terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required packages (Streamlit, TensorFlow, PIL, etc.)

## Step 2: Run the App

Once dependencies are installed, start the web app:

### Option A: Using Python directly
```bash
streamlit run app.py
```

### Option B: Using the setup script
```bash
python run_app.py
```

## Step 3: Use the App

The app will automatically open in your browser at `http://localhost:8501`

1. **Upload an image** or **take a photo** using your camera
2. **View the prediction** - see which class (With/Without Mask) and confidence %
3. **Adjust settings** using the sidebar if needed
4. **Download results** to save the classification report

---

## 📋 What You Can Do

✅ Upload images (JPG, PNG, BMP, WebP)  
✅ Take photos directly from your camera  
✅ Get real-time predictions with confidence scores  
✅ Adjust confidence threshold for stricter/lenient classification  
✅ Download classification reports  
✅ Train your own model with custom data  

---

## 🎯 Using Your Own Trained Model

If you have a pre-trained model or want to train one:

### Train a new model:
```bash
python train_model.py
```

**Note:** You'll need a dataset with this structure:
```
data/
├── with_mask/      (images with masks)
└── without_mask/   (images without masks)
```

The trained model will be saved as `image_classification_model.h5`

### Use an existing model:
- Place your `.h5` model file in the project directory
- Name it `image_classification_model.h5`
- Restart the Streamlit app

---

## ⚙️ Settings & Configuration

Access settings from the **left sidebar**:

- **Confidence Threshold**: Adjust how confident the model must be
  - Lower = More lenient (more predictions pass)
  - Higher = More strict (fewer predictions pass)

- **Model Type**: Choose between different model architectures
  - MobileNetV2 Transfer Learning (faster, uses pre-trained weights)
  - Custom CNN (trained from scratch)

---

## 🐛 Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**App won't start:**
- Check that Python 3.7+ is installed: `python --version`
- Close any other app using port 8501
- Try: `streamlit run app.py --logger.level=debug`

**Model not loading:**
- A demo model will be used if no trained model is found
- Train your own with `python train_model.py`

**Slow predictions:**
- First prediction takes time (model loading)
- Subsequent predictions are faster
- GPU support can speed this up significantly

---

## 📁 Project Structure

```
Image Classification project/
├── app.py                           # Main Streamlit app
├── train_model.py                   # Training script
├── run_app.py                       # Quick start script
├── requirements.txt                 # Python dependencies
├── README.md                        # Full documentation
├── QUICKSTART.md                    # This file
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
└── image_classification_model.h5    # Trained model (after training)
```

---

## 💡 Tips

- **For best results**: Use clear, well-lit images
- **Accuracy depends on**: Quality of training data and model training
- **Save your model**: Once trained, the `.h5` file is reusable
- **Batch processing**: Modify `app.py` to process multiple images

---

## 📞 Support

For Streamlit help: https://docs.streamlit.io/  
For TensorFlow help: https://www.tensorflow.org/  
For Python help: https://www.python.org/doc/

Enjoy! 🎉
