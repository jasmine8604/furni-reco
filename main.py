"""
app/main.py

This file defines the main FastAPI backend for the Furniture Recommendation Web App.
It exposes endpoints for health checks and product recommendations using Pinecone.

Author: Jasmine Panesar
Date: 19 October 2025
"""
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from pydantic import BaseModel
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables (like Pinecone API key)
load_dotenv()

# Initialize Pinecone client
api_key = os.getenv("PINECONE_API_KEY")
index_name = os.getenv("INDEX_NAME")
pc = Pinecone(api_key=api_key)
index = pc.Index(index_name)

# Initialize Sentence Transformer model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FLAN-T5 model for text generation
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# Create FastAPI app instance
app = FastAPI(
    title="FurniReco API",
    description="Backend service for furniture product recommendations using ML and Pinecone.",
    version="1.0"
)

# Enable CORS to allow frontend (React) communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for recommendations
class RecommendationRequest(BaseModel):
    query: str
    top_k: int = 5  # number of results to return

@app.get("/")
def home():
    """Basic route to confirm backend is live."""
    return {"message": " Backend is running successfully!"}

@app.post("/recommend")
async def recommend(query: dict):
    """
    Given a text query, encode it, search Pinecone for similar products,
    and return the most relevant recommendations with metadata.
    """
    user_query = query.get("query", "")
    top_k = int(query.get("top_k", 5))

    if not user_query.strip():
        return {"error": "Empty query provided"}

    # Encode query
    query_vector = model.encode(user_query).tolist()

    # Query Pinecone
    try:
        response = index.query(vector=query_vector, top_k=top_k, include_metadata=True)
    except Exception as e:
        return {"error": f"Pinecone query failed: {e}"}

    results = []
    for match in response.get("matches", []):
        metadata = match.get("metadata", {})

        results.append({
            "id": match.get("id"),
            "score": round(match.get("score", 0), 3),
            "title": metadata.get("title", "Not specified"),
            "brand": metadata.get("brand", "Not specified"),
            "price": metadata.get("price", "Not specified"),
            "material": metadata.get("material", "Not specified"),
            "color": metadata.get("color", "Not specified"),
            "categories": metadata.get("categories", "Not specified"),
        })

    if not results:
        return {"message": "No results found"}

    return {
        "query": user_query,
        "results": results
    }

    # Convert query to embedding vector
    query_vector = model.encode(request.query).tolist()

    # Query Pinecone for top_k most similar items
    search_results = index.query(
        vector=query_vector,
        top_k=request.top_k,
        include_metadata=True
    )

    # Format response neatly
    formatted_results = []
    for match in search_results.get("matches", []):
        metadata = match["metadata"]
            # Generate creative product description using FLAN-T5
    product_name = metadata.get("title", "Unknown product")
    material = metadata.get("material", "")
    brand = metadata.get("brand", "")
    gen_prompt = f"Write a short, appealing product description for a {product_name} made of {material} by {brand}."

    gen_output = generator(gen_prompt, max_new_tokens=60, do_sample=True)[0]['generated_text']

    formatted_results.append({
        "id": match["id"],
        "score": round(match["score"], 3),
        "title": product_name,
        "brand": brand,
        "price": metadata.get("price", "N/A"),
        "material": material,
        "color": metadata.get("color", "N/A"),
        "categories": metadata.get("categories", "N/A"),
        "ai_description": gen_output.strip()
    })


    return {
        "query": request.query,
        "results": formatted_results
    }




app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "✅ Backend is running successfully!"}


@app.post("/query")
def query_products(payload: dict):
    query_text = payload.get("query", "")
    top_k = payload.get("top_k", 5)


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = "furni-reco-index"

pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index(index_name)

# Load the same model used for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load the dataset (used for product metadata)
df = pd.read_csv("data/intern_data_ikarus.csv")  


@app.post("/recommend")
async def recommend(request: dict):
    
    query_vector = model.encode(request.get("query", "")).tolist()
    top_k = request.get("top_k", 5)

    # Query Pinecone for similar items
    try:
        search_results = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
    except Exception as e:
        return {"error": f"Error while querying Pinecone: {e}"}

    formatted_results = []

    for match in search_results.get("matches", []):
        metadata = match.get("metadata", {})

        # Generate creative product description using FLAN-T5
        product_name = metadata.get("title", "Unknown product")
        material = metadata.get("material", "")
        brand = metadata.get("brand", "")
        gen_prompt = (
            f"Write a short, appealing product description for a {product_name} "
            f"made of {material} by {brand}."
        )

        gen_output = generator(
            gen_prompt,
            max_new_tokens=60,
            do_sample=True
        )[0]['generated_text']

        formatted_results.append({
            "id": match.get("id"),
            "score": round(match.get("score", 0), 3),
            "title": product_name,
            "brand": brand,
            "price": metadata.get("price", "N/A"),
            "material": material,
            "color": metadata.get("color", "N/A"),
            "categories": metadata.get("categories", "N/A"),
            "ai_description": gen_output.strip()
        })

    return {
        "query": request.get("query", ""),
        "results": formatted_results
    }

@app.get("/analytics")
def get_analytics():
    try:
        # Path to your dataset
        data_path = os.path.join(os.path.dirname(__file__), "../data/intern_data_ikarus.csv")
        df = pd.read_csv(data_path)

        # Fill missing values
        df["brand"] = df["brand"].fillna("Unknown")
        df["categories"] = df["categories"].fillna("Unknown")

        # Clean and convert price column
        df["price"] = (
            df["price"]
            .astype(str)
            .str.replace("[^0-9.]", "", regex=True)
            .replace("", "0")
            .astype(float)
        )

        # Compute analytics 
        brand_counts = df["brand"].value_counts().head(10).to_dict()

        price_bins = pd.cut(
            df["price"], bins=[0, 100, 500, 1000, 5000, 10000, 50000]
        )
        price_dist = price_bins.value_counts().sort_index()
        price_bins_dict = {str(k): int(v) for k, v in price_dist.items()}

        category_counts = {}
        for cats in df["categories"].dropna():
            for c in str(cats).strip("[]").replace("'", "").split(","):
                c = c.strip()
                if c:
                    category_counts[c] = category_counts.get(c, 0) + 1

        category_counts = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:8])

        return {
            "brand_counts": brand_counts,
            "price_bins": price_bins_dict,
            "category_counts": category_counts,
        }

    except Exception as e:
        return {"error": str(e)}
