# RAG FAQ Agent - Vertex AI

> **Portfolio Project**: A demonstration of RAG (Retrieval-Augmented Generation) implementation using Google Vertex AI and Google Cloud Platform.

A Retrieval-Augmented Generation (RAG) chatbot powered by Google Vertex AI that provides intelligent customer support for travel booking services. The agent uses a knowledge base of FAQ documents to answer user questions accurately and contextually.

This project showcases the integration of modern AI technologies including vector embeddings, semantic search, and large language models to create an intelligent customer support system.

## Features

- **RAG-powered responses**: Combines retrieval from a knowledge base with generative AI for accurate answers
- **Vertex AI integration**: Uses Google's Gemini 2.0 Flash model with RAG capabilities
- **Customer support focused**: Specifically designed for travel booking inquiries
- **Multilingual support**: Responds in the same language as the user's question
- **URL references**: Automatically includes relevant URLs from the knowledge base
- **Interactive chat**: Command-line interface for real-time conversations

## Prerequisites

- Google Cloud Project with Vertex AI API enabled
- Google Cloud Storage bucket
- Service account credentials with appropriate permissions:
  - Vertex AI User
  - Storage Admin
  - AI Platform Admin
- Python 3.8+

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rag-faq-agent-vertex-ai
   ```

2. **Set up virtual environment and install dependencies**:
   ```bash
   make install
   ```
   
   Or manually:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud credentials**:
   - Place your service account JSON file as `credentials.json` in the project root
   - The Makefile automatically sets `GOOGLE_APPLICATION_CREDENTIALS=credentials.json`

4. **Update configuration**:
   - Edit `deploy/rag-deploy.py` to set your actual values:
     - `PROJECT_ID`: Your Google Cloud Project ID
     - `LOCATION`: Your preferred GCP region (default: `us-central1`)
     - `BUCKET_NAME`: Your Google Cloud Storage bucket name
   - After running the deployment script, update `agent/agent.py`:
     - `PROJECT_ID`: Same as above
     - `LOCATION`: Same as above
     - `RAG_CORPUS_NAME`: The corpus name generated after deployment

## Data Format

The knowledge base should be in JSONL format (`data/utils/faq_dataset_rag_ready.jsonl`). Each line should contain a JSON object with the FAQ data:

```json
{"question": "How do I cancel my reservation?", "answer": "To cancel your reservation...", "url": "https://travel-agency.example.com/cancellation"}
```

## Usage

### 1. Deploy the Knowledge Base

First, upload your FAQ dataset and create the RAG corpus in Vertex AI:

```bash
make upload-rag-corpus
```

This command:
- Uploads the JSONL file to Google Cloud Storage
- Creates a RAG corpus in Vertex AI
- Imports and processes the data for retrieval

**Note**: This process can take several minutes to complete.

### 2. Run the Chat Agent

Once the corpus is deployed, start the interactive chat agent:

```bash
make run-agent
```

The agent will start and you can begin asking questions:

```
Chat Agent Ready! Ask me anything about the documents in your corpus.
Type 'exit' to end the chat.
You: How do I make a hotel reservation?
Agent: To make a hotel reservation with our travel agency...
```

## Project Structure

```
rag-faq-agent-vertex-ai/
├── agent/
│   ├── __init__.py
│   ├── agent.py              # Main chat agent implementation
│   └── llm_instruction.py    # System instructions for the AI
├── data/
│   └── utils/
│       └── faq_dataset_rag_ready.jsonl  # Knowledge base data
├── deploy/
│   └── rag-deploy.py         # Deployment script for RAG corpus
├── credentials.json          # Google Cloud service account key
├── requirements.txt          # Python dependencies
├── Makefile                  # Build and deployment commands
└── README.md                 # This file
```

## Configuration

### Key Configuration Files

- **`deploy/rag-deploy.py`**: Configure `PROJECT_ID`, `LOCATION`, `BUCKET_NAME`
- **`agent/agent.py`**: Configure `PROJECT_ID`, `LOCATION`, `RAG_CORPUS_NAME`
- **`agent/llm_instruction.py`**: Customize the AI's behavior and instructions

### Environment Variables

The project uses the following environment variable:
- `GOOGLE_APPLICATION_CREDENTIALS`: Path to the service account JSON file (set automatically by Makefile)

## Use Cases

This RAG agent is specifically designed for travel agency customer support and can help with:

- Hotel reservation procedures
- Payment methods and policies
- Cancellation rules and processes
- Invoice requests
- Booking price information
- Partnership services (e.g., tour operators, activity providers)
- General booking inquiries

## Troubleshooting

### Common Issues

1. **Authentication errors**:
   - Ensure `credentials.json` is in the project root
   - Verify the service account has the required permissions

2. **Corpus not found**:
   - Run `make upload-rag-corpus` first to create the corpus
   - Update `RAG_CORPUS_NAME` in `agent/agent.py` with the correct corpus ID

3. **Import errors**:
   - Activate the virtual environment: `source .venv/bin/activate`
   - Reinstall dependencies: `make install`

4. **Slow responses**:
   - The first query may be slower as the model initializes
   - Large knowledge bases may require more processing time

## Dependencies

- `google-cloud-aiplatform[adk,agent_engines,corpora]>=1.102.0`: Google Cloud AI Platform SDK

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Google Cloud Vertex AI documentation
3. Open an issue in the repository
