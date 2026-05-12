import React, { useState, useEffect } from "react";
import Navbar from "../components/Navbar";
import "../styles/documents.css";

import { useAuth } from "../context/AuthContext";
import { uploadDocument, fetchDocuments, deleteDocument } from "../api/document";

export default function DocumentsPage() {
  const { user, token } = useAuth();

  const [documents, setDocuments] = useState([]);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  // LOAD DOCUMENTS FOR USER
  const loadDocs = async () => {
    try {
      setStatus("Loading documents...");
      const res = await fetchDocuments(user?.id, token);
      setDocuments(res.documents || []);
      setStatus("");
    } catch (err) {
      console.error(err);
      setStatus("Failed to load documents.");
    }
  };

  useEffect(() => {
    loadDocs();
  }, []);

 
  // UPLOAD NEW DOCUMENT
  
  const handleUpload = async () => {
    if (!file) {
      alert("Please choose a PDF/DOC file first.");
      return;
    }

    try {
      setLoading(true);
      setStatus("Uploading document...");

      const res = await uploadDocument(file, user?.id, token);

      if (res) {
        setStatus("Uploaded successfully!");
        setFile(null);
        loadDocs();
      }
    } catch (err) {
      console.error(err);
      setStatus("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  
  // DELETE DOCUMENT
  
  const handleDelete = async (id) => {
    const confirmDelete = window.confirm("Delete this document permanently?");
    if (!confirmDelete) return;

    try {
      await deleteDocument(id, token);
      loadDocs();
    } catch (err) {
      console.error(err);
      alert("Failed to delete.");
    }
  };

  return (
    <>
      <Navbar />

      <div className="docs-wrapper">

        {/* Upload Box */}
        <div className="upload-box">
          <h3>Upload New Document</h3>

          <input
            type="file"
            accept=".pdf,.doc,.docx"
            onChange={(e) => setFile(e.target.files[0])}
          />

          {file && <p className="file-name">📄 {file.name}</p>}

          <button
            className="upload-btn"
            onClick={handleUpload}
            disabled={loading}
          >
            {loading ? "Uploading..." : "Upload"}
          </button>

          {status && <p className="status-text">{status}</p>}
        </div>

        {/* Documents List */}
        <div className="docs-list">
          <h3>Your Documents</h3>

          {documents.length === 0 ? (
            <p className="empty-text">No documents uploaded yet.</p>
          ) : (
            documents.map((doc) => (
              <div className="doc-card" key={doc.id}>
                <div className="doc-info">
                  <h4>📄 {doc.filename}</h4>
                  <p><b>Extracted Text:</b> {doc.text?.slice(0, 120)}...</p>
                  <p className="timestamp">
                    Uploaded: {new Date(doc.created_at).toLocaleString()}
                  </p>
                </div>

                <button
                  className="delete-btn"
                  onClick={() => handleDelete(doc.id)}
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>

      </div>
    </>
  );
}
