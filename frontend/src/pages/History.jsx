import React, { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import HistoryItem from "../components/HistoryItem";
import { useAuth } from "../context/AuthContext";
import axios from "axios";
import "../styles/history.css";

export default function History() {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    if (!user) return;

    axios
      .get(`http://127.0.0.1:8000/history/${user.id}`)
      .then((res) => setHistory(res.data))
      .catch((err) => console.error(err));
  }, [user]);

  return (
    <>
      <Navbar />

      <div className="history-wrapper">
        <h2 className="history-title">Your Past Conversions</h2>

        {history.length === 0 && (
          <p className="empty-history">No past summaries found.</p>
        )}

        {history.map((item) => (
          <HistoryItem key={item.summary_id} item={item} onClick={setSelected} />
        ))}
      </div>

      {selected && (
        <div className="history-popup">
          <div className="popup-content">
            <button className="popup-close" onClick={() => setSelected(null)}>
              ✕
            </button>

            <h3>{selected.filename}</h3>
            <p className="popup-summary">{selected.summary_text}</p>

            {selected.wordcloud && (
              <img
                src={`http://127.0.0.1:8000${selected.wordcloud}`}
                className="popup-wordcloud"
                alt="word cloud"
              />
            )}

            {selected.video_url && (
              <video
                controls
                className="popup-video"
                src={`http://127.0.0.1:8000${selected.video_url}`}
              />
            )}
          </div>
        </div>
      )}
    </>
  );
}
