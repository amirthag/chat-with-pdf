import { useState, useRef } from "react";
import API from "../api";

export default function UploadPdf({ setUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const inputRef = useRef();

  const uploadFile = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);

    try {
      const res = await API.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (e) => {
          setProgress(Math.round((e.loaded * 100) / e.total));
        },
      });

      alert(`Uploaded!\nPages: ${res.data.pages}`);

      setUploaded(true);
      setFile(null);

    } catch (err) {
      console.error(err);
      alert("Upload failed. Check backend.");
    }

    setLoading(false);
    setProgress(0);
  };

  return (
    <div className="upload">

      <input
        type="file"
        ref={inputRef}
        hidden
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={() => inputRef.current.click()}>
        Select PDF
      </button>

      {file && <p>{file.name}</p>}

      {loading && (
        <div>
          Uploading... {progress}%
        </div>
      )}

      <button onClick={uploadFile} disabled={!file || loading}>
        Upload
      </button>

    </div>
  );
}