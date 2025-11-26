from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import io
import base64
import matplotlib
# Use non-interactive backend to avoid threading issues
matplotlib.use('Agg')  # Important: This must be before importing pyplot
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load the trained model
model = None
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

def load_model():
    """Load the trained model"""
    global model
    try:
        if os.path.exists('trained_model.h5'):
            model = keras.models.load_model('trained_model.h5')
            print("✅ Model loaded successfully!")
            return True
        else:
            print("❌ No pre-trained model found. Please train the model first.")
            print("💡 Run: python model/quick_train.py")
            return False
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False

def preprocess_image(image):
    """Preprocess uploaded image for prediction"""
    try:
        # Convert to grayscale if needed
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize to 28x28
        image = image.resize((28, 28))
        
        # Convert to numpy array and normalize
        image_array = np.array(image) / 255.0
        
        # Invert colors if background is white (Fashion MNIST has white background)
        if np.mean(image_array) > 0.5:  # If background is white
            image_array = 1 - image_array
        
        # Reshape for model input
        image_array = image_array.reshape(1, 28, 28, 1)
        
        return image_array
    except Exception as e:
        raise Exception(f"Image preprocessing failed: {str(e)}")

def create_prediction_plot(processed_image, predictions):
    """Create prediction visualization without threading issues"""
    try:
        # Create figure with specific size
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Show processed image
        ax1.imshow(processed_image[0, :, :, 0], cmap='gray')
        ax1.set_title('Processed Image', fontsize=12, pad=10)
        ax1.axis('off')
        
        # Show prediction probabilities
        y_pos = np.arange(len(class_names))
        bars = ax2.barh(y_pos, predictions[0])
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(class_names, fontsize=10)
        ax2.set_xlabel('Probability', fontsize=11)
        ax2.set_title('Prediction Probabilities', fontsize=12, pad=10)
        ax2.set_xlim(0, 1)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            # Only label if probability is significant
            if width > 0.1:
                ax2.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{width:.3f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        
        # Save plot to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)  # Important: close the figure to free memory
        
        return plot_data
    except Exception as e:
        print(f"Plot creation error: {e}")
        return None

def create_sample_plot(sample_image, true_label, predictions):
    """Create sample prediction visualization"""
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Show sample image
        ax1.imshow(sample_image, cmap='gray')
        ax1.set_title(f'True Label: {class_names[true_label]}', fontsize=12, pad=10)
        ax1.axis('off')
        
        # Show prediction probabilities
        y_pos = np.arange(len(class_names))
        bars = ax2.barh(y_pos, predictions[0])
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(class_names, fontsize=10)
        ax2.set_xlabel('Probability', fontsize=11)
        ax2.set_title('Prediction Probabilities', fontsize=12, pad=10)
        ax2.set_xlim(0, 1)
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            if width > 0.1:
                ax2.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
                        f'{width:.3f}', ha='left', va='center', fontsize=9)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        plt.close(fig)  # Important: close the figure
        
        return plot_data
    except Exception as e:
        print(f"Sample plot creation error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html', class_names=class_names)

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first by running: python model/quick_train.py'})
    
    try:
        # Check if image file is present
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'})
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'})
        
        # Check file type
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            return jsonify({'error': 'Please upload an image file (PNG, JPG, JPEG, GIF, BMP)'})
        
        # Read and preprocess image
        image = Image.open(io.BytesIO(file.read()))
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Create visualization
        plot_data = create_prediction_plot(processed_image, predictions)
        
        if not plot_data:
            return jsonify({'error': 'Failed to create visualization'})
        
        return jsonify({
            'success': True,
            'prediction': class_names[predicted_class],
            'confidence': confidence,
            'all_predictions': {name: float(prob) for name, prob in zip(class_names, predictions[0])},
            'plot': plot_data
        })
        
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'})

@app.route('/sample_prediction', methods=['POST'])
def sample_prediction():
    if model is None:
        return jsonify({'error': 'Model not loaded. Please train the model first.'})
    
    try:
        from tensorflow.keras.datasets import fashion_mnist
        import random
        
        # Load test data
        (_, _), (test_images, test_labels) = fashion_mnist.load_data()
        
        # Select random sample
        index = random.randint(0, len(test_images) - 1)
        sample_image = test_images[index] / 255.0
        true_label = test_labels[index]
        
        # Preprocess for prediction
        processed_image = sample_image.reshape(1, 28, 28, 1)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Create visualization
        plot_data = create_sample_plot(sample_image, true_label, predictions)
        
        if not plot_data:
            return jsonify({'error': 'Failed to create visualization'})
        
        return jsonify({
            'success': True,
            'prediction': class_names[predicted_class],
            'true_label': class_names[true_label],
            'confidence': confidence,
            'all_predictions': {name: float(prob) for name, prob in zip(class_names, predictions[0])},
            'plot': plot_data,
            'is_correct': predicted_class == true_label
        })
        
    except Exception as e:
        return jsonify({'error': f'Sample prediction failed: {str(e)}'})

@app.route('/model_status')
def model_status():
    """Check if model is loaded"""
    status = load_model()  # Try to reload model
    return jsonify({
        'model_loaded': model is not None,
        'message': 'Model is ready!' if model else 'Model not loaded. Train model first.'
    })

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

if __name__ == '__main__':
    # Set environment variable to avoid TensorFlow warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # Load model at startup
    model_loaded = load_model()
    
    print("🚀 Fashion MNIST Classifier Starting...")
    print("📊 Model status:", "✅ Loaded" if model_loaded else "❌ Not loaded")
    if not model_loaded:
        print("💡 To train model, run: python model/train_model.py")
    print("🌐 Web interface available at: http://localhost:5000")
    print("=" * 50)
    
    # Run with threaded=False to avoid matplotlib issues
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=False)