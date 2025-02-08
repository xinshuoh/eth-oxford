import { useEffect, useState } from "react";
import axios from "axios";

interface Debate {
  topic: string;
  summary: string;
}

function App() {
  const [debates, setDebates] = useState<Debate[]>([]);

  useEffect(() => {
    axios
      .get("http://localhost:8000/debates/")
      .then((response) => setDebates(response.data.debates))
      .catch((error) => console.error("Error fetching debates:", error));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold">Crypto Twitter Debate Analyzer</h1>
      <div className="mt-4">
        {debates.length === 0 ? (
          <p>No debates found.</p>
        ) : (
          debates.map((debate, index) => (
            <div key={index} className="border p-4 my-2 rounded">
              <h2 className="font-semibold">{debate.topic}</h2>
              <p>{debate.summary}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
