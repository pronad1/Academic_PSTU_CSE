"""
LIME - Local Interpretable Model-agnostic Explanations
Simple Implementation for Final Exam

Explains WHY a model made a prediction by:
1. Creating similar samples (perturbations)
2. Getting predictions for them
3. Training simple linear model locally
4. Showing which features matter most
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

# Training Data: [Study Hours, Previous Score] -> Admit(1) or Reject(0)
X_train = np.array([
    [8, 85], [6, 75], [9, 90], [5, 70], [7, 80],
    [10, 95], [4, 65], [8, 88], [6, 72], [9, 92]
])
y_train = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1])

features = ['Study_Hours', 'Previous_Score']

# Train black box model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# LIME Algorithm
def lime_explain(model, instance, num_samples=100):
    """Explain a single prediction"""
    
    # Step 1: Generate perturbed samples (add noise)
    samples = []
    for _ in range(num_samples):
        noise = np.random.normal(0, 0.2, size=instance.shape)
        perturbed = instance + instance * noise
        perturbed = np.maximum(perturbed, 0)  # Keep positive
        samples.append(perturbed)
    samples = np.array(samples)
    
    # Step 2: Get predictions from black box
    predictions = model.predict_proba(samples)[:, 1]
    
    # Step 3: Calculate weights (closer samples = more important)
    distances = np.sqrt(np.sum((samples - instance) ** 2, axis=1))
    weights = np.exp(-(distances ** 2) / 2)
    
    # Step 4: Train simple linear model
    linear_model = LinearRegression()
    linear_model.fit(samples, predictions, sample_weight=weights)
    
    # Step 5: Get feature importance
    importance = linear_model.coef_
    
    return importance

# Test instance
instance = np.array([7, 78])  # Study=7 hrs, Score=78

print("LIME - Explainable AI")
print("="*40)

# Get prediction
prediction = model.predict([instance])[0]
prob = model.predict_proba([instance])[0][1]

print(f"\nInput: {features}")
print(f"       {instance}")
print(f"\nPrediction: {'ADMIT' if prediction == 1 else 'REJECT'} ({prob:.2%})")

# Explain with LIME
importance = lime_explain(model, instance)

print("\nFeature Importance:")
for i, feat in enumerate(features):
    sign = "↑" if importance[i] > 0 else "↓"
    print(f"  {feat:15}: {importance[i]:+.3f} {sign}")

print("\nMost Important:", features[np.argmax(np.abs(importance))])
print("="*40)

