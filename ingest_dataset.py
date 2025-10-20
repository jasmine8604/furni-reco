import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# STEP 1: Load API key and connect to Pinecone

load_dotenv()
api_key = os.getenv("PINECONE_API_KEY")

if not api_key:
    raise ValueError("PINECONE_API_KEY not found. Please check your .env file.")

pc = Pinecone(api_key=api_key)
index_name = "furni-reco-index"

# Create index if not already exists
if index_name not in [i["name"] for i in pc.list_indexes()]:
    print("Creating Pinecone index...")
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

index = pc.Index(index_name)

# ======================================================
# STEP 2: Load dataset
# ======================================================
csv_path = "data/intern_data_ikarus.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f" Dataset not found at {csv_path}")

df = pd.read_csv(csv_path)
df = df.fillna("Not specified")

print(f" Loaded dataset with {len(df)} records")


# STEP 3: Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# STEP 4: Generate embeddings and upload in batches
batch_size = 50
vectors = []

for i, row in tqdm(df.iterrows(), total=len(df), desc="Uploading to Pinecone"):
    try:
        text = f"{row['title']} {row['description']} {row['categories']} {row['material']} {row['color']}"
        embedding = model.encode(text).tolist()

        metadata = {
            "title": str(row.get("title", "Not specified")),
            "brand": str(row.get("brand", "Not specified")),
            "price": str(row.get("price", "Not specified")),
            "material": str(row.get("material", "Not specified")),
            "color": str(row.get("color", "Not specified")),
            "categories": str(row.get("categories", "Not specified")),
        }

        vectors.append((str(row["uniq_id"]), embedding, metadata))

        if len(vectors) >= batch_size:
            index.upsert(vectors=vectors)
            vectors = []

    except Exception as e:
        print(f" Error at row {i}: {e}")

if vectors:
    index.upsert(vectors=vectors)

print("Ingestion complete. All embeddings and metadata uploaded successfully!")
