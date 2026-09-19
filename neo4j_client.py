import os

from neo4j import GraphDatabase


# ============================================================
# NEO4J CONFIGURATION
# ============================================================

NEO4J_URI = os.getenv(
    "NEO4J_URI",
    "bolt://localhost:7687"
)

NEO4J_USERNAME = os.getenv(
    "NEO4J_USERNAME",
    "neo4j"
)

NEO4J_PASSWORD = os.getenv(
    "NEO4J_PASSWORD",
    "insurance123"
)

NEO4J_DATABASE = os.getenv(
    "NEO4J_DATABASE",
    "neo4j"
)


# ============================================================
# NEO4J DRIVER
# ============================================================

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(
        NEO4J_USERNAME,
        NEO4J_PASSWORD
    )
)


# ============================================================
# CONNECTION TEST
# ============================================================

def verify_connection():

    driver.verify_connectivity()

    print(
        "Neo4j connection successful."
    )


# ============================================================
# RUN CYPHER QUERY
# ============================================================

def run_query(
    query,
    parameters=None
):

    records, summary, keys = driver.execute_query(
        query,
        parameters_=parameters or {},
        database_=NEO4J_DATABASE
    )

    return [
        record.data()
        for record in records
    ]


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    verify_connection()

    result = run_query(
        """
        RETURN
            "Python connected to Neo4j successfully!" AS message
        """
    )

    print(result)