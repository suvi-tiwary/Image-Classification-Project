"""
Image Classification Model Training Script
Train a CNN model for mask detection/classification
"""

import os
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

# Configuration
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20
VALIDATION_SPLIT = 0.2

class ImageClassificationTrainer:
    def __init__(self, img_size=IMG_SIZE):
        self.img_size = img_size
        self.model = None
        self.history = None
        
    def load_images_from_directory(self, directory_path, label):
        """Load images from a directory"""
        images = []
        
        if not os.path.exists(directory_path):
            print(f"❌ Directory not found: {directory_path}")
            return [], []
        
        files = [f for f in os.listdir(directory_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        print(f"Loading {len(files)} images from {directory_path}...")
        
        for filename in files:
            try:
                img_path = os.path.join(directory_path, filename)
                img = Image.open(img_path)
                img = img.resize((self.img_size, self.img_size))
                img = img.convert('RGB')
                img_array = np.array(img) / 255.0
                images.append(img_array)
            except Exception as e:
                print(f"⚠️ Error loading {filename}: {e}")
                continue
        
        labels = [label] * len(images)
        print(f"✅ Loaded {len(images)} images")
        return images, labels
    
    def build_model(self):
        """Build CNN model"""
        self.model = keras.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(1, activation='sigmoid')  # Binary classification
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )
        
        print("\n📐 Model Architecture:")
        self.model.summary()
        return self.model
    
    def train(self, x_train, y_train):
        """Train the model"""
        print(f"\n🚀 Training model for {EPOCHS} epochs...")
        
        self.history = self.model.fit(
            x_train, y_train,
            epochs=EPOCHS,
            batch_size=BATCH_SIZE,
            validation_split=VALIDATION_SPLIT,
            verbose=1
        )
        
        return self.history
    
    def evaluate(self, x_test, y_test):
        """Evaluate the model"""
        loss, accuracy = self.model.evaluate(x_test, y_test, verbose=0)
        print(f"\n📊 Test Results:")
        print(f"   Loss: {loss:.4f}")
        print(f"   Accuracy: {accuracy*100:.2f}%")
        return loss, accuracy
    
    def save_model(self, filepath='image_classification_model.h5'):
        """Save the trained model"""
        self.model.save(filepath)
        print(f"\n💾 Model saved to: {filepath}")
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy plot
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.set_title('Model Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        print("📈 Training history saved to: training_history.png")
        plt.show()

def main():
    """Main training function"""
    print("="*50)
    print("Image Classification Model Training")
    print("="*50)
    
    # Configure dataset paths
    # Modify these paths to match your dataset structure
    with_mask_path = "./data/with_mask"
    without_mask_path = "./data/without_mask"
    
    # Initialize trainer
    trainer = ImageClassificationTrainer()
    
    # Load dataset
    print("\n📂 Loading dataset...")
    with_mask_images, with_mask_labels = trainer.load_images_from_directory(with_mask_path, 1)
    without_mask_images, without_mask_labels = trainer.load_images_from_directory(without_mask_path, 0)
    
    # Check if data was loaded
    if not with_mask_images and not without_mask_images:
        print("\n❌ No images found! Please check your dataset paths.")
        print(f"Expected directories:")
        print(f"  - {with_mask_path}")
        print(f"  - {without_mask_path}")
        return
    
    # Combine data
    all_images = np.array(with_mask_images + without_mask_images)
    all_labels = np.array(with_mask_labels + without_mask_labels)
    
    print(f"\n📊 Dataset Summary:")
    print(f"   Total samples: {len(all_images)}")
    print(f"   With Mask: {sum(all_labels)}")
    print(f"   Without Mask: {len(all_labels) - sum(all_labels)}")
    
    # Split data
    x_train, x_test, y_train, y_test = train_test_split(
        all_images, all_labels,
        test_size=0.2,
        random_state=42,
        stratify=all_labels
    )
    
    print(f"\n✂️  Data Split:")
    print(f"   Training samples: {len(x_train)}")
    print(f"   Test samples: {len(x_test)}")
    
    # Build model
    print("\n🏗️  Building model...")
    trainer.build_model()
    
    # Train model
    trainer.train(x_train, y_train)
    
    # Evaluate model
    trainer.evaluate(x_test, y_test)
    
    # Plot history
    trainer.plot_training_history()
    
    # Save model
    trainer.save_model()
    
    print("\n" + "="*50)
    print("✅ Training Complete!")
    print("="*50)
    print("\nNext steps:")
    print("1. Run 'streamlit run app.py' to test the model")
    print("2. Upload test images to verify predictions")
    print("3. Adjust threshold in the app settings if needed")

if __name__ == "__main__":
    main()
