from neo4j_client import run_query


def get_claim_network(claim_id: str):
    """
    Get the connected entities for a claim:
    Claim -> Policy
    Claim -> Customer
    Claim -> Vehicle
    """

    query = """
    MATCH (claim:Claim {claim_id: $claim_id})

    OPTIONAL MATCH (policy:Policy)-[:HAS_CLAIM]->(claim)

    OPTIONAL MATCH (claim)-[:FILED_BY]->(customer:Customer)

    OPTIONAL MATCH (claim)-[:INVOLVES_VEHICLE]->(vehicle:Vehicle)

    RETURN
        claim.claim_id AS claim_id,
        claim.claim_type AS claim_type,
        claim.claim_amount AS claim_amount,
        claim.status AS claim_status,

        policy.policy_number AS policy_number,
        policy.policy_type AS policy_type,
        policy.coverage AS coverage,
        policy.status AS policy_status,

        customer.customer_id AS customer_id,
        customer.name AS customer_name,

        vehicle.vehicle_id AS vehicle_id,
        vehicle.registration_number AS registration_number,
        vehicle.make AS vehicle_make,
        vehicle.model AS vehicle_model,
        vehicle.vehicle_type AS vehicle_type
    """

    return run_query(query, {"claim_id": claim_id})


def get_customer_claims(customer_id: str):
    """
    Find policies and claims belonging to a customer.
    """

    query = """
    MATCH (customer:Customer {customer_id: $customer_id})

    OPTIONAL MATCH (customer)-[:OWNS_POLICY]->(policy:Policy)

    OPTIONAL MATCH (policy)-[:HAS_CLAIM]->(claim:Claim)

    RETURN
        customer.customer_id AS customer_id,
        customer.name AS customer_name,

        policy.policy_number AS policy_number,
        policy.policy_type AS policy_type,
        policy.status AS policy_status,

        claim.claim_id AS claim_id,
        claim.claim_type AS claim_type,
        claim.claim_amount AS claim_amount,
        claim.status AS claim_status

    ORDER BY claim.claim_id
    """

    return run_query(query, {"customer_id": customer_id})


def get_vehicle_claims(vehicle_id: str):
    """
    Find claims involving a vehicle.
    """

    query = """
    MATCH (vehicle:Vehicle {vehicle_id: $vehicle_id})

    OPTIONAL MATCH (claim:Claim)-[:INVOLVES_VEHICLE]->(vehicle)

    OPTIONAL MATCH (claim)-[:FILED_BY]->(customer:Customer)

    RETURN
        vehicle.vehicle_id AS vehicle_id,
        vehicle.registration_number AS registration_number,
        vehicle.make AS vehicle_make,
        vehicle.model AS vehicle_model,
        vehicle.vehicle_type AS vehicle_type,

        claim.claim_id AS claim_id,
        claim.claim_type AS claim_type,
        claim.claim_amount AS claim_amount,
        claim.status AS claim_status,

        customer.customer_id AS customer_id,
        customer.name AS customer_name

    ORDER BY claim.claim_id
    """ 

    return run_query(query, {"vehicle_id": vehicle_id})


if __name__ == "__main__":

    print("\n--- CLAIM NETWORK: CLM001 ---")

    result = get_claim_network("CLM001")

    for row in result:
        print(row)

    print("\n--- CUSTOMER CLAIMS: CUS001 ---")

    result = get_customer_claims("CUS001")

    for row in result:
        print(row)

    print("\n--- VEHICLE CLAIMS: VEH001 ---")

    result = get_vehicle_claims("VEH001")

    for row in result:
        print(row)