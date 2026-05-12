// src/pages/HistoryDetails.jsx
import React from "react";
import { useLocation } from "react-router-dom";
import Navbar from "../components/Navbar";
import VideoPlayer from "../components/VideoPlayer";
import "../styles/history.css";
import { API_BASE } from "../api/convert";

export default function HistoryDetails() {
  const { state } = useLocation();
  const item = state?.item;

  if (!item) {
    return <h2>No history data found</h2>;
  }

  return (
    <>
      <Navbar />

      <div className="history-details-wrapper">
        <h2 className="details-title">{item.filename}</h2>

        {/* SUMMARY */}
        <div className="details-card">
          <h3 className="details-heading">Summary</h3>
          <p className="details-text">{item.summary_text}</p>
        </div>

        {/* WORDCLOUD */}
        {item.wordcloud && (
          <div className="details-card">
            <h3 className="details-heading">Wordcloud</h3>

            <img
              src={`${API_BASE}${item.wordcloud}`}
              alt="Wordcloud"
              className="details-wordcloud"
            />
          </div>
        )}

        {/* ISL VIDEO */}
        {item.isl_video && (
          <div className="details-card">
            <h3 className="details-heading">ISL Video</h3>

            <VideoPlayer videoUrl={`${API_BASE}${item.isl_video}`} />
          </div>
        )}
      </div>
    </>
  );
}
