\# 🚗 Agentic AI Insurance Claims Investigation System



An end-to-end \*\*Agentic AI insurance claims investigation system\*\* that combines \*\*Google Gemini, Model Context Protocol (MCP), Retrieval-Augmented Generation (RAG), and Machine Learning\*\* to investigate automobile insurance claims.



The system allows an AI agent to dynamically use MCP tools to retrieve claim, policy, customer, and vehicle information, perform ML-based fraud-risk prediction, and retrieve relevant insurance policy evidence through semantic search.



> \*\*Note:\*\* This project is an educational/demo system using synthetic insurance data. The ML model and policy documents are not intended for real-world insurance decisions.



\---



\## 🚀 Project Overview



Insurance claims investigation often requires information from multiple systems:



\- Claim records

\- Insurance policies

\- Customer history

\- Vehicle information

\- Fraud-risk analysis

\- Policy documents and coverage conditions



This project demonstrates how an \*\*Agentic AI architecture\*\* can coordinate these different capabilities through \*\*MCP tools\*\*.



Instead of hard-coding a fixed workflow, the Gemini-based agent determines which tools are required based on the user's request and uses their results to build an investigation report.



\### Example



A user can ask:



> Investigate claim CLM001 completely. Check the claim, policy, customer, vehicle, use the ML fraud model, and search the policy documents to determine whether the accidental damage is covered.



The agent can then perform a workflow such as:



```text

User Request

&#x20;    │

&#x20;    ▼

Gemini Agent

&#x20;    │

&#x20;    ├──► get\_claim

&#x20;    │

&#x20;    ├──► get\_policy

&#x20;    │

&#x20;    ├──► get\_customer

&#x20;    │

&#x20;    ├──► get\_vehicle

&#x20;    │

&#x20;    ├──► predict\_fraud\_risk

&#x20;    │

&#x20;    └──► search\_policy\_documents

&#x20;                │

&#x20;                ▼

&#x20;         Policy Evidence

&#x20;                │

&#x20;                ▼

&#x20;         Gemini Reasoning

&#x20;                │

&#x20;                ▼

&#x20;     Investigation Report

🏗️ System Architecture

&#x20;                        ┌─────────────────────┐

&#x20;                        │       User          │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │    Gemini Agent     │

&#x20;                        │  Agentic Reasoning  │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                  ┌────────────────┼────────────────┐

&#x20;                  │                │                │

&#x20;                  ▼                ▼                ▼

&#x20;             MCP Tools          ML Model           RAG

&#x20;                  │                │                │

&#x20;                  ▼                ▼                ▼

&#x20;         Insurance Data      Fraud Prediction   FAISS Search

&#x20;                  │                │                │

&#x20;                  └────────────────┼────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │ Evidence + Reasoning│

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │ Investigation Report│

&#x20;                        └─────────────────────┘

🤖 Agentic AI



The project uses Google Gemini as the reasoning engine.



The agent is instructed to:



Understand the user's investigation request.

Identify the required information.

Select the appropriate MCP tools.

Follow relationships between insurance records.

Execute MCP tools.

Analyze ML fraud-risk information.

Search policy documents using RAG.

Distinguish facts from policy evidence and interpretation.

Generate a structured investigation report.



The agent is not limited to a single hard-coded sequence.



🔌 Model Context Protocol (MCP)



The project uses MCP to expose insurance capabilities as tools that can be dynamically discovered and called by the AI agent.



The MCP server currently exposes 7 tools.



Available MCP Tools

Tool	Purpose

&#x20;get\_claim    -	Retrieves insurance claim information

get\_policy    - Retrieves policy information

get\_customer  -	Retrieves customer information

get\_vehicle   - 	Retrieves vehicle information

calculate\_fraud\_score -	Performs rule-based fraud scoring

predict\_fraud\_risk   -	Performs ML-based fraud-risk prediction

search\_policy\_documents -   Performs semantic search over policy documents

🔄 Claim Investigation Workflow



The agent can follow relationships between the insurance records.



Claim

&#x20; │

&#x20; │ policy\_number

&#x20; ▼

Policy

&#x20; │

&#x20; │ customer\_id

&#x20; ▼

Customer

&#x20; │

&#x20; │ vehicle\_id

&#x20; ▼

Vehicle



For example:



get\_claim

&#x20;   │

&#x20;   ▼

policy\_number

&#x20;   │

&#x20;   ▼

get\_policy

&#x20;   │

&#x20;   ▼

customer\_id

&#x20;   │

&#x20;   ▼

get\_customer

&#x20;   │

&#x20;   ▼

vehicle\_id

&#x20;   │

&#x20;   ▼

get\_vehicle



After gathering the required information, the agent can use:



predict\_fraud\_risk



and:



search\_policy\_documents



to support the investigation.



📚 Retrieval-Augmented Generation (RAG)



The project includes a semantic search pipeline for insurance policy documents.



RAG Pipeline

Policy Documents

&#x20;      │

&#x20;      ▼

Document Chunking

&#x20;      │

&#x20;      ▼

Sentence Transformers

&#x20;      │

&#x20;      ▼

Text Embeddings

&#x20;      │

&#x20;      ▼

FAISS Vector Index

&#x20;      │

&#x20;      ▼

Semantic Search

&#x20;      │

&#x20;      ▼

Relevant Policy Evidence

&#x20;      │

&#x20;      ▼

Gemini Agent

Embedding Model

all-MiniLM-L6-v2

Vector Database

FAISS



The embeddings are normalized and searched using cosine similarity through a FAISS inner-product index.



📄 Policy Documents



The project currently contains synthetic insurance policy documents covering areas such as:



Comprehensive automobile insurance

Third-party insurance

Claims guidelines

Fraud investigation guidelines



The documents are stored in:



policies/



The vector database is stored in:



vector\_db/

🧠 Machine Learning Fraud-Risk Model



The project includes a Random Forest-based fraud-risk prediction model.



Features



The model uses features including:



claim\_amount

previous\_claims

policy\_age

vehicle\_age

claim\_frequency

repair\_cost

location\_risk

Model

RandomForestClassifier



The model was trained using synthetic insurance claim data for demonstration purposes.



Demonstration Results



The model training experiment achieved approximately:



Accuracy: 93.50%

ROC-AUC: 0.9807



These results should not be interpreted as real-world insurance fraud detection performance because the training dataset is synthetic.



🛡️ Fraud Risk Interpretation



The ML output is treated as an investigation-support signal.



The system does not use the prediction as proof of fraud.



Example:



Fraud Probability: 1%

Risk Level: Low



The final insurance decision should remain subject to appropriate human review and business processes.



📊 Rule-Based Fraud Scoring



The project also includes a simpler rule-based fraud scoring tool:



calculate\_fraud\_score



This demonstrates how traditional business rules can coexist with ML-based predictions within an Agentic AI system.



🔎 Policy Evidence and Reasoning



The agent is instructed to separate information into three categories.



FACTS



Information directly returned by MCP tools.



POLICY EVIDENCE



Information retrieved from insurance policy documents through RAG.



INTERPRETATION



Reasoning performed by the AI agent using the available facts and policy evidence.



This separation helps reduce unsupported assumptions.



📋 Final Investigation Report



For a complete investigation, the agent generates a structured report containing:



Claim Summary

Policy Verification

Customer Information

Vehicle Information

ML Fraud Assessment

Policy Coverage Analysis

Key Risk Indicators

Recommended Next Investigation Steps

Human Review Recommendation

🛠️ Technology Stack

Programming

Python 3.11

Generative AI

Google Gemini

Google GenAI Python SDK

Agentic AI

Model Context Protocol (MCP)

MCP Python SDK

Machine Learning

Scikit-learn

Random Forest

Pandas

NumPy

RAG

Sentence Transformers

FAISS

Semantic Search

Vector Embeddings

Development

Python virtual environment

PowerShell

Git

GitHub

📁 Project Structure

agentic-ai-mcp-insurance/

│

├── agent.py

│   └── Gemini Agent + MCP orchestration

│

├── server.py

│   └── MCP server and insurance tools

│

├── client.py

│   └── MCP client

│

├── tool\_test.py

│   └── MCP tool testing

│

├── gemini\_test.py

│   └── Gemini API testing

│

├── fraud\_model.py

│   └── Synthetic dataset generation and model training

│

├── fraud\_predict.py

│   └── Fraud prediction testing

│

├── fraud\_model.pkl

│   └── Trained Random Forest model

│

├── rag\_ingest.py

│   └── Policy document ingestion and vector indexing

│

├── rag\_search.py

│   └── Semantic policy search

│

├── policies/

│   ├── auto\_comprehensive\_policy.txt

│   ├── auto\_third\_party\_policy.txt

│   ├── claims\_guidelines.txt

│   └── fraud\_investigation\_guidelines.txt

│

├── vector\_db/

│   ├── insurance\_policies.index

│   └── metadata.json

│

├── requirements.txt

│

├── .gitignore

│

└── README.md

⚙️ Installation

1\. Clone the repository

git clone https://github.com/Sharathchandra234/agentic-ai-mcp-insurance.git



Move into the project:



cd agentic-ai-mcp-insurance

2\. Create a virtual environment



Windows:



python -m venv .venv



Activate it:



.venv\\Scripts\\Activate.ps1

3\. Install dependencies

pip install -r requirements.txt

🔑 Gemini API Configuration



The project requires a Gemini API key.



Set the API key as an environment variable.



Windows PowerShell

$env:GEMINI\_API\_KEY="YOUR\_GEMINI\_API\_KEY"



Do not commit your API key to GitHub.



The .gitignore file is configured to ignore environment files and other local configuration files.



▶️ Running the Project



After activating the virtual environment and setting the API key:



python agent.py



The application will discover the available MCP tools and prompt you for an investigation request.



Example:



Investigate claim CLM001 completely. Check the claim, policy,

customer, vehicle, use the ML fraud model, and search the policy

documents to determine whether the accidental damage is covered.

🧪 Testing Individual Components

Test Gemini

python gemini\_test.py

Test MCP tools

python tool\_test.py

Test fraud model

python fraud\_model.py

Test fraud prediction

python fraud\_predict.py

Test RAG search

python rag\_search.py

🔬 Example Investigation



Example claim:



Claim ID: CLM001

Policy ID: POL1001

Claim Type: Accident

Claim Amount: ₹85,000

Repair Cost: ₹60,000

Claim Status: Under Review



The agent can retrieve:



Claim

&#x20;  ↓

Policy

&#x20;  ↓

Customer

&#x20;  ↓

Vehicle

&#x20;  ↓

ML Fraud Risk

&#x20;  ↓

Policy Coverage Evidence



The final response combines the retrieved information into a structured investigation report.



🔐 Security Considerations



Never commit:



.env

API keys

passwords

credentials

private certificates



The project .gitignore excludes common local secrets and development artifacts.



Before pushing changes to GitHub, always check:



git status

⚠️ Disclaimer



This project is intended for educational, portfolio, and technical demonstration purposes.



The insurance records and ML training data are synthetic.



The fraud model should not be used to make real insurance fraud determinations.



The policy documents included in this repository are demonstration documents and should not be interpreted as actual insurance contracts.



Production deployment would require:



Real insurance data governance

Model validation

Security controls

Authentication and authorization

Audit logging

Human oversight

Regulatory compliance

Production-grade policy sources

Monitoring and evaluation

🔮 Future Improvements



Potential future extensions include:



FastAPI backend

REST API for claim investigation

Web-based dashboard

Authentication and role-based access

PostgreSQL / MongoDB integration

Production vector database

Advanced RAG evaluation

RAG citations and source highlighting

LLM observability

MLflow model tracking

Model monitoring

Human-in-the-loop claim review

Docker deployment

Kubernetes deployment

Cloud deployment

Automated evaluation pipelines

Multi-agent insurance workflows

MCP authentication and authorization

Production insurance data integration

🎯 Key Learning Outcomes



This project demonstrates practical implementation of:



Agentic AI

LLM tool calling

Model Context Protocol

MCP server/client architecture

Dynamic tool discovery

Retrieval-Augmented Generation

Vector databases

Semantic search

Sentence embeddings

FAISS

Machine Learning

Random Forest

AI-assisted insurance investigation

Tool orchestration

Human-in-the-loop AI

AI safety and grounded reasoning

👨‍💻 Author



Sharath Chandra



B.Tech – Computer Science \& Engineering (AI \& ML)



Interested in:



AI/ML

Generative AI

LLMs

Agentic AI

RAG

MCP

Machine Learning Engineering



GitHub:



https://github.com/Sharathchandra234

