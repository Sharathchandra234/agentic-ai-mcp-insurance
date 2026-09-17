import joblib
import pandas as pd


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

model = joblib.load("fraud_model.pkl")

print("Fraud model loaded successfully.")


# ============================================================
# 2. CREATE A CLAIM TO TEST
# ============================================================

claim = {
    "claim_amount": 85000,
    "previous_claims": 1,
    "policy_age": 4,
    "vehicle_age": 5,
    "claim_frequency": 1,
    "repair_cost": 60000,
    "location_risk": 1
}


# ============================================================
# 3. CONVERT CLAIM TO DATAFRAME
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

X = pd.DataFrame(
    [claim],
    columns=features
)


# ============================================================
# 4. PREDICT
# ============================================================

prediction = model.predict(X)[0]

fraud_probability = model.predict_proba(X)[0][1]


# ============================================================
# 5. DETERMINE RISK
# ============================================================

if fraud_probability >= 0.70:
    risk_level = "High"

elif fraud_probability >= 0.40:
    risk_level = "Medium"

else:
    risk_level = "Low"


# ============================================================
# 6. DISPLAY RESULT
# ============================================================

print("\n========== FRAUD PREDICTION ==========")

print(f"Claim Amount: ₹{claim['claim_amount']}")
print(f"Previous Claims: {claim['previous_claims']}")
print(f"Policy Age: {claim['policy_age']} years")
print(f"Vehicle Age: {claim['vehicle_age']} years")
print(f"Claim Frequency: {claim['claim_frequency']}")
print(f"Repair Cost: ₹{claim['repair_cost']}")
print(f"Location Risk: {claim['location_risk']}")

print("\n========== MODEL RESULT ==========")

print(
    f"Fraud Probability: {fraud_probability:.2%}"
)

print(
    f"Risk Level: {risk_level}"
)

print(
    f"Predicted Class: {'Fraud' if prediction == 1 else 'Not Fraud'}"
)