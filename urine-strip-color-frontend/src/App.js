import React, { useState } from "react";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [colors, setColors] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("image", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setColors(data.colors);
      } else {
        console.error("Error uploading image");
        setError("Error uploading image");
      }
    } catch (error) {
      console.error("Error: " + error.message);
      setError("Error: " + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1 className="mt-5">Color Detection</h1>
        <div className="input-group mt-3">
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="form-control"
          />
          <button
            className="btn btn-primary"
            onClick={handleUpload}
            disabled={isLoading}
          >
            {isLoading ? "Uploading..." : "Upload"}
          </button>
        </div>
        {error && <p className="text-danger mt-2">{error}</p>}
        <h2 className="mt-4">Detected Colors:</h2>
        <div className="color-boxes">
          {colors.map((color, index) => (
            <div
              key={index}
              className="color-box"
              style={{
                backgroundColor: `rgb(${color[0]}, ${color[1]}, ${color[2]})`,
              }}
            ></div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;
