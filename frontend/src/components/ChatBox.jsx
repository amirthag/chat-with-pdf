import { useState, useRef, useEffect } from "react";
import API from "../api";

export default function ChatBox() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const chatRef = useRef(null);

  useEffect(() => {
    chatRef.current.scrollTop = chatRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMsg = query;
    setQuery("");

    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);

    try {
      const res = await API.post("/ask", { query: userMsg });

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: res.data.answer,
          source: res.data.source
        }
      ]);

    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error fetching response" }
      ]);
    }
  };

  return (
    <div className="chat-container">

      <div className="chat-box" ref={chatRef}>

        {messages.map((m, i) => (
          <div key={i} className={m.role === "user" ? "user" : "bot"}>

            <div>{m.text}</div>

            {m.source && (
              <div className="sources">
                📄 Page {m.source.page}
              </div>
            )}

          </div>
        ))}

      </div>

      <div className="input-bar">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />

        <button onClick={sendMessage}>
          Send
        </button>
      </div>

    </div>
  );
}