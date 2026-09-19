# 🚗 Agentic AI Insurance Claims Investigation System

An end-to-end Agentic AI insurance claims investigation system that combines Google Gemini, Model Context Protocol (MCP), Retrieval-Augmented Generation (RAG), Machine Learning, and Neo4j Knowledge Graphs to investigate automobile insurance claims.

The system allows an AI agent to dynamically use MCP tools to retrieve claim, policy, customer, and vehicle information, perform ML-based fraud-risk prediction, retrieve relevant insurance policy evidence through semantic search, and analyze relationships between insurance entities using a Neo4j Knowledge Graph.

> Note: This project is an educational/demo system using synthetic insurance data. The ML model, policy documents, and insurance records are not intended for real-world insurance decisions.

---

## 🚀 Project Overview

Insurance claims investigation often requires information from multiple systems:

- Claim records
- Insurance policies
- Customer history
- Vehicle information
- Fraud-risk analysis
- Policy documents and coverage conditions
- Relationships between claims, customers, policies, and vehicles

This project demonstrates how an Agentic AI architecture can coordinate these different capabilities through MCP tools, RAG, ML, and a Knowledge Graph.

Instead of hard-coding a fixed workflow, the Gemini-based agent determines which tools are required based on the user's request and uses their results to build an investigation report.

### Example

A user can ask:

Investigate claim CLM001 completely. Check the claim, policy, customer, vehicle, use the ML fraud model, search the policy documents, and analyze the relationships in the knowledge graph.

The agent can dynamically perform a workflow such as:

User Request
     |
     v
Gemini Agent
     |
     +----> get_claim
     |
     +----> get_policy
     |
     +----> get_customer
     |
     +----> get_vehicle
     |
     +----> query_knowledge_graph
     |
     +----> predict_fraud_risk
     |
     +----> search_policy_documents
                    |
                    v
             Policy Evidence
                    |
                    v
             Gemini Reasoning
                    |
                    v
          Investigation Report

---

# 🏗️ System Architecture

                         +---------------------+
                         |        User         |
                         +----------+----------+
                                    |
                                    v
                         +---------------------+
                         |    Gemini Agent     |
                         |  Agentic Reasoning  |
                         +----------+----------+
                                    |
                   +----------------+-------------------+
                   |                |                   |
                   v                v                   v
             MCP Tools         ML Model               RAG
                   |                |                   |
                   v                v                   v
          Insurance Data     Fraud Prediction     FAISS Search
                   |                                    |
                   |                                    v
                   |                            Policy Evidence
                   |
                   v
          Neo4j Knowledge Graph
                   |
        +----------+-----------+
        |          |           |
        v          v           v
     Customer    Policy      Vehicle
        |          |           |
        |          v           |
        |        Claim         |
        |          ^           |
        +----------+-----------+
                   |
                   v
          Evidence + Reasoning
                   |
                   v
          Investigation Report

---

# 🤖 Agentic AI

The project uses Google Gemini as the reasoning engine.

The agent is instructed to:

- Understand the user's investigation request.
- Identify the required information.
- Dynamically select appropriate MCP tools.
- Follow relationships between insurance records.
- Query the Neo4j Knowledge Graph when relationship analysis is required.
- Execute MCP tools.
- Analyze ML fraud-risk information.
- Search policy documents using RAG.
- Distinguish facts from policy evidence and interpretation.
- Generate a structured investigation report.

The agent is not limited to a single hard-coded sequence.

Gemini can decide which available tools are required based on the user's request.

---

# 🔌 Model Context Protocol (MCP)

The project uses Model Context Protocol (MCP) to expose insurance capabilities as tools that can be dynamically discovered and called by the AI agent.

The MCP server currently exposes 8 tools.

## Available MCP Tools

Tool                         Purpose

get_claim                    Retrieves insurance claim information

get_policy                   Retrieves policy information

get_customer                 Retrieves customer information

