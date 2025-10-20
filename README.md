# 🪑 AI Furniture Recommendation System

### An ML-powered web app that recommends furniture products, generates creative AI descriptions, and provides interactive analytics — built using **FastAPI**, **React**, **LangChain**, **Pinecone**, and **FLAN-T5**.

---

## 🌟 Overview

This project is an **end-to-end AI-driven recommendation platform** for furniture items.  
It combines Machine Learning, NLP, Computer Vision, and Generative AI to deliver smart product suggestions, semantic search, and data insights — all through a simple web interface.

---

## 🧩 Features

### 🔹 Product Recommendation
Recommends furniture items based on natural-language queries such as:
> “Show me modern wooden chairs under ₹5000”

### 🔹 Generative AI Descriptions
Uses **FLAN-T5** to generate creative, human-like product descriptions for recommended items.

### 🔹 NLP + Vector Search
- Embeds product data using **SentenceTransformers**
- Stores embeddings in **Pinecone** for semantic similarity search

### 🔹 Computer Vision
Includes an image classification model (ResNet-18) for identifying furniture categories and assisting in recommendation logic.

### 🔹 Analytics Dashboard
An interactive React page visualizing:
- Price distribution  
- Top brands  
- Popular categories  

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | React.js, Axios, Recharts |
| **Backend** | FastAPI (Python) |
| **Vector DB** | Pinecone |
| **ML/NLP Models** | SentenceTransformers, FLAN-T5 |
| **CV Model** | ResNet-18 |
| **Integration** | LangChain |
| **Data Handling** | Pandas, NumPy |
| **Visualization** | Chart.js / Recharts |

---

## 🧠 Architecture
User Query → FastAPI → LangChain → Pinecone (Vector DB)
     ↓                                ↓
   FLAN-T5 (description)         SentenceTransformer (embeddings)
     ↓                                ↓
  React Frontend ← Axios ← FastAPI JSON Response

