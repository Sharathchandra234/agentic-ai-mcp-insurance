import os
import json
import sys

import faiss
import joblib
import pandas as pd

from sentence_transformers import SentenceTransformer
from mcp.server.mcpserver import MCPServer


# ============================================================
# MCP SERVER
# ============================================================

mcp = MCPServer("Insurance Agentic AI Server")


# ============================================================
# ML FRAUD MODEL
# ============================================================

FRAUD_MODEL_FILE = "fraud_model.pkl"

fraud_model = joblib.load(
    FRAUD_MODEL_FILE
)

FRAUD_FEATURES = [
    "claim_amount",
    "previous_claims",
    "policy_age",
    "vehicle_age",
    "claim_frequency",
    "repair_cost",
    "location_risk"
]


# ============================================================
# RAG CONFIGURATION
# ============================================================

VECTOR_DB_FOLDER = "vector_db"

INDEX_FILE = os.path.join(
    VECTOR_DB_FOLDER,
    "insurance_policies.index"
)

METADATA_FILE = os.path.join(
    VECTOR_DB_FOLDER,
    "metadata.json"
)

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# ============================================================
# LOAD RAG DATABASE
# ============================================================

print(
    "Loading RAG vector database...",
    file=sys.stderr
)

rag_index = faiss.read_index(
    INDEX_FILE
)

with open(
    METADATA_FILE,
    "r",
    encoding="utf-8"
) as file:

    rag_metadata = json.load(file)


print(
    f"RAG database loaded: {rag_index.ntotal} vectors",
    file=sys.stderr
)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print(
    "Loading embedding model...",
    file=sys.stderr
)

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

print(
    "Embedding model loaded.",
    file=sys.stderr
)


# ============================================================
# TOOL 1 — GET POLICY
# ============================================================

@mcp.tool()
def get_policy(
    policy_number: str
) -> dict:

    """Get insurance policy details using the policy number."""

    policies = {

        "POL1001": {

            "policy_number": "POL1001",

            "customer_id": "CUS001",

            "vehicle_id": "VEH001",

            "policy_type": "Auto Insurance",

            "status": "Active",

            "coverage": "Comprehensive",

            "premium": 18000,

            "policy_age": 4
        },

        "POL1002": {

            "policy_number": "POL1002",

            "customer_id": "CUS002",

            "vehicle_id": "VEH002",

            "policy_type": "Auto Insurance",

            "status": "Expired",

            "coverage": "Third Party",

            "premium": 12000,

            "policy_age": 6
        },

        "POL1003": {

            "policy_number": "POL1003",

            "customer_id": "CUS003",

            "vehicle_id": "VEH003",

            "policy_type": "Auto Insurance",

            "status": "Under Review",

            "coverage": "Comprehensive",

            "premium": 22000,

            "policy_age": 2
        }
    }

    return policies.get(
        policy_number,
        {
            "error": "Policy not found"
        }
    )


# ============================================================
# TOOL 2 — GET CLAIM
# ============================================================

@mcp.tool()
def get_claim(
    claim_id: str
) -> dict:

    """Get insurance claim details using the claim ID."""

    claims = {

        "CLM001": {

            "claim_id": "CLM001",

            "policy_number": "POL1001",

            "claim_amount": 85000,

            "claim_type": "Accident",

            "status": "Under Review",

            "repair_cost": 60000,

            "claim_frequency": 1,

            "location_risk": 1
        },

        "CLM002": {

            "claim_id": "CLM002",

            "policy_number": "POL1002",

            "claim_amount": 45000,

            "claim_type": "Theft",

            "status": "Rejected",

            "repair_cost": 30000,

            "claim_frequency": 3,

            "location_risk": 2
        }
    }

    return claims.get(
        claim_id,
        {
            "error": "Claim not found"
        }
    )


# ============================================================
# TOOL 3 — GET CUSTOMER
# ============================================================

@mcp.tool()
def get_customer(
    customer_id: str
) -> dict:

    """Get customer information using the customer ID."""

    customers = {

        "CUS001": {

            "customer_id": "CUS001",

            "name": "Customer One",

            "previous_claims": 1,

            "customer_since": 2022
        },

        "CUS002": {

            "customer_id": "CUS002",

            "name": "Customer Two",

            "previous_claims": 4,

            "customer_since": 2020
        },

        "CUS003": {

            "customer_id": "CUS003",

            "name": "Customer Three",

            "previous_claims": 2,

            "customer_since": 2024
        }
    }

    return customers.get(
        customer_id,
        {
            "error": "Customer not found"
        }
    )


# ============================================================
# TOOL 4 — CALCULATE RULE-BASED FRAUD SCORE
# ============================================================

@mcp.tool()
def calculate_fraud_score(
    claim_amount: float,
    previous_claims: int
) -> dict:

    """Calculate a simple demonstration fraud risk score."""

    score = 0

    if claim_amount > 100000:

        score += 50

    elif claim_amount > 50000:

        score += 30

    if previous_claims >= 5:

        score += 40

    elif previous_claims >= 3:

        score += 20

    if score >= 60:

        risk = "High"

    elif score >= 30:

        risk = "Medium"

    else:

        risk = "Low"

    return {

        "fraud_score": score,

        "risk_level": risk
    }


# ============================================================
# TOOL 5 — GET VEHICLE
# ============================================================

