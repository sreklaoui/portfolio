from google.cloud import storage
from vertexai.preview import rag
import vertexai
import os

PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
BUCKET_NAME = "your-rag-corpus-bucket"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_FILE = os.path.join(ROOT, "data/utils", "faq_dataset_rag_ready.jsonl")
DEST_BLOB = "faq_dataset_rag_ready.jsonl"

def upload_to_bucket(bucket_name, source_file, dest_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(source_file)
    print(f"File {source_file} uploaded to gs://{bucket_name}/{dest_blob}.")
    return bucket, dest_blob

def create_or_update_corpus(bucket, blob_name):
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Configure embedding model
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-005"
        )
    )
    
    print("Creating RAG corpus... This may take a few minutes.")
    # Create RagCorpus
    rag_corpus = rag.create_corpus(
        display_name=BUCKET_NAME,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    
    print(f"Corpus '{rag_corpus.name}' created.")
    gcs_path = f"gs://{bucket.name}/{blob_name}"
    print(f"Importing files from {gcs_path} into the corpus... This may also take a while.")

    rag.import_files(
        rag_corpus.name,
        [gcs_path],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(
                chunk_size=512,
                chunk_overlap=100,
            ),
        ),
        max_embedding_requests_per_min=1000,
    )
    
    print(f"Successfully imported files to corpus '{rag_corpus.name}'.")
    return rag_corpus

if __name__ == "__main__":
    bucket, blob_name = upload_to_bucket(BUCKET_NAME, SOURCE_FILE, DEST_BLOB)
    create_or_update_corpus(bucket, blob_name)
