import React from "react";
import "../styles/history.css";

export default function HistoryItem({ item, onClick }) {
  return (
    <div className="history-item" onClick={() => onClick(item)}>
      <div className="history-item-left">
        <p className="history-filename">📄 {item.filename}</p>
        <p className="history-date">
          {new Date(item.created_at).toLocaleString()}
        </p>
      </div>

      <div className="history-item-right">
        {item.wordcloud && (
          <img
            src={`http://127.0.0.1:8000${item.wordcloud}`}
            alt="wordcloud"
            className="history-icon"
          />
        )}

        {item.video_url && (
          <span className="history-video-btn">🎥</span>
        )}
      </div>
    </div>
  );
}
