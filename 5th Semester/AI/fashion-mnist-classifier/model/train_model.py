# import numpy as np
# import matplotlib.pyplot as plt
# import tensorflow as tf
# from tensorflow import keras
# import keras_tuner as kt
# import os

# def load_and_preprocess_data():
#     """Load and preprocess Fashion MNIST data"""
#     fashion_mnist = keras.datasets.fashion_mnist
#     (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
    
#     # Normalize pixel values
#     train_images = train_images / 255.0
#     test_images = test_images / 255.0
    
#     # Reshape for CNN
#     x_train = train_images.reshape(-1, 28, 28, 1)
#     x_test = test_images.reshape(-1, 28, 28, 1)
    
#     return (x_train, train_labels), (x_test, test_labels), (train_images, test_images)

# def build_model(hp):
#     """Build model for hyperparameter tuning"""
#     model = keras.Sequential([
#         # First conv_block
#         keras.layers.Conv2D(
#             filters=hp.Choice('conv_1_filter', values=[32, 64, 128]),
#             kernel_size=hp.Choice('conv_1_kernel', values=[3, 5]),
#             activation='relu',
#             input_shape=(28, 28, 1)),
#         keras.layers.MaxPooling2D((2, 2)),
#         keras.layers.Dropout(hp.Float('dropout_1', 0.1, 0.5, step=0.1)),
        
#         # Second conv_block
#         keras.layers.Conv2D(
#             filters=hp.Choice('conv_2_filter', values=[32, 64, 128]),
#             kernel_size=hp.Choice('conv_2_kernel', values=[3, 5]),
#             activation='relu'),
#         keras.layers.MaxPooling2D((2, 2)),
#         keras.layers.Dropout(hp.Float('dropout_2', 0.1, 0.5, step=0.1)),
        
#         # Third conv_block for better feature extraction
#         keras.layers.Conv2D(
#             filters=hp.Choice('conv_3_filter', values=[32, 64]),
#             kernel_size=hp.Choice('conv_3_kernel', values=[3]),
#             activation='relu'),
#         keras.layers.Dropout(hp.Float('dropout_3', 0.1, 0.4, step=0.1)),
        
#         # --------------------------------
#         keras.layers.Flatten(),
#         keras.layers.Dense(units=hp.Choice('dense_1', values=[128, 256, 512]),
#                           activation='relu'),
#         keras.layers.Dropout(hp.Float('dropout_4', 0.2, 0.6, step=0.1)),
        
#         keras.layers.Dense(units=hp.Choice('dense_2', values=[64, 128]),
#                           activation='relu'),
#         keras.layers.Dropout(hp.Float('dropout_5', 0.1, 0.4, step=0.1)),
        
#         # --------------------------------
#         keras.layers.Dense(10, activation='softmax')
#     ])

#     model.compile(
#         optimizer=keras.optimizers.Adam(
#             hp.Choice('learning_rate', values=[1e-3, 1e-4])
#         ),
#         loss='sparse_categorical_crossentropy',
#         metrics=['accuracy']
#     )
#     return model

# def perform_hyperparameter_tuning(x_train, train_labels):
#     """Perform hyperparameter tuning"""
#     early_stop = keras.callbacks.EarlyStopping(
#         monitor='val_loss', 
#         patience=5, 
#         restore_best_weights=True
#     )
    
#     tuner = kt.Hyperband(
#         build_model,
#         objective="val_accuracy",
#         max_epochs=10,
#         factor=3,
#         directory='hyperband_tuning',
#         project_name='fashion_mnist'
#     )
    
#     tuner.search(
#         x_train, train_labels, 
#         epochs=20, 
#         validation_split=0.2,
#         callbacks=[early_stop],
#         batch_size=64,
#         verbose=1
#     )
    
#     return tuner

# def train_final_model(x_train, train_labels, x_test, test_labels, best_hps):
#     """Train final model with best hyperparameters"""
#     early_stop = keras.callbacks.EarlyStopping(
#         monitor='val_loss', 
#         patience=10, 
#         restore_best_weights=True
#     )
    
#     reduce_lr = keras.callbacks.ReduceLROnPlateau(
#         monitor='val_loss',
#         factor=0.2,
#         patience=5,
#         min_lr=1e-7
#     )
    
#     model = build_model(best_hps)
    
#     history = model.fit(
#         x_train, train_labels,
#         epochs=100,
#         batch_size=64,
#         validation_split=0.2,
#         callbacks=[early_stop, reduce_lr],
#         verbose=1
#     )
    
#     # Evaluate model
#     test_loss, test_accuracy = model.evaluate(x_test, test_labels, verbose=0)
#     print(f"Test Accuracy: {test_accuracy:.4f}")
#     print(f"Test Loss: {test_loss:.4f}")
    
#     return model, history

# def save_model(model, filename='trained_model.h5'):
#     """Save trained model"""
#     model.save(filename)
#     print(f"Model saved as {filename}")

# if __name__ == "__main__":
#     # Load data
#     (x_train, train_labels), (x_test, test_labels), (_, _) = load_and_preprocess_data()
    
#     # Perform hyperparameter tuning
#     print("Starting hyperparameter tuning...")
#     tuner = perform_hyperparameter_tuning(x_train, train_labels)
    
