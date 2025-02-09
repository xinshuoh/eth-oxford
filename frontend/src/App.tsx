import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

// interface Debate {
//   title: string;
//   summary: string;
// }

function App() {
  const [debates, setDebates] = useState<[]>([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/debates/")
      .then((response) => setDebates(response.data.debates))
      .catch((error) => console.error("Error fetching debates:", error));
  }, []);

  return (
    <div className="app-container">
      <h1 className="header-title">Crypto Twitter Debate Analyzer</h1>

      <div className="debates-container">
        {debates.length === 0 ? (
          <p className="no-debates">No debates found. 📭</p>
        ) : (
          debates.map((debate, index) => (
            <div key={index} className="debate-card">
              <h2 className="debate-title">📢 {debate[1]}</h2>
              <p className="debate-summary">{debate[3]}</p>
              <button className="read-more-btn">Read More</button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
