import tensorflow as tf
from tensorflow import keras
import keras_tuner as kt
from train_model import load_and_preprocess_data, build_model

def quick_tuning():
    """Quick hyperparameter tuning for demonstration"""
    (x_train, train_labels), (_, _), (_, _) = load_and_preprocess_data()
    
    # Use a subset for faster tuning
    x_subset = x_train[:10000]
    y_subset = train_labels[:10000]
    
    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=3)
    
    tuner = kt.BayesianOptimization(
        build_model,
        objective='val_accuracy',
        max_trials=10,
        directory='quick_tuning',
        project_name='fashion_mnist_quick'
    )
    
    tuner.search(
        x_subset, y_subset,
        epochs=10,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )
    
    return tuner

if __name__ == "__main__":
    tuner = quick_tuning()
    best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
    print("Quick tuning completed!")