#     # Get best hyperparameters
#     best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    
#     print("\nBest Hyperparameters:")
#     print(f"conv_1_filter: {best_hps.get('conv_1_filter')}")
#     print(f"conv_1_kernel: {best_hps.get('conv_1_kernel')}")
#     print(f"conv_2_filter: {best_hps.get('conv_2_filter')}")
#     print(f"conv_2_kernel: {best_hps.get('conv_2_kernel')}")
#     print(f"conv_3_filter: {best_hps.get('conv_3_filter')}")
#     print(f"conv_3_kernel: {best_hps.get('conv_3_kernel')}")
#     print(f"dense_1: {best_hps.get('dense_1')}")
#     print(f"dense_2: {best_hps.get('dense_2')}")
#     print(f"learning_rate: {best_hps.get('learning_rate')}")
    
#     # Train final model
#     print("\nTraining final model...")
#     model, history = train_final_model(x_train, train_labels, x_test, test_labels, best_hps)
    
#     # Save model
#     save_model(model)




import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import keras_tuner as kt
import os
import time

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
    
    return (x_train, train_labels), (x_test, test_labels), (train_images, test_images)

def build_model(hp):
    """Build model for hyperparameter tuning"""
    model = keras.Sequential([
        # First conv_block
        keras.layers.Conv2D(
            filters=hp.Choice('conv_1_filter', values=[32, 64]),
            kernel_size=hp.Choice('conv_1_kernel', values=[3, 5]),
            activation='relu',
            input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(hp.Float('dropout_1', 0.1, 0.3, step=0.1)),
        
        # Second conv_block
        keras.layers.Conv2D(
            filters=hp.Choice('conv_2_filter', values=[32, 64]),
            kernel_size=hp.Choice('conv_2_kernel', values=[3, 5]),
            activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(hp.Float('dropout_2', 0.1, 0.3, step=0.1)),
        
        # --------------------------------
        keras.layers.Flatten(),
        keras.layers.Dense(units=hp.Choice('dense_1', values=[128, 256]),
                          activation='relu'),
        keras.layers.Dropout(hp.Float('dropout_3', 0.2, 0.4, step=0.1)),
        
        # --------------------------------
        keras.layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer=keras.optimizers.Adam(
            hp.Choice('learning_rate', values=[1e-3, 1e-4])
        ),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def quick_hyperparameter_tuning(x_train, train_labels, max_trials=5, max_epochs=5):
    """Quick hyperparameter tuning with limited trials"""
    print("Starting quick hyperparameter tuning...")
    
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss', 
        patience=2, 
        restore_best_weights=True
    )
    
    # Use BayesianOptimization for faster convergence
    tuner = kt.BayesianOptimization(
        build_model,
        objective="val_accuracy",
        max_trials=max_trials,
        directory='quick_tuning',
        project_name='fashion_mnist_quick'
    )
    
    # Use subset for faster tuning
    x_subset = x_train[:10000]
    y_subset = train_labels[:10000]
    
    print(f"Running {max_trials} trials with {max_epochs} epochs each...")
    
    start_time = time.time()
    tuner.search(
        x_subset, y_subset,
        epochs=max_epochs,
        validation_split=0.2,
        callbacks=[early_stop],
        batch_size=64,
        verbose=1
    )
    
    end_time = time.time()
    print(f"Hyperparameter tuning completed in {end_time - start_time:.2f} seconds")
    
    return tuner

def train_final_model(x_train, train_labels, x_test, test_labels, best_hps, epochs=20):
    """Train final model with best hyperparameters"""
    print("\nTraining final model with best hyperparameters...")
    
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
    
    model = build_model(best_hps)
    
    print("Model Architecture:")
    model.summary()
    
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
    print(f"\nFinal Model Performance:")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    print(f"Test Loss: {test_loss:.4f}")
    
    return model, history

def save_model(model, filename='trained_model.h5'):
    """Save trained model"""
    model.save(filename)
    print(f"Model saved as {filename}")

def plot_training_history(history):
    """Plot training history"""
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    plt.show()

if __name__ == "__main__":
    # Load data
    print("Loading Fashion MNIST dataset...")
    (x_train, train_labels), (x_test, test_labels), (_, _) = load_and_preprocess_data()
    
    print(f"Training data shape: {x_train.shape}")
    print(f"Test data shape: {x_test.shape}")
    
    # Perform quick hyperparameter tuning
    tuner = quick_hyperparameter_tuning(x_train, train_labels, max_trials=5, max_epochs=5)
    
    # Get best hyperparameters
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    
    print("\n" + "="*50)
    print("BEST HYPERPARAMETERS FOUND:")
    print("="*50)
    print(f"conv_1_filter: {best_hps.get('conv_1_filter')}")
    print(f"conv_1_kernel: {best_hps.get('conv_1_kernel')}")
    print(f"conv_2_filter: {best_hps.get('conv_2_filter')}")
    print(f"conv_2_kernel: {best_hps.get('conv_2_kernel')}")
    print(f"dense_1: {best_hps.get('dense_1')}")
    print(f"learning_rate: {best_hps.get('learning_rate')}")
    print(f"dropout_1: {best_hps.get('dropout_1')}")
    print(f"dropout_2: {best_hps.get('dropout_2')}")
    print(f"dropout_3: {best_hps.get('dropout_3')}")
    
    # Train final model
    model, history = train_final_model(x_train, train_labels, x_test, test_labels, best_hps, epochs=20)
    
    # Plot training history
    plot_training_history(history)
    
    # Save model
    save_model(model)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*50)