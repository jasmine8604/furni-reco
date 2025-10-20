import React, { useState } from "react";
import axios from "axios";
import ProductCard from "../components/ProductCard";

function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/recommend", {
        query: query,
        top_k: 5
      });

      setResults(response.data.results);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      alert("Failed to fetch recommendations. Is your backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "40px" }}>
      <h2>Find the perfect furniture for your space 🪑</h2>
      <p>Ask naturally — for example: <i>“Show me modern wooden chairs under ₹5000”</i></p>

      <div style={{ marginTop: "20px" }}>
        <input
          type="text"
          placeholder="Type your query here..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            width: "60%",
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            marginRight: "10px"
          }}
        />
        <button onClick={handleSearch}>Search</button>
      </div>

      {loading && <p style={{ marginTop: "20px" }}>Loading recommendations...</p>}

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
        gap: "20px",
        marginTop: "30px"
      }}>
        {results.map((item, index) => (
          <ProductCard key={index} item={item} />
        ))}
      </div>
    </div>
  );
}

export default Home;
