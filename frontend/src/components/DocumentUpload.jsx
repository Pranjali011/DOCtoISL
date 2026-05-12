import React from "react";
import uploadIcon from "../assets/upload-icon.png";
import "../styles/home.css";

export default function DocumentUpload({ onFileSelect }) {
  return (
    <div className="upload-wrapper">
      <div className="upload-header">
        <img src={uploadIcon} className="upload-small-icon" alt="upload" />
        <span className="upload-title-text">Upload Document</span>
      </div>

      <input
        type="file"
        accept=".pdf,.doc,.docx"
        onChange={(e) => onFileSelect(e.target.files[0])}
        className="upload-input"
      />

      <p className="upload-note">only PDF/DOC files are supported</p>
    </div>
  );
}
