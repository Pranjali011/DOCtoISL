import React from "react";
import "../styles/home.css";
import textIcon from "../assets/text-icon.png";

export default function SummaryCard({ summary, sentences }) {
  return (
    <div className="summary-card">
      <div className="summary-header">
        <img src={textIcon} alt="text" className="summary-icon" />
        <h3>Summary</h3>
      </div>

      <p className="summary-text">{summary}</p>

      <h4 className="summary-subheader">Simplified Sentences</h4>

      <ul className="sentence-list">
        {sentences.map((s, i) => (
          <li key={i}>{s}</li>
        ))}
      </ul>
    </div>
  );
}
