import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

function Analytics() {
  const [brandData, setBrandData] = useState([]);
  const [priceData, setPriceData] = useState([]);
  const [categoryData, setCategoryData] = useState([]);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/analytics");
      const { brand_counts, price_bins, category_counts } = response.data;

      // Convert backend data to Recharts-friendly format
      setBrandData(
        Object.entries(brand_counts).map(([brand, count]) => ({
          name: brand,
          count: count,
        }))
      );
      setPriceData(
        Object.entries(price_bins).map(([range, count]) => ({
          range: range,
          count: count,
        }))
      );
      setCategoryData(
        Object.entries(category_counts).map(([cat, count]) => ({
          name: cat,
          count: count,
        }))
      );
    } catch (error) {
      console.error("Error fetching analytics:", error);
      alert("Failed to load analytics data. Is your backend running?");
    }
  };

  const COLORS = ["#8884d8", "#82ca9d", "#ffc658", "#d88484", "#8dd1e1"];

  return (
    <div style={{ padding: "40px" }}>
      <h2> Dataset Analytics</h2>

      <div style={{ marginTop: "40px" }}>
        <h3>Top Brands</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={brandData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: "40px" }}>
        <h3>Price Distribution</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={priceData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="range" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#82ca9d" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: "40px" }}>
        <h3>Category Breakdown</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={categoryData}
              dataKey="count"
              nameKey="name"
              outerRadius={100}
              fill="#8884d8"
              label
            >
              {categoryData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default Analytics;
