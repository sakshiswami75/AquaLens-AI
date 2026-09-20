import { useState } from "react";
import { Droplets, Search, Leaf, ArrowRight } from "lucide-react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [source, setSource] = useState("");
  const [loading, setLoading] = useState(false);

  const askAquaLens = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSource("");

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question,
        }),
      });

      const data = await response.json();

      setAnswer(data.answer);
      setSource(data.source);
    } catch (error) {
      setAnswer(
        "Unable to connect to AquaLens. Please make sure the backend is running."
      );
    }

    setLoading(false);
  };

  const exampleQuestions = [
    "What is the water footprint of rice?",
    "Why does cotton use water?",
    "How can we save water in rice farming?",
  ];

  return (
    <div className="app">
      <nav className="navbar">
        <div className="logo">
          <Droplets size={24} />
          <span>AquaLens</span>
        </div>

        <div className="nav-tag">
          <Leaf size={16} />
          <span>Water • Sustainability • AI</span>
        </div>
      </nav>

      <main className="main">
        <section className="hero">
          <div className="badge">
            <Droplets size={15} />
            AI-powered water intelligence
          </div>

          <h1>
            See the water behind
            <span> what you consume.</span>
          </h1>

          <p className="subtitle">
            AquaLens helps you understand the hidden water footprint of
            everyday products using trusted knowledge and IBM Granite AI.
          </p>

          <div className="search-box">
            <Search size={21} />

            <input
              type="text"
              placeholder="Ask about a product or water footprint..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  askAquaLens();
                }
              }}
            />

            <button onClick={askAquaLens} disabled={loading}>
              {loading ? "Thinking..." : "Ask AquaLens"}
              {!loading && <ArrowRight size={17} />}
            </button>
          </div>

          <div className="examples">
            <span>Try asking:</span>

            {exampleQuestions.map((item) => (
              <button
                key={item}
                onClick={() => setQuestion(item)}
              >
                {item}
              </button>
            ))}
          </div>
        </section>

        {answer && (
          <section className="result">
            <div className="result-header">
              <div className="result-icon">
                <Droplets size={20} />
              </div>

              <div>
                <p className="result-label">AquaLens AI</p>
                <h2>Your answer</h2>
              </div>
            </div>

            <div className="answer">
              {answer}
            </div>

            {source && (
              <details className="source">
                <summary>View retrieved knowledge</summary>
                <p>{source}</p>
              </details>
            )}
          </section>
        )}

        <section className="why">
          <div>
            <p className="section-label">WHY IT MATTERS</p>
            <h2>
              Every product has a
              <br />
              water story.
            </h2>
          </div>

          <p>
            Water is hidden in the production of the food, clothes, and
            products we use every day. AquaLens makes that information easier
            to understand so people can make more informed choices.
          </p>
        </section>
      </main>

      <footer>
        <span>Built for sustainable consumption</span>
        <span>SDG 6 • SDG 12 • SDG 13</span>
      </footer>
    </div>
  );
}

export default App;