get_vehicle                  Retrieves vehicle information

calculate_fraud_score        Performs rule-based fraud scoring

predict_fraud_risk           Performs ML-based fraud-risk prediction

search_policy_documents      Performs semantic search over policy documents

query_knowledge_graph        Queries Neo4j relationships between insurance entities

---

# 🧠 Neo4j Knowledge Graph

The system includes a Neo4j-based Knowledge Graph to provide relationship-aware insurance investigation.

Traditional lookup tools retrieve individual records.

The Knowledge Graph allows the agent to traverse relationships between:

- Customers
- Policies
- Claims
- Vehicles

## Graph Schema

Customer
   |
   +---- OWNS_POLICY ------> Policy
   |                            |
   |                            +---- HAS_CLAIM ----> Claim
   |
   +---- OWNS_VEHICLE -----> Vehicle

Claim
   |
   +---- FILED_BY ---------> Customer
   |
   +---- INVOLVES_VEHICLE -> Vehicle

### Nodes

(:Customer)

(:Policy)

(:Claim)

(:Vehicle)

### Relationships

(:Customer)-[:OWNS_POLICY]->(:Policy)

(:Customer)-[:OWNS_VEHICLE]->(:Vehicle)

(:Policy)-[:HAS_CLAIM]->(:Claim)

(:Claim)-[:FILED_BY]->(:Customer)

(:Claim)-[:INVOLVES_VEHICLE]->(:Vehicle)

---

# 🔎 Knowledge Graph Operations

The MCP Knowledge Graph tool supports three operations.

## 1. Claim Network

Operation:

claim_network

Used to investigate the entities directly connected to a claim.

Example:

query_knowledge_graph(
    operation="claim_network",
    entity_id="CLM001"
)

Example relationship:

CLM001
  |
  +---- Policy: POL1001
  |
  +---- Customer: CUS001
  |
  +---- Vehicle: VEH001

---

## 2. Customer Claims

Operation:

customer_claims

Used to investigate policies and claims associated with a customer.

Example:

query_knowledge_graph(
    operation="customer_claims",
    entity_id="CUS001"
)

---

## 3. Vehicle Claims

Operation:

vehicle_claims

Used to investigate claims and customers associated with a vehicle.

Example:

query_knowledge_graph(
    operation="vehicle_claims",
    entity_id="VEH001"
)

---

# 🧩 Why Use a Knowledge Graph?

Individual database-style tools are useful for retrieving specific records.

For example:

get_claim("CLM001")

can return claim information.

However, relationship questions require connecting multiple entities.

The Knowledge Graph provides a structured way to represent and traverse these relationships.

Examples include:

- Which policy is connected to a claim?
- Which customer filed the claim?
- Which vehicle is involved?
- Which claims are associated with a customer?
- Which claims are associated with a vehicle?
- Are there additional connected entities in the available graph?

The AI agent can combine:

Structured MCP Data
        +
Neo4j Relationships
        +
ML Prediction
        +
Policy RAG
        +
Gemini Reasoning

to produce a more complete investigation.

The current graph contains the synthetic entities and relationships loaded by neo4j_loader.py. The system does not infer or invent relationships that are not present in the graph.

---

# 🔄 Claim Investigation Workflow

The agent can follow relationships between insurance records.

Traditional record workflow:

Claim
  |
  | policy_number
  v
Policy
  |
  | customer_id
  v
Customer
  |
  | vehicle_id
  v
Vehicle

The Knowledge Graph provides an additional relationship layer:

                    +--------------+
                    |   Customer   |
                    +------+-------+
                           |
                      OWNS_POLICY
                           |
                           v
                    +--------------+
                    |    Policy    |
                    +------+-------+
                           |
                       HAS_CLAIM
                           |
                           v
                    +--------------+
                    |    Claim     |
                    +------+-------+
                           |
                  INVOLVES_VEHICLE
                           |
                           v
                    +--------------+
                    |   Vehicle    |
                    +--------------+

