
// A simple product card that supports two backend shapes:
// 1) { title, brand, price, ... }  OR
// 2) { metadata: { title, brand, price, ... } }

import React from "react";

function ProductCard({ item }) {
  // Normalize metadata: prefer top-level fields, fall back to metadata object
  const meta = {
    title: item.title ?? item.metadata?.title ?? "Untitled Product",
    brand: item.brand ?? item.metadata?.brand ?? "Not specified",
    material: item.material ?? item.metadata?.material ?? "Not specified",
    color: item.color ?? item.metadata?.color ?? "Not specified",
    categories: item.categories ?? item.metadata?.categories ?? "Not specified",
    price: item.price ?? item.metadata?.price ?? "Not specified",
    score: item.score ?? item.metadata?.score ?? null,
    ai_description: item.ai_description ?? item.metadata?.ai_description ?? ""
  };

  return (
    <div style={{
      border: "1px solid #ddd",
      borderRadius: "10px",
      padding: "15px",
      backgroundColor: "white",
      boxShadow: "0 2px 6px rgba(0, 0, 0, 0.08)"
    }}>
      <h3>{meta.title}</h3>
      <p><strong>Brand:</strong> {meta.brand}</p>
      <p><strong>Material:</strong> {meta.material}</p>
      <p><strong>Color:</strong> {meta.color}</p>
      <p><strong>Category:</strong> {meta.categories}</p>
      <p><strong>Price:</strong> {meta.price}</p>
      {meta.ai_description && (
        <p><strong>AI Description:</strong> {meta.ai_description}</p>
      )}
      {meta.score !== null && (
        <p style={{ color: "#777", fontSize: "0.9em" }}>Score: {Number(meta.score).toFixed(3)}</p>
      )}
    </div>
  );
}

export default ProductCard;
