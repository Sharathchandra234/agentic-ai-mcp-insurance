from neo4j import GraphDatabase


# ============================================================
# NEO4J CONFIGURATION
# ============================================================

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "insurance123"
DATABASE = "neo4j"


# ============================================================
# EXISTING INSURANCE DATA
# Taken from the current MCP server
# ============================================================

POLICIES = {

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


CLAIMS = {

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


CUSTOMERS = {

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


VEHICLES = {

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


# ============================================================
# CREATE NEO4J DRIVER
# ============================================================

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


# ============================================================
# LOAD DATA
# ============================================================

def load_graph():

    with driver.session(database=DATABASE) as session:

        # ----------------------------------------------------
        # CREATE CUSTOMERS
        # ----------------------------------------------------

        for customer in CUSTOMERS.values():

            session.run(
                """
                MERGE (c:Customer {
                    customer_id: $customer_id
                })

                SET
                    c.name = $name,
                    c.previous_claims = $previous_claims,
                    c.customer_since = $customer_since
                """,

                customer_id=customer["customer_id"],
                name=customer["name"],
                previous_claims=customer["previous_claims"],
                customer_since=customer["customer_since"]
            )


        # ----------------------------------------------------
        # CREATE VEHICLES
        # ----------------------------------------------------

        for vehicle in VEHICLES.values():

            session.run(
                """
                MERGE (v:Vehicle {
                    vehicle_id: $vehicle_id
                })

                SET
                    v.registration_number = $registration_number,
                    v.make = $make,
                    v.model = $model,
                    v.year = $year,
                    v.vehicle_type = $vehicle_type
                """,

                vehicle_id=vehicle["vehicle_id"],
                registration_number=vehicle["registration_number"],
                make=vehicle["make"],
                model=vehicle["model"],
                year=vehicle["year"],
                vehicle_type=vehicle["vehicle_type"]
            )


        # ----------------------------------------------------
        # CREATE POLICIES
        # ----------------------------------------------------

        for policy in POLICIES.values():

            session.run(
                """
                MERGE (p:Policy {
                    policy_number: $policy_number
                })

                SET
                    p.policy_type = $policy_type,
                    p.status = $status,
                    p.coverage = $coverage,
                    p.premium = $premium,
                    p.policy_age = $policy_age
                """,

                policy_number=policy["policy_number"],
                policy_type=policy["policy_type"],
                status=policy["status"],
                coverage=policy["coverage"],
                premium=policy["premium"],
                policy_age=policy["policy_age"]
            )


        # ----------------------------------------------------
        # CREATE CLAIMS
        # ----------------------------------------------------

        for claim in CLAIMS.values():

            session.run(
                """
                MERGE (cl:Claim {
                    claim_id: $claim_id
                })

                SET
                    cl.claim_amount = $claim_amount,
                    cl.claim_type = $claim_type,
                    cl.status = $status,
                    cl.repair_cost = $repair_cost,
                    cl.claim_frequency = $claim_frequency,
                    cl.location_risk = $location_risk
                """,

                claim_id=claim["claim_id"],
                claim_amount=claim["claim_amount"],
                claim_type=claim["claim_type"],
                status=claim["status"],
                repair_cost=claim["repair_cost"],
                claim_frequency=claim["claim_frequency"],
                location_risk=claim["location_risk"]
            )


        # ----------------------------------------------------
        # CUSTOMER → POLICY
        # ----------------------------------------------------

        for policy in POLICIES.values():

            session.run(
                """
                MATCH (c:Customer {
                    customer_id: $customer_id
                })

                MATCH (p:Policy {
                    policy_number: $policy_number
                })

                MERGE (c)-[:OWNS_POLICY]->(p)
                """,

                customer_id=policy["customer_id"],
                policy_number=policy["policy_number"]
            )


        # ----------------------------------------------------
        # CUSTOMER → VEHICLE
        # ----------------------------------------------------

        for vehicle in VEHICLES.values():

            session.run(
                """
                MATCH (c:Customer {
                    customer_id: $customer_id
                })

                MATCH (v:Vehicle {
                    vehicle_id: $vehicle_id
                })

                MERGE (c)-[:OWNS_VEHICLE]->(v)
                """,

                customer_id=vehicle["owner"],
                vehicle_id=vehicle["vehicle_id"]
            )


        # ----------------------------------------------------
        # POLICY → CLAIM
        # ----------------------------------------------------

        for claim in CLAIMS.values():

            session.run(
                """
                MATCH (p:Policy {
                    policy_number: $policy_number
                })

                MATCH (cl:Claim {
                    claim_id: $claim_id
                })

                MERGE (p)-[:HAS_CLAIM]->(cl)
                """,

                policy_number=claim["policy_number"],
                claim_id=claim["claim_id"]
            )


        # ----------------------------------------------------
        # CLAIM → CUSTOMER
        # ----------------------------------------------------

        for claim in CLAIMS.values():

            policy = POLICIES[
                claim["policy_number"]
            ]

            session.run(
                """
                MATCH (cl:Claim {
                    claim_id: $claim_id
                })

                MATCH (c:Customer {
                    customer_id: $customer_id
                })

                MERGE (cl)-[:FILED_BY]->(c)
                """,

                claim_id=claim["claim_id"],
                customer_id=policy["customer_id"]
            )


        # ----------------------------------------------------
        # CLAIM → VEHICLE
        # ----------------------------------------------------

        for claim in CLAIMS.values():

            policy = POLICIES[
                claim["policy_number"]
            ]

            session.run(
                """
                MATCH (cl:Claim {
                    claim_id: $claim_id
                })

                MATCH (v:Vehicle {
                    vehicle_id: $vehicle_id
                })

                MERGE (cl)-[:INVOLVES_VEHICLE]->(v)
                """,

                claim_id=claim["claim_id"],
                vehicle_id=policy["vehicle_id"]
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("Loading insurance data into Neo4j...")

    load_graph()

    print("Insurance data successfully loaded into Neo4j.")

    driver.close()