For example:

get_claim
    |
    v
policy_number
    |
    v
get_policy
    |
    +-----------------> customer_id
    |                       |
    |                       v
    |                 get_customer
    |
    +-----------------> vehicle_id
                            |
                            v
                       get_vehicle

The agent can additionally query:

query_knowledge_graph

to verify and analyze relationships between these entities.

---

# 📚 Retrieval-Augmented Generation (RAG)

The project includes a semantic search pipeline for insurance policy documents.

## RAG Pipeline

Policy Documents
      |
      v
Document Chunking
      |
      v
Sentence Transformers
      |
      v
Text Embeddings
      |
      v
FAISS Vector Index
      |
      v
Semantic Search
      |
      v
Relevant Policy Evidence
      |
      v
Gemini Agent

## Embedding Model

all-MiniLM-L6-v2

## Vector Database

FAISS

The embeddings are normalized and searched using cosine similarity through a FAISS inner-product index.

---

# 📄 Policy Documents

The project currently contains synthetic insurance policy documents covering areas such as:

- Comprehensive automobile insurance
- Third-party insurance
- Claims guidelines
- Fraud investigation guidelines

The documents are stored in:

policies/

The vector database is stored in:

vector_db/

---

# 🧠 Machine Learning Fraud-Risk Model

The project includes a Random Forest-based fraud-risk prediction model.

## Features

The model uses features including:

claim_amount
previous_claims
policy_age
vehicle_age
claim_frequency
repair_cost
location_risk

## Model

RandomForestClassifier

The model was trained using synthetic insurance claim data for demonstration purposes.

## Demonstration Results

The model training experiment achieved approximately:

Accuracy: 93.50%

ROC-AUC: 0.9807

These results should not be interpreted as real-world insurance fraud detection performance because the training dataset is synthetic.

---

# 🛡️ Fraud Risk Interpretation

The ML output is treated as an investigation-support signal.

The system does not use the prediction as proof of fraud.

Example:

Fraud Probability: 1%

Risk Level: Low

Prediction: Not Fraud

The model explicitly provides a warning that its prediction is based on synthetic demonstration data.

The final insurance decision should remain subject to appropriate human review and business processes.

---

# 📊 Rule-Based Fraud Scoring

The project also includes a simpler rule-based fraud scoring tool:

calculate_fraud_score

This demonstrates how traditional business rules can coexist with ML-based predictions within an Agentic AI system.

---

# 🔎 Policy Evidence and Reasoning

The agent is instructed to separate information into three categories.

## FACTS

Information directly returned by MCP tools.

Examples:

- Claim amount
- Policy status
- Customer ID
- Vehicle ID
- ML prediction
- Knowledge Graph relationships

## POLICY EVIDENCE

Information retrieved from insurance policy documents through RAG.

Examples:

- Coverage
- Exclusions
- Deductibles
- Claim procedures
- Policy conditions

## INTERPRETATION

Reasoning performed by the AI agent using the available facts and policy evidence.

This separation helps reduce unsupported assumptions and makes the investigation easier to review.

---

# 📋 Final Investigation Report

For a complete investigation, the agent generates a structured report containing:

1. Claim Summary
2. Policy Verification
3. Customer Information
4. Vehicle Information
5. Knowledge Graph Analysis
6. ML Fraud Assessment
7. Policy Coverage Analysis
8. Key Risk Indicators
9. Recommended Next Investigation Steps
10. Human Review Recommendation

---

# 🧪 End-to-End Example

Example claim:

Claim ID: CLM001

Policy ID: POL1001

Customer ID: CUS001

Vehicle ID: VEH001

Claim Type: Accident

Claim Amount: ₹85,000

Repair Cost: ₹60,000

Claim Status: Under Review

The Gemini agent can dynamically execute tools such as:

1. get_claim
2. get_policy
3. query_knowledge_graph
4. get_customer
5. get_vehicle
6. predict_fraud_risk
7. search_policy_documents

The Knowledge Graph can return:

CLM001
   |
   +---- POL1001
   |
   +---- CUS001
   |
   +---- VEH001

The ML model can return:

Fraud Probability: 1.0%

Risk Level: Low

Prediction: Not Fraud

The RAG system can retrieve relevant policy evidence for:

- Accidental Damage Coverage
- Deductibles
- Policy Verification
- Claim Decision Procedures

Gemini then combines the evidence into a structured investigation report.

---

# 🧪 Verified MCP + Neo4j Integration

The Knowledge Graph integration has been tested through the MCP client.

Verified operations:

claim_network

customer_claims

vehicle_claims

Example:

query_knowledge_graph
        |
        v
      MCP
        |
        v
graph_queries.py
        |
        v
neo4j_client.py
        |
        v
      Neo4j

The complete Gemini agent has also been tested successfully with the Knowledge Graph MCP tool.

The agent dynamically discovered all 8 MCP tools and used the Knowledge Graph during an end-to-end insurance claim investigation.

---

# 🗄️ Neo4j Setup

The Knowledge Graph uses Neo4j.

The project can be run locally using Docker.

## Start Neo4j

Example Docker command:

docker run -d `
  --name insurance-neo4j `
  -p 7474:7474 `
  -p 7687:7687 `
  -e NEO4J_AUTH=neo4j/insurance123 `
  -v neo4j_data:/data `
  neo4j:latest

Neo4j Browser:

http://localhost:7474

Default development credentials used by this project:

Username: neo4j

Password: insurance123

For production environments, use secure credentials and proper secret management. Do not use the development password shown above.

---

# 🔌 Neo4j Python Connection

The project uses the official Neo4j Python driver.

Install:

pip install neo4j

The connection is implemented in:

neo4j_client.py

The file supports environment variables:

NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
NEO4J_DATABASE

Default local development configuration:

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=insurance123
NEO4J_DATABASE=neo4j

---

# 📥 Loading Insurance Data into Neo4j

The synthetic insurance data can be loaded into Neo4j using:

python neo4j_loader.py

The loader creates:

- Customer nodes
- Policy nodes
- Claim nodes
- Vehicle nodes

and their relationships.

---

# 🧪 Testing the Knowledge Graph

Test the Neo4j Python connection:

python neo4j_client.py

Test graph queries directly:

python graph_queries.py

Test the Knowledge Graph through MCP:

python neo4j_mcp_test.py

The MCP test can verify:

- claim_network
- customer_claims
- vehicle_claims

---

# 🛠️ Technology Stack

## Programming

- Python 3.11

## Generative AI

- Google Gemini
- Google GenAI Python SDK

## Agentic AI

- Model Context Protocol (MCP)
- MCP Python SDK
- Dynamic tool discovery
- Function/tool calling

## Knowledge Graph

- Neo4j
- Neo4j Python Driver
- Cypher
- Graph-based relationship traversal

## Machine Learning

- Scikit-learn
- Random Forest
- Pandas
- NumPy

## RAG

- Sentence Transformers
- FAISS
- Semantic Search
- Vector Embeddings

## Development

- Python virtual environment
- PowerShell
- Docker
- Git
- GitHub

---

# 📁 Project Structure

agentic-ai-mcp-insurance/
|
├── agent.py
│   └── Gemini Agent + MCP orchestration
|
├── server.py
│   └── MCP server and insurance tools
|
├── client.py
│   └── MCP client
|
├── tool_test.py
│   └── MCP tool testing
|
├── gemini_test.py
│   └── Gemini API testing
|
├── fraud_model.py
│   └── Synthetic dataset generation and model training
|
├── fraud_predict.py
│   └── Fraud prediction testing
|
├── fraud_model.pkl
│   └── Trained Random Forest model
|
├── rag_ingest.py
│   └── Policy document ingestion and vector indexing
|
├── rag_search.py
│   └── Semantic policy search
|
├── neo4j_client.py
│   └── Neo4j database connection and query execution
|
├── neo4j_loader.py
│   └── Loads synthetic insurance data into Neo4j
|
├── graph_queries.py
│   └── Cypher-based Knowledge Graph queries
|
├── neo4j_mcp_test.py
│   └── Tests Neo4j Knowledge Graph through MCP
|
├── policies/
│   ├── auto_comprehensive_policy.txt
│   ├── auto_third_party_policy.txt
│   ├── claims_guidelines.txt
│   └── fraud_investigation_guidelines.txt
|
├── vector_db/
│   ├── insurance_policies.index
│   └── metadata.json
|
├── requirements.txt
|
├── .gitignore
|
└── README.md

---

# ⚙️ Installation

## 1. Clone the repository

git clone https://github.com/Sharathchandra234/agentic-ai-mcp-insurance.git

Move into the project:

cd agentic-ai-mcp-insurance

## 2. Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\Activate.ps1

## 3. Install dependencies

pip install -r requirements.txt

If Neo4j is not included in the requirements file:

pip install neo4j

---

# 🔑 Gemini API Configuration

The project requires a Gemini API key.

Set the API key as an environment variable.

### Windows PowerShell

$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

Do not commit your API key to GitHub.

The .gitignore file is configured to ignore environment files and other local configuration files.

---

# 🔐 Neo4j Configuration

For local development, the project uses:

NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=insurance123
NEO4J_DATABASE=neo4j

For better security, these values can be provided through environment variables.

Example:

$env:NEO4J_URI="bolt://localhost:7687"
$env:NEO4J_USERNAME="neo4j"
$env:NEO4J_PASSWORD="YOUR_NEO4J_PASSWORD"
$env:NEO4J_DATABASE="neo4j"

---

# ▶️ Running the Project

After activating the virtual environment, starting Neo4j, and setting the Gemini API key:

python agent.py

The application will:

1. Start the MCP server.
2. Discover the available MCP tools.
3. Expose all 8 tools to Gemini.
4. Accept an insurance investigation request.
5. Dynamically call required tools.
6. Query Neo4j when relationship analysis is needed.
7. Use ML fraud prediction when appropriate.
8. Search policy documents using RAG.
9. Generate a structured investigation report.

---

# 💬 Example User Request

Investigate claim CLM001. Analyze the claim, its policy, customer, vehicle, ML fraud risk, relevant policy coverage, and the relationships available in the knowledge graph.

The agent can dynamically determine which tools are necessary.

---

# 🧪 Testing Individual Components

## Test Gemini

python gemini_test.py

## Test MCP tools

python tool_test.py

## Test fraud model

python fraud_model.py

## Test fraud prediction

python fraud_predict.py

## Test RAG search

python rag_search.py

## Test Neo4j connection

python neo4j_client.py

## Test Neo4j graph queries

python graph_queries.py

## Test Neo4j through MCP

python neo4j_mcp_test.py

---

# 🔬 Example Investigation

Example claim:

Claim ID: CLM001

Policy ID: POL1001

Customer ID: CUS001

Vehicle ID: VEH001

Claim Type: Accident

Claim Amount: ₹85,000

Repair Cost: ₹60,000

Claim Status: Under Review

The agent can retrieve:

Claim
  ↓
Policy
  ↓
Customer
  ↓
Vehicle
  ↓
Knowledge Graph Relationships
  ↓
ML Fraud Risk
  ↓
Policy Coverage Evidence

The final response combines the retrieved information into a structured investigation report.

---

# 🔐 Security Considerations

Never commit:

.env

API keys

passwords

credentials

private certificates

The project .gitignore excludes common local secrets and development artifacts.

Before pushing changes to GitHub, always check:

git status

Also verify that sensitive files are not staged:

git status

---

# ⚠️ Disclaimer

