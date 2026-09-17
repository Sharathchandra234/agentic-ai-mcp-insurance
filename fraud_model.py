import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score
)

import joblib


# ============================================================
# 1. CREATE SYNTHETIC INSURANCE CLAIM DATA
# ============================================================

np.random.seed(42)

NUMBER_OF_CLAIMS = 1000

data = {
    "claim_amount": np.random.randint(
        10000,
        300000,
        NUMBER_OF_CLAIMS
    ),

    "previous_claims": np.random.randint(
        0,
        8,
        NUMBER_OF_CLAIMS
    ),

    "policy_age": np.random.randint(
        1,
        15,
        NUMBER_OF_CLAIMS
    ),

    "vehicle_age": np.random.randint(
        1,
        15,
        NUMBER_OF_CLAIMS
    ),

    "claim_frequency": np.random.randint(
        0,
        6,
        NUMBER_OF_CLAIMS
    ),

    "repair_cost": np.random.randint(
        5000,
        250000,
        NUMBER_OF_CLAIMS
    ),

    "location_risk": np.random.randint(
        0,
        5,
        NUMBER_OF_CLAIMS
    )
}


df = pd.DataFrame(data)


# ============================================================
# 2. CREATE DEMONSTRATION FRAUD LABEL
# ============================================================

fraud_score = (
    (df["claim_amount"] > 180000).astype(int) * 2
    + (df["previous_claims"] >= 4).astype(int) * 2
    + (df["claim_frequency"] >= 3).astype(int) * 2
    + (df["vehicle_age"] >= 10).astype(int)
    + (df["location_risk"] >= 3).astype(int)
    + (
        df["repair_cost"] > df["claim_amount"] * 0.8
    ).astype(int) * 2
)


df["fraud"] = (
    fraud_score >= 5
).astype(int)


# ============================================================
# 3. DISPLAY DATASET INFORMATION
# ============================================================

print("\n========== DATASET ==========\n")

print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nFraud distribution:")
print(df["fraud"].value_counts())


# ============================================================
# 4. FEATURES AND TARGET
# ============================================================

features = [
    "claim_amount",
    "previous_claims",
    "policy_age",
    "vehicle_age",
    "claim_frequency",
    "repair_cost",
    "location_risk"
]

X = df[features]

y = df["fraud"]


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\n========== TRAINING DATA ==========")

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 6. TRAIN RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


print("\n========== TRAINING MODEL ==========\n")

model.fit(
    X_train,
    y_train
)

print("Model training completed.")


# ============================================================
# 7. PREDICTIONS
# ============================================================

y_pred = model.predict(X_test)

y_probability = model.predict_proba(X_test)[:, 1]


# ============================================================
# 8. MODEL EVALUATION
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

roc_auc = roc_auc_score(
    y_test,
    y_probability
)


print("\n========== MODEL PERFORMANCE ==========\n")

print(
    f"Accuracy: {accuracy:.4f}"
)

print(
    f"ROC-AUC: {roc_auc:.4f}"
)


print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        y_pred
    )
)


print("\nConfusion Matrix:\n")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# 9. FEATURE IMPORTANCE
# ============================================================

feature_importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})


feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)


print("\n========== FEATURE IMPORTANCE ==========\n")

print(feature_importance)


# ============================================================
# 10. SAVE MODEL
# ============================================================

joblib.dump(
    model,
    "fraud_model.pkl"
)


print("\n========== MODEL SAVED ==========\n")

print("Saved as: fraud_model.pkl")