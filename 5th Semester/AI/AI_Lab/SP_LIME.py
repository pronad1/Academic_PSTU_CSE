"""
SP-LIME - Submodular Pick LIME
Simple Implementation for Final Exam

Difference from LIME:
- LIME: Explains ONE prediction
- SP-LIME: Picks MULTIPLE representative instances to explain the WHOLE model

Steps:
1. Run LIME on multiple instances
2. Select most representative explanations using submodular optimization
3. Show global feature importance
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

# LIME for single instance
def lime_explain(model, instance, num_samples=100):
    """Explain a single prediction"""
    samples = []
    for _ in range(num_samples):
        noise = np.random.normal(0, 0.2, size=instance.shape)
        perturbed = instance + instance * noise
        perturbed = np.maximum(perturbed, 0)
        samples.append(perturbed)
    samples = np.array(samples)
    
    predictions = model.predict_proba(samples)[:, 1]
    distances = np.sqrt(np.sum((samples - instance) ** 2, axis=1))
    weights = np.exp(-(distances ** 2) / 2)
    
    linear_model = LinearRegression()
    linear_model.fit(samples, predictions, sample_weight=weights)
    
    return linear_model.coef_

# SP-LIME Algorithm
def sp_lime(model, X_data, num_picks=3):
    """
    Submodular Pick LIME - Select representative instances
    
    Steps:
    1. Get LIME explanations for all instances
    2. Calculate coverage (how many features are explained)
    3. Pick instances that maximize coverage (submodular optimization)
    """
    
    # Step 1: Get LIME explanation for each instance
    all_explanations = []
    for instance in X_data:
        importance = lime_explain(model, instance)
        all_explanations.append(importance)
    
    all_explanations = np.array(all_explanations)
    
    # Step 2: Submodular Pick - Select diverse representative instances
    selected_indices = []
    covered_features = set()
    
    for _ in range(num_picks):
        best_idx = None
        best_coverage = 0
        
        # Find instance that adds most new coverage
        for i in range(len(X_data)):
            if i in selected_indices:
                continue
            
            # Check which features are important in this explanation
            important_features = set(np.where(np.abs(all_explanations[i]) > 0.01)[0])
            
            # Calculate new coverage
            new_coverage = len(important_features - covered_features)
            
            if new_coverage > best_coverage:
                best_coverage = new_coverage
                best_idx = i
        
        if best_idx is not None:
            selected_indices.append(best_idx)
            important_features = set(np.where(np.abs(all_explanations[best_idx]) > 0.01)[0])
            covered_features.update(important_features)
    
    return selected_indices, all_explanations

# Main
print("SP-LIME - Global Model Explanation")
print("="*40)

# Run SP-LIME
num_picks = 3
selected_indices, all_explanations = sp_lime(model, X_train, num_picks)

print(f"\nSelected {num_picks} representative instances:\n")

for idx in selected_indices:
    instance = X_train[idx]
    prediction = model.predict([instance])[0]
    importance = all_explanations[idx]
    
    print(f"Instance {idx+1}: {instance}")
    print(f"  Prediction: {'ADMIT' if prediction == 1 else 'REJECT'}")
    print(f"  Feature Importance:")
    for i, feat in enumerate(features):
        sign = "↑" if importance[i] > 0 else "↓"
        print(f"    {feat:15}: {importance[i]:+.3f} {sign}")
    print()

# Global feature importance (average of selected instances)
global_importance = np.mean([all_explanations[i] for i in selected_indices], axis=0)

print("="*40)
print("Global Feature Importance (Model-wide):")
print("="*40)
for i, feat in enumerate(features):
    sign = "↑" if global_importance[i] > 0 else "↓"
    print(f"  {feat:15}: {global_importance[i]:+.3f} {sign}")

print("\nMost Important:", features[np.argmax(np.abs(global_importance))])
print("="*40)
