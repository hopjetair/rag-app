# RAG Application with FastAPI and AWS

This repository contains a RAG (Retrieval-Augmented Generation) application built with FastAPI, integrated with a PostgreSQL database (`hopjetairline_db`) for vector storage using `pgvector`, and deployed on AWS Fargate. The application processes a PDF document (e.g., `Airline_Regulations_v1.0.pdf`) to enable question-answering capabilities, leveraging HuggingFace embeddings and ChatOllama for generation. The project is modularized into two phases: **Data Ingestion & Indexing** (one-time setup) and **Inference & Querying** (live application).

- **Last Updated**: July 02, 2025, 12:06 AM AEST
- **Author**: [Your Name or Team]
- **License**: [Add License, e.g., MIT]

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Local Development](#local-development)
  - [AWS Deployment](#aws-deployment)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Overview

The RAG application indexes a PDF document and allows users to query it via a FastAPI endpoint (`/ask`). Data ingestion and indexing are separated from the live querying service to optimize performance. The PDF is stored in an S3 bucket for production, with a local fallback for development. The application is deployed on AWS Fargate, with CI/CD managed via GitHub Actions.

## Features

- Modular design with Phase 1 (ingestion) and Phase 2 (inference).
- Supports local PostgreSQL and AWS Aurora/RDS with `pgvector`.
- Integrates with S3 for PDF storage.
- Deployable on AWS Fargate with autoscaling.
- CI/CD pipeline for building and deploying Docker images to ECR.

## Prerequisites

- **Python 3.9+**
- **Docker** (for local DB and containerization)
- **AWS CLI** (configured for local and CI/CD)
- **PostgreSQL 15+** (with `pgvector` extension)
- **AWS Account** with access to:
  - S3
  - ECR
  - ECS/Fargate
  - IAM (role: `arn:aws:iam::109038807292:role/GitHubActionsRole`)
  - Secrets Manager
- **GitHub Account** with repository access

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/rag-app.git
   cd rag-app

   ```

2. Install dependencies:

   ```ps
    python -m venv application
    .\application\Scripts\activate
    pip install -r requirements.txt

   ```

3. Set up environment variables (see Configuration).

## Local Database Setup

    1. Run a local PostgreSQL instance:

        ```bash
        docker run -d -p 5432:5432 -e POSTGRES_USER=ppm -e POSTGRES_PASSWORD=airlinerag -e POSTGRES_DB=hopjetairline_db postgres:15

    2. Enable pgvector:
        ```sql
        CREATE EXTENSION IF NOT EXISTS vector;

        if there is an error in window please refer to https://www.youtube.com/watch?v=0eDXpNzAjV4&t=284s&ab_channel=TechSupport

## S3 Setup

    Create an S3 bucket (e.g., hopjetairline-rag-docs) in ap-south-1.
    Upload Airline_Regulations_v1.0.pdf to the bucket.
    Configure IAM permissions for the ecsTaskExecutionRole to access the bucket.

## Usage

    Local Development
        1. Configure Environment:
            .  Copy .env.example to .env and update with your local settings:
                ```text
                USE_S3=false
                LOCAL_PDF_PATH=./data/Airline_Regulations_v1.0.pdf
                CONNECTION_STRING=postgresql://ppm:airlinerag@localhost:5432/hopjetairline_db
                COLLECTION_NAME=airline_docs_pg

            . Place the PDF in ./data/Airline_Regulations_v1.0.pdf (excluded from Git).

        2. Run Phase 1 (Ingestion):
            . Index the PDF:
                ```bash
                python phase1/ingest.py
        3. Run Phase 2 (API):
            . Start the FastAPI server:
                ```bash
                uvicorn phase2.api:app --host 0.0.0.0 --port 8003
            . Test endpoints:
                .Health: curl http://localhost:8003/health
                .Query: curl -X POST http://localhost:8003/ask -d '{"query": "What are the regulations?"}' -H "Content-Type: application/json"

## AWS Deployment

    1. Configure Environment:
        . Update .env with AWS settings:
            ```text
            USE_S3=true
            BUCKET_NAME=hopjetairline-rag-docs
            OBJECT_KEY=Airline_Regulations_v1.0.pdf
            CONNECTION_STRING=postgresql://ppm:your_password@your-hopjetairline-db-host.ap-south-1.rds.amazonaws.com:5432/hopjetairline_db
            COLLECTION_NAME=airline_docs_pg
        . Store RDS_PASSWORD in Secrets Manager.
    2. Trigger CI/CD:
        . Push changes to the main branch to initiate the GitHub Actions workflow.
        . The pipeline builds the Docker image, pushes it to ECR, and deploys to Fargate.
    3. Access the API:
        . Use the ALB DNS or public IP (e.g., http://54.252.165.253:8003/ask) after deployment.

## Project Structure

```
    rag-app/
    ├── phase1/
    │ ├── ingest.py # Data ingestion and indexing
    │ ├── embeddings.py # Embedding generation
    │ ├── vector_store.py # Vector store management
    │ └── **init**.py
    ├── phase2/
    │ ├── api.py # FastAPI application
    │ ├── retrieval.py # RAG retrieval logic
    │ ├── vector_store.py # Vector store querying
    │ └── **init**.py
    ├── Dockerfile
    ├── task-definition.json
    ├── .github/workf
    │ └── ci-cd.yml
    ├── requirements.txt
    └── .env.example # Example environment variables

```

## Configuration

    . Use a .env file based on .env.example with the following variables:
        . USE_S3: true for S3, false for local PDF.
        . LOCAL_PDF_PATH: Local path to the PDF (e.g., ./data/Airline_Regulations_v1.0.pdf).
        . BUCKET_NAME: S3 bucket name (e.g., hopjetairline-rag-docs).
        . OBJECT_KEY: S3 object key (e.g., Airline_Regulations_v1.0.pdf).
        . CONNECTION_STRING: PostgreSQL connection string.
        . COLLECTION_NAME: Vector store collection name (e.g., airline_docs_pg).
    . Example .env:
        ```text
        USE_S3=false
        LOCAL_PDF_PATH=./data/Airline_Regulations_v1.0.pdf
        CONNECTION_STRING=postgresql://ppm:airlinerag@localhost:5432/hopjetairline_db
        COLLECTION_NAME=airline_docs_pg

## CI/CD Pipeline

    . Trigger: Push to main branch.
    . Steps:
        . Checkout code.
        . Configure AWS credentials with OIDC (role: arn:aws:iam::109038807292:role/GitHubActionsRole).
        . Login to ECR.
        . Build and push Docker image to 109038807292.dkr.ecr.ap-south-1.amazonaws.com/rag-api.
        . Register and update ECS task definition.
    . Permissions: id-token: write, contents: read.

## Deployment

    . Local: Run ingestion and API as described.
    . AWS: Automated via CI/CD. Ensure S3 bucket, RDS, and IAM roles are configured.

## Contributing

    1. Fork the repository.
    2. Create a feature branch (git checkout -b feature-branch).
    3. Commit changes (git commit -m "Add feature").
    4. Push to the branch (git push origin feature-branch).
    5. Open a Pull Request.

## License

[Add your license here, e.g., MIT License]

```text
### Notes

- **PDF Management**: The README emphasizes excluding the PDF from Git and using S3, with a local fallback in `./data/`. Update paths or bucket names as needed.
- **Customization**: Replace placeholders (e.g., `your-username`, `your_password`, `your-hopjetairline-db-host`) with actual values.
- **Testing**: Add specific test commands or endpoints if you have additional requirements.

This `README.md` provides a clear guide for setting up and using the project, aligning with your current setup as of July 02, 2025. Let me know if you’d like to adjust any sections!
```
