// src/api/convert.js
import axios from "axios";

export const API_BASE = "http://127.0.0.1:8000";

// POST /convert/text-to-isl
// body: { user_id, document_id?, text }
export const convertTextToISL = async ({ user_id, document_id, text, token }) => {
  const res = await axios.post(
    `${API_BASE}/convert/text-to-isl`,
    {
      user_id: user_id,
      document_id: document_id || null,
      text: text
    },
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    }
  );

  return res.data;
};


// POST /convert/summary-to-isl/{summary_id}
export async function convertSummaryToISL({ summaryId, token }) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await axios.post(
    `${API_BASE}/convert/summary-to-isl/${summaryId}`,
    {},
    { headers }
  );
  return res.data;
}