This project is intended for educational, portfolio, and technical demonstration purposes.

The insurance records and ML training data are synthetic.

The fraud model should not be used to make real insurance fraud determinations.

The policy documents included in this repository are demonstration documents and should not be interpreted as actual insurance contracts.

The Neo4j Knowledge Graph contains synthetic demonstration relationships and should not be treated as a production insurance database.

Production deployment would require:

- Real insurance data governance
- Model validation
- Security controls
- Authentication and authorization
- Audit logging
- Human oversight
- Regulatory compliance
- Production-grade policy sources
- Monitoring and evaluation

---

# 🔮 Future Improvements

Potential future extensions include:

- FastAPI backend
- REST API for claim investigation
- Web-based dashboard
- Authentication and role-based access
- PostgreSQL / MongoDB integration
- Production vector database
- Advanced RAG evaluation
- RAG citations and source highlighting
- LLM observability
- MLflow model tracking
- Model monitoring
- Human-in-the-loop claim review
- Docker deployment
- Kubernetes deployment
- Cloud deployment
- Automated evaluation pipelines
- Multi-agent insurance workflows
- MCP authentication and authorization
- Production insurance data integration
- Advanced Neo4j graph analytics
- Graph-based fraud pattern detection
- Fraud-ring relationship analysis
- Graph + vector hybrid retrieval
- Knowledge Graph visualization

---

# 🎯 Key Learning Outcomes

This project demonstrates practical implementation of:

## Agentic AI

- Agentic AI
- LLM tool calling
- Dynamic tool selection
- Tool orchestration
- AI-assisted insurance investigation

## Model Context Protocol

- Model Context Protocol
- MCP server/client architecture
- Dynamic tool discovery
- MCP function calling
- MCP-based tool orchestration

## Knowledge Graphs

- Neo4j
- Graph data modeling
- Cypher queries
- Entity relationships
- Relationship-aware AI investigation
- Knowledge Graph + MCP integration

## Retrieval-Augmented Generation

- Retrieval-Augmented Generation
- Vector databases
- Semantic search
- Sentence embeddings
- FAISS

## Machine Learning

- Random Forest
- Fraud-risk prediction
- Synthetic dataset generation
- ML inference

## AI Safety and Grounded Reasoning

- Grounded reasoning
- Evidence-based responses
- Separation of facts and interpretation
- Human-in-the-loop decision making
- Avoiding unsupported insurance decisions

---

# 🏆 Project Highlights

This project demonstrates an integrated Agentic AI architecture combining:

                  Gemini
                    |
                    v
             Agentic Reasoning
                    |
                    v
                   MCP
                    |
       +------------+-------------+
       |            |             |
       v            v             v
     Tools          ML            RAG
       |            |             |
       |            |             v
       |            |           FAISS
       |            |             |
       |            |             v
       |            |       Policy Evidence
       |
       v
     Neo4j
       |
       v
Knowledge Graph

The system demonstrates how LLMs, tool calling, MCP, ML, RAG, and Knowledge Graphs can work together in a single AI-driven investigation workflow.

---

# 👨‍💻 Author

Sharath Chandra

B.Tech – Computer Science & Engineering (AI & ML)

Interested in:

- AI/ML
- Generative AI
- LLMs
- Agentic AI
- RAG
- MCP
- Knowledge Graphs
- Machine Learning Engineering

GitHub:

https://github.com/Sharathchandra234

---

# ⭐ Project Summary

Agentic AI Insurance Claims Investigation System

A portfolio implementation demonstrating:

Google Gemini
      +
Agentic AI
      +
Model Context Protocol
      +
Machine Learning
      +
RAG
      +
FAISS
      +
Neo4j Knowledge Graph
      +
Insurance Investigation

The goal is to demonstrate how an AI agent can dynamically combine structured data, machine learning predictions, document retrieval, and graph relationships to support complex investigation workflows while keeping final decisions under human oversight.