# How to use the `rag-deploy.py` script

This document explains the purpose and detailed functioning of the `deploy/rag-deploy.py` script, which is part of the `rag-faq-agent-vertex-ai` project.

## Purpose

The main purpose of `rag-deploy.py` is to prepare and deploy the knowledge base (corpus) for a Retrieval-Augmented Generation (RAG) agent in Vertex AI. The script automates two key tasks:

1.  Upload the FAQ dataset to Google Cloud Storage (GCS).
2.  Create a RAG Corpus in Vertex AI and populate it with the uploaded data.

## Detailed Functioning

The script runs sequentially and performs the following actions:

### 1. Configuration

At the beginning of the script, several important constants are defined:

- `PROJECT_ID`: The ID of your Google Cloud project.
- `LOCATION`: The region where Vertex AI resources will be created (e.g., `us-central1`).
- `BUCKET_NAME`: The name of the Google Cloud Storage bucket to store the data.
- `SOURCE_FILE`: The local path to the data file (`faq_dataset_rag_ready.jsonl`) containing questions and answers.
- `DEST_BLOB`: The name of the uploaded data file in the GCS bucket.

### 2. Uploading data to Google Cloud Storage

The `upload_to_bucket` function:

- Connects to Google Cloud Storage.
- Selects the bucket specified in `BUCKET_NAME`.
- Uploads the `SOURCE_FILE` to the bucket with the name `DEST_BLOB`.
- Prints a confirmation message to the console.

### 3. Creating or updating the RAG Corpus

The `create_or_update_corpus` function:

- Initializes Vertex AI with the `PROJECT_ID` and `LOCATION` defined.
- Configures the embedding model to convert text into numeric vectors (embeddings).
- Creates a new corpus in Vertex AI. This process can take several minutes, so the script prints a message to notify the user.
- Imports and processes the data file from GCS. During the import, the text is divided into chunks to optimize information retrieval. This process can also be long, and the user is notified.
- Prints a success message upon completion of the import.

## How to run the script

To run the script, you can use the `make` command:

```bash
make upload-rag-corpus
```

This command will execute the script `python3 deploy/rag-deploy.py`, which will perform all the steps described above.

@startuml
participant "Vertex AI RAG" as RAG
participant "Google Cloud Storage" as GCS
participant "Script (deploy/rag-deploy.py)" as SCRIPT
participant "Makefile" as MAKEFILE

SCRIPT ->> GCS: 1. Upload data to GCS
GCS ->> SCRIPT: Bucket ready
SCRIPT ->> RAG: 2. Create or update corpus
RAG ->> SCRIPT: Corpus ready
SCRIPT ->> RAG: 3. Import data from bucket
RAG ->> SCRIPT: Import done

@enduml

