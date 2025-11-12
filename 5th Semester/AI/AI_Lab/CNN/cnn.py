import tensorflow as tf
from tensorflow.keras import layers, models
import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

# STEP 0: Remove invalid/corrupted images using OpenCV
def clean_invalid_images_cv(directory):
    removed = 0
    for folder in os.listdir(directory):
        folder_path = os.path.join(directory, folder)
        if not os.path.isdir(folder_path):
            continue
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                img = cv2.imread(file_path)
                if img is None:
                    os.remove(file_path)
                    removed += 1
                    print(f"❌ Invalid image removed: {file_path}")
            except:
                os.remove(file_path)
                removed += 1
                print(f"⚠️ Problem reading: {file_path}")
    print(f"\n🧹 Cleanup Done! Removed {removed} invalid images.\n")

# Run cleanup on both train and test folders
clean_invalid_images_cv(r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\train")
clean_invalid_images_cv(r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\test")

# STEP 1: Load train & test datasets
raw_train_ds = tf.keras.utils.image_dataset_from_directory(
    r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\train",
    image_size=(256, 256),  
    batch_size=32
)

raw_test_ds = tf.keras.utils.image_dataset_from_directory(
    r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\test",
    image_size=(256, 256),  
    batch_size=32
)

# Save class names
class_names = raw_train_ds.class_names
print("Detected Classes:", class_names)

# STEP 2: Normalize images
train_ds = raw_train_ds.map(lambda x, y: (x / 255.0, y))
test_ds = raw_test_ds.map(lambda x, y: (x / 255.0, y))

# STEP 3: Improve performance
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

# STEP 4: Build CNN model
model = models.Sequential([
    layers.Input(shape=(256, 256, 3)), 
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

model.summary()

# STEP 5: Compile and Train model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_ds, validation_data=test_ds, epochs=10)

# STEP 6: Evaluate model
loss, accuracy = model.evaluate(test_ds)
print(f"\n✅ Test Accuracy: {accuracy*100:.2f}%")

# STEP 7: Plot accuracy/loss graphs
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.legend()
plt.show()

# STEP 8: Predict images 
def predict_image_opencv(img_path):
    if not os.path.exists(img_path):
        print(f"❌ File not found: {img_path}")
        return

    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Cannot read image: {img_path}")
        return

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    img_resized = cv2.resize(img, (256, 256)) 
    img_input = img_resized.reshape((1, 256, 256, 3)) / 255.0

    prediction = model.predict(img_input)
    predicted_class = class_names[np.argmax(prediction[0])]
    confidence = np.max(prediction[0]) * 100

    print(f"🖼️ {os.path.basename(img_path)} → {predicted_class} ({confidence:.2f}%)")

# STEP 9: Test with sample images
cat_path = r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\cat16.png"
dog_path = r"D:\Languages\Academic_PSTU_CSE\5th Semester\AI\AI_Lab\CNN\dog16.png"

predict_image_opencv(cat_path)
predict_image_opencv(dog_path)
