import { useState } from "react";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery) {
      setError("Please enter an item.");
      setResult(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await fetch(
        `http://127.0.0.1:8000/search?q=${encodeURIComponent(trimmedQuery)}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Something went wrong");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="app">
      <div className="container">
        <h1>SortSmart</h1>
        <p className="subtitle">Find which UBC bin your item belongs in</p>

        <div className="search-box">
          <input
            type="text"
            placeholder="Enter an item"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button onClick={handleSearch}>Search</button>
        </div>

        {loading && <p>Searching...</p>}

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result-card">
            <h2>{result.canonical_name}</h2>
            <p>
              <strong>Bin:</strong> {result.bin_type.bin_name}
            </p>
            <p>
              <strong>Color:</strong> {result.bin_type.color}
            </p>
            <p>
              <strong>Explanation:</strong> {result.explanation}
            </p>
            {result.notes && (
              <p>
                <strong>Notes:</strong> {result.notes}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;