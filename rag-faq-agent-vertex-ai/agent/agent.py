import vertexai
from vertexai.preview import rag
from vertexai.generative_models import GenerativeModel, Tool
from llm_instruction import INSTRUCTION

# Project and RAG configuration
PROJECT_ID = "your-gcp-project-id"
LOCATION = "us-central1"
RAG_CORPUS_NAME = "projects/your-gcp-project-id/locations/us-central1/ragCorpora/your-corpus-id"


# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create a RAG retrieval tool
rag_retrieval_tool = Tool.from_retrieval(
    retrieval=rag.Retrieval(
        source=rag.VertexRagStore(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=RAG_CORPUS_NAME,
                )
            ]
        )
    )
)

# Create a Gemini model instance with the RAG tool
rag_model = GenerativeModel(
    model_name="gemini-2.0-flash-001",
    tools=[rag_retrieval_tool],
    system_instruction=INSTRUCTION
)

print("Chat Agent Ready! Ask me anything about the documents in your corpus.")
print("Type 'exit' to end the chat.")

# Start a chat session
chat = rag_model.start_chat()

while True:
    # Get user input
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Ending chat. Goodbye!")
        break

    # Send the message to the model and print the response
    response = chat.send_message(user_input)
    print(f"Agent: {response.text}")

