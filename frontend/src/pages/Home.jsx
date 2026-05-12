// src/pages/Home.jsx
import React, { useState } from "react";
import Navbar from "../components/Navbar";
import SummaryCard from "../components/SummaryCard";
import VideoPlayer from "../components/VideoPlayer";
import "../styles/home.css";

import { useAuth } from "../context/AuthContext";
import { uploadDocument } from "../api/document";
import { convertTextToISL, API_BASE } from "../api/convert";

export default function Home() {
  const { user, token } = useAuth();

  const [status, setStatus] = useState("");
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [sentences, setSentences] = useState([]);
  const [videoUrl, setVideoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  
  // GENERATE SUMMARY + ISL VIDEO
 
  const handleGenerateSummary = async () => {
    if (!text && !file) {
      setError("Please upload a document or paste some text.");
      return;
    }

    setLoading(true);
    setError("");
    setSummary("");
    setSentences([]);
    setVideoUrl("");
    setStatus("Starting…");

    try {
      let usedText = text;
      let documentId = null;
      // 1) HANDLE DOCUMENT UPLOAD
      
      if (file) {
        setStatus("Uploading document…");

        const uploadRes = await uploadDocument(file, user?.id, token);
        console.log("UPLOAD RESPONSE:", uploadRes);

        documentId = uploadRes?.document_id || null;

        setStatus("Extracting text from uploaded file…");

        usedText =
          usedText ||
          uploadRes?.text || 
          "";

        setText(usedText);
      }

      
      // VALIDATE TEXT
     
      if (!usedText || usedText.trim().length < 3) {
        setError("No valid text found. Please upload a readable PDF or paste text.");
        setLoading(false);
        return;
      }

      
      // 2) CALL /convert/text-to-isl
      
      setStatus("Generating summary…");

      const payload = {
        user_id: user?.id,
        text: usedText,
        document_id: documentId || 0,
      };

      const convertRes = await convertTextToISL(payload);
      console.log("CONVERT RESPONSE:", convertRes);

      setStatus("Creating simplified sentences…");

      const summaryText =
        convertRes?.summary_text ||
        convertRes?.summary ||
        "";

      const sentencesList =
        convertRes?.simplified_sentences ||
        convertRes?.sentences ||
        [];

      setSummary(summaryText);
      setSentences(sentencesList);

      
      // 3) VIDEO
     
      setStatus("Rendering ISL video… This may take a moment.");

      let videoPath = convertRes?.video_url || "";

      if (videoPath && !videoPath.startsWith("http")) {
        videoPath = `${API_BASE}${videoPath}`;
      }

      console.log("FINAL VIDEO URL:", videoPath);

      setVideoUrl(videoPath);

      if (videoPath) {
        setStatus("Done! Your ISL video is ready 🎉");
      }

    } catch (err) {
      console.error(err);

      let msg =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.response?.data ||
        err.message ||
        "Something went wrong.";

      if (typeof msg !== "string") msg = JSON.stringify(msg);

      setError(msg);
      setStatus("");

    } finally {
      setLoading(false);
    }
  };

  
  // CLEAR EVERYTHING
  
  const clearAll = () => {
    setFile(null);
    setText("");
    setSummary("");
    setSentences([]);
    setVideoUrl("");
    setError("");
    setStatus("");
  };

  return (
    <>
      <Navbar />

      <div className="home-wrapper">
        {/* LEFT PANEL */}
        <div className="left-panel">
          <div className="editor-card">
            <span className="editor-title">Enter or Upload Text</span>

            <textarea
              className="editor-textarea"
              placeholder="Paste your text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />

            <div className="editor-actions">
              <label className="upload-btn">
                <input
                  type="file"
                  accept=".pdf,.doc,.docx"
                  onChange={(e) => setFile(e.target.files[0])}
                  hidden
                />
                ⬆️ Upload Document
              </label>

              {file && (
                <p className="file-label">
                  📄 {file.name.length > 40 ? file.name.slice(0, 40) + "…" : file.name}
                </p>
              )}

              <button className="clear-btn" onClick={clearAll}>
                Clear
              </button>

              {status && (
                <p className="status-text" style={{ color: "#5a4ae3" }}>
                  {status}
                </p>
              )}

              <button
                className="generate-small"
                onClick={handleGenerateSummary}
                disabled={loading}
              >
                {loading ? "Generating..." : "Generate →"}
              </button>
            </div>

            {error && <p className="status-text error">{error}</p>}
          </div>
        </div>

        {/* RIGHT PANEL */}
        <div className="right-panel">
          {summary && (
            <div className="output-card">
              <SummaryCard summary={summary} sentences={sentences} />
            </div>
          )}

          {videoUrl && (
            <div className="output-card">
              <VideoPlayer videoUrl={videoUrl} />
            </div>
          )}
        </div>
      </div>
    </>
  );
}
