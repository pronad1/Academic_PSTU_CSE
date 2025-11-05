# =============================
# 📊 EDA Template for Any Dataset
# Author: Prosenjit Sir's ML Toolkit
# =============================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======== CONFIG ========
FILE_PATH = r"D:\Languages\Python-Library\All Method\cancer.csv"  # Change this to your dataset path
TARGET_COLUMN = None  # Set target column name if you have one (e.g., "diagnosis")
# =========================

# Display settings
pd.set_option("display.max_columns", None)
sns.set(style="whitegrid")

# 1️⃣ Load Data
print("Loading dataset...")
df = pd.read_csv(FILE_PATH)
print(f"\n✅ Dataset loaded successfully! Shape: {df.shape}")

# 2️⃣ Basic Info
print("\n--- Basic Info ---")
print(df.info())

# 3️⃣ First Rows
print("\n--- First 5 Rows ---")
print(df.head())

# 4️⃣ Missing Values
print("\n--- Missing Values ---")
print(df.isnull().sum())

# 5️⃣ Duplicates
print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())

# 6️⃣ Summary Statistics
print("\n--- Numeric Summary ---")
print(df.describe())

print("\n--- Categorical Summary ---")
print(df.describe(include='object'))

# 7️⃣ Data Types Count
print("\n--- Data Types Count ---")
print(df.dtypes.value_counts())

# 8️⃣ Univariate Plots
print("\nGenerating univariate plots...")
df.hist(figsize=(12, 8))
plt.suptitle("Feature Distributions")
plt.show()

# 9️⃣ Boxplots for Outliers
numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
if len(numeric_cols) > 0:
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[numeric_cols])
    plt.xticks(rotation=90)
    plt.title("Numeric Feature Outliers")
    plt.show()

# 🔟 Categorical Countplots
categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    plt.figure(figsize=(6, 4))
    sns.countplot(x=col, data=df)
    plt.title(f"Count Plot - {col}")
    plt.xticks(rotation=45)
    plt.show()

# 1️⃣1️⃣ Correlation Heatmap
if len(numeric_cols) > 1:
    plt.figure(figsize=(10, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
    plt.title("Correlation Heatmap")
    plt.show()

# 1️⃣2️⃣ Pairplot
if len(numeric_cols) <= 10:  # Avoids heavy plotting for very large datasets
    sns.pairplot(df, diag_kind="kde")
    plt.show()

print("\n🎯 EDA Completed Successfully!")