@mcp.tool()
def get_vehicle(
    vehicle_id: str
) -> dict:

    """Get vehicle information using the vehicle ID."""

    vehicles = {

        "VEH001": {

            "vehicle_id": "VEH001",

            "registration_number": "TS09AB1234",

            "make": "Toyota",

            "model": "Corolla",

            "year": 2021,

            "vehicle_type": "Car",

            "owner": "CUS001"
        },

        "VEH002": {

            "vehicle_id": "VEH002",

            "registration_number": "TS10CD5678",

            "make": "Hyundai",

            "model": "Creta",

            "year": 2019,

            "vehicle_type": "SUV",

            "owner": "CUS002"
        },

        "VEH003": {

            "vehicle_id": "VEH003",

            "registration_number": "TS11EF9012",

            "make": "Honda",

            "model": "City",

            "year": 2023,

            "vehicle_type": "Sedan",

            "owner": "CUS003"
        }
    }

    return vehicles.get(
        vehicle_id,
        {
            "error": "Vehicle not found"
        }
    )


# ============================================================
# TOOL 6 — ML FRAUD PREDICTION
# ============================================================

@mcp.tool()
def predict_fraud_risk(
    claim_amount: float,
    previous_claims: int,
    policy_age: int,
    vehicle_age: int,
    claim_frequency: int,
    repair_cost: float,
    location_risk: int
) -> dict:

    """Predict insurance fraud risk using the trained Random Forest model."""

    claim = {

        "claim_amount": claim_amount,

        "previous_claims": previous_claims,

        "policy_age": policy_age,

        "vehicle_age": vehicle_age,

        "claim_frequency": claim_frequency,

        "repair_cost": repair_cost,

        "location_risk": location_risk
    }

    X = pd.DataFrame(
        [claim],
        columns=FRAUD_FEATURES
    )

    prediction = int(
        fraud_model.predict(X)[0]
    )

    fraud_probability = float(
        fraud_model.predict_proba(X)[0][1]
    )

    if fraud_probability >= 0.70:

        risk_level = "High"

    elif fraud_probability >= 0.40:

        risk_level = "Medium"

    else:

        risk_level = "Low"

    return {

        "fraud_probability":
            round(
                fraud_probability,
                4
            ),

        "fraud_probability_percent":
            round(
                fraud_probability * 100,
                2
            ),

        "risk_level":
            risk_level,

        "prediction":
            "Fraud"
            if prediction == 1
            else "Not Fraud",

        "model":
            "Random Forest",

        "note":
            "Model trained on synthetic demonstration data. "
            "Prediction should support investigation and "
            "not be treated as a definitive fraud determination."
    }


# ============================================================
# TOOL 7 — RAG POLICY SEARCH
# ============================================================

@mcp.tool()
def search_policy_documents(
    query: str,
    top_k: int = 3
) -> dict:

    """
    Search insurance policy documents using
    semantic similarity.

    Only sufficiently relevant results are returned.
    """

    # ========================================================
    # VALIDATE INPUT
    # ========================================================

    if not query or not query.strip():

        return {
            "query": query,
            "results": [],
            "message": "Search query cannot be empty."
        }

    # Prevent excessively large retrieval requests.
    top_k = max(1, min(top_k, 5))

    # Minimum cosine similarity required for
    # a result to be considered relevant.
    SIMILARITY_THRESHOLD = 0.55

    # ========================================================
    # CREATE QUERY EMBEDDING
    # ========================================================

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    # ========================================================
    # NORMALIZE FOR COSINE SIMILARITY
    # ========================================================

    faiss.normalize_L2(
        query_embedding
    )

    # ========================================================
    # SEARCH FAISS
    # ========================================================

    similarities, indices = rag_index.search(
        query_embedding,
        top_k
    )

    results = []

    # ========================================================
    # FILTER BY RELEVANCE
    # ========================================================

    for similarity, index_id in zip(
        similarities[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        similarity = float(similarity)

        # Ignore weak matches.
        if similarity < SIMILARITY_THRESHOLD:
            continue

        chunk = rag_metadata[index_id]

        results.append({

            "filename":
                chunk["filename"],

            "chunk_id":
                chunk["chunk_id"],

            "cosine_similarity":
                round(
                    similarity,
                    4
                ),

            "text":
                chunk["text"]
        })

    # ========================================================
    # NO RELEVANT RESULTS
    # ========================================================

    if not results:

        return {

            "query":
                query,

            "results":
                [],

            "message":
                "No sufficiently relevant policy evidence "
                "was found for this query.",

            "similarity_threshold":
                SIMILARITY_THRESHOLD
        }

    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "query":
            query,

        "results":
            results,

        "similarity_threshold":
            SIMILARITY_THRESHOLD,

        "result_count":
            len(results)
    }

    """
    Search insurance policy documents using
    semantic similarity and return relevant sections.
    """

    # ========================================================
    # CREATE QUERY EMBEDDING
    # ========================================================

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    # ========================================================
    # NORMALIZE FOR COSINE SIMILARITY
    # ========================================================

    faiss.normalize_L2(
        query_embedding
    )

    # ========================================================
    # SEARCH VECTOR DATABASE
    # ========================================================

    similarities, indices = rag_index.search(
        query_embedding,
        top_k
    )

    results = []

    for similarity, index_id in zip(
        similarities[0],
        indices[0]
    ):

        if index_id == -1:
            continue

        chunk = rag_metadata[index_id]

        results.append({

            "filename":
                chunk["filename"],

            "chunk_id":
                chunk["chunk_id"],

            "cosine_similarity":
                round(
                    float(similarity),
                    4
                ),

            "text":
                chunk["text"]
        })

    return {

        "query":
            query,

        "results":
            results
    }


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":

    print(
        "\n==========================================",
        file=sys.stderr
    )

    print(
        "   INSURANCE AGENTIC AI MCP SERVER",
        file=sys.stderr
    )

    print(
        "==========================================",
        file=sys.stderr
    )

    print(
        "Tools available: 7",
        file=sys.stderr
    )

    print(
        "RAG: Enabled",
        file=sys.stderr
    )

    print(
        "ML Fraud Model: Enabled",
        file=sys.stderr
    )

    mcp.run()