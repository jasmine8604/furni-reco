# pinecone_setup.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
environment = os.getenv("PINECONE_ENVIRONMENT")
index_name = os.getenv("INDEX_NAME")

# Initialize Pinecone
pc = Pinecone(api_key=api_key)

# Create index if it doesn’t exist
if index_name not in [i["name"] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=384,  # matches SentenceTransformer embeddings
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f" Created new Pinecone index: {index_name}")
else:
    print(f" Pinecone index '{index_name}' already exists.")

index = pc.Index(index_name)
print("Connected to Pinecone successfully.")
