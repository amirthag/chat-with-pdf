import { useState } from "react";
import UploadPdf from "./components/UploadPdf";
import ChatBox from "./components/ChatBox";
import "./styles.css";

function App() {
  const [pdfUploaded, setPdfUploaded] = useState(false);

  return (
    <div className="app">
      <div className="header">📄 Chat with PDF (RAG AI)</div>

      {!pdfUploaded ? (
        <UploadPdf setUploaded={setPdfUploaded} />
      ) : (
        <ChatBox />
      )}
    </div>
  );
}

export default App;