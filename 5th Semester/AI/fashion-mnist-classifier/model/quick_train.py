import numpy as np
import tensorflow as tf
from tensorflow import keras
import os

def load_and_preprocess_data():
    """Load and preprocess Fashion MNIST data"""
    fashion_mnist = keras.datasets.fashion_mnist
    (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    
    # Normalize pixel values
    train_images = train_images / 255.0
    test_images = test_images / 255.0
    
    # Reshape for CNN
    x_train = train_images.reshape(-1, 28, 28, 1)
    x_test = test_images.reshape(-1, 28, 28, 1)
    
    return (x_train, train_labels), (x_test, test_labels)

def create_simple_model():
    """Create a simple CNN model without hyperparameter tuning"""
    model = keras.Sequential([
        # First conv_block
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.25),
        
        # Second conv_block
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.25),
        
        # Third conv_block
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Dropout(0.25),
        
        # --------------------------------
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_simple_model(epochs=15):
    """Train a simple model quickly"""
    print("Loading data...")
    (x_train, train_labels), (x_test, test_labels) = load_and_preprocess_data()
    
    print("Creating model...")
    model = create_simple_model()
    
    print("Model Architecture:")
    model.summary()
    
    # Callbacks
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss', 
        patience=5, 
        restore_best_weights=True
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=1e-7
    )
    
    print(f"\nTraining model for {epochs} epochs...")
    history = model.fit(
        x_train, train_labels,
        epochs=epochs,
        batch_size=64,
        validation_split=0.2,
        callbacks=[early_stop, reduce_lr],
        verbose=1
    )
    
    # Evaluate model
    test_loss, test_accuracy = model.evaluate(x_test, test_labels, verbose=0)
    print(f"\nModel Performance:")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    # Save model
    model.save('trained_model.h5')
    print("Model saved as 'trained_model.h5'")
    
    return model, history

if __name__ == "__main__":
    train_simple_model(epochs=15)