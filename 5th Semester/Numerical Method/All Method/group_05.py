import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor, SGDClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

# Load your dataset
df = pd.read_csv(r"D:\Languages\Python-Library\All Method\rajshahi_housing_final.csv")

# Separate features and target
X = df.iloc[:, :-1]

y = df.iloc[:, -1]

# One-hot encode categorical variables
X = pd.get_dummies(X)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Regression task with SGDRegressor
regressor = SGDRegressor(random_state=42, max_iter=1000, tol=1e-3)
regressor.fit(X_train_scaled, y_train)

y_pred = regressor.predict(X_test_scaled)

# Show results
result_df = pd.DataFrame({'Real Values': y_test, 'Predicted Values': y_pred})
print(result_df.head(10))

# Plot Actual vs Predicted
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, color='blue', alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted House Prices')
plt.grid(True)
plt.show()

# ======= Classification Task =======
# Create classification target: 1 if price > median else 0
threshold = y.median()
y_class = (y > threshold).astype(int)

# Split for classification
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X, y_class, test_size=0.2, random_state=42)

# Scale features for classification
scaler_cls = StandardScaler()
X_train_cls_scaled = scaler_cls.fit_transform(X_train_cls)
X_test_cls_scaled = scaler_cls.transform(X_test_cls)

# Train classifier
clf = SGDClassifier(random_state=42, max_iter=1000, tol=1e-3)
clf.fit(X_train_cls_scaled, y_train_cls)

y_pred_cls = clf.predict(X_test_cls_scaled)

# Classification metrics
print("\n=== Classification Metrics (SGD Classifier) ===")
print(f"Accuracy:  {accuracy_score(y_test_cls, y_pred_cls):.4f}")
print(f"Precision: {precision_score(y_test_cls, y_pred_cls):.4f}")
print(f"Recall:    {recall_score(y_test_cls, y_pred_cls):.4f}")
print(f"F1 Score:  {f1_score(y_test_cls, y_pred_cls):.4f}")





import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load dataset
df = pd.read_csv(r"D:\Languages\Python-Library\All Method\rajshahi_housing_final.csv")
# print(df.shape)
df = df.dropna()

# Features and target
X = df.iloc[:, :-1]
y = df.iloc[:, -1]

# One-hot encode categorical columns
X = pd.get_dummies(X)
print(X)
# X = pd.get_dummies(X, dtype=int)
# print(X)

# Split data
X_train, X_test, y_train_reg, y_test_reg = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# === BGD for Regression ===
def batch_gradient_descent(X, y, lr=0.01, epochs=1000):
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0

    for epoch in range(epochs):
        y_pred = np.dot(X, weights) + bias
        error = y_pred - y

        dw = (1/m) * np.dot(X.T, error)
        db = (1/m) * np.sum(error)

        weights -= lr * dw
        bias -= lr * db

    return weights, bias

# Train regression model
weights, bias = batch_gradient_descent(X_train_scaled, y_train_reg.values, lr=0.01, epochs=1000)
y_pred_reg = np.dot(X_test_scaled, weights) + bias

# Show results
result_df = pd.DataFrame({'Real Values': y_test_reg.values, 'Predicted Values': y_pred_reg})
print(result_df.head(10))


# Plot regression prediction
plt.figure(figsize=(10,6))
plt.scatter(y_test_reg, y_pred_reg, color='yellow', alpha=0.6)
plt.plot([y_test_reg.min(), y_test_reg.max()], [y_test_reg.min(), y_test_reg.max()], 'r--')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual vs Predicted House Prices (BGD)')
plt.grid(True)
plt.show()

# === BGD for Classification ===
# Create binary target: 1 if price > median else 0
threshold = y.median()
y_class = (y > threshold).astype(int)

# Split for classification
X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X, y_class, test_size=0.2, random_state=42)

# Scale
X_train_cls_scaled = scaler.fit_transform(X_train_cls)
X_test_cls_scaled = scaler.transform(X_test_cls)

# BGD for binary classification (Perceptron-like)
def bgd_classifier(X, y, lr=0.01, epochs=1000):
    m, n = X.shape
    weights = np.zeros(n)
    bias = 0

    for epoch in range(epochs):
        linear_output = np.dot(X, weights) + bias
        y_pred = (linear_output > 0).astype(int)

        error = y_pred - y
        dw = (1/m) * np.dot(X.T, error)
        db = (1/m) * np.sum(error)

        weights -= lr * dw
        bias -= lr * db
    return weights, bias

# Train classifier
weights_cls, bias_cls = bgd_classifier(X_train_cls_scaled, y_train_cls.values, lr=0.01, epochs=1000)

# Predict
y_pred_cls = (np.dot(X_test_cls_scaled, weights_cls) + bias_cls > 0).astype(int)


# Classification metrics
print("\n=== Classification Metrics (BGD Classifier) ===")
print(f"Accuracy:  {accuracy_score(y_test_cls, y_pred_cls):.4f}")
print(f"Precision: {precision_score(y_test_cls, y_pred_cls):.4f}")
print(f"Recall:    {recall_score(y_test_cls, y_pred_cls):.4f}")
print(f"F1 Score:  {f1_score(y_test_cls, y_pred_cls):.4f}")
