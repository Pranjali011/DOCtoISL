import axios from "axios";

export const API_BASE = "http://127.0.0.1:8000";

export const fetchHistory = async (userId, token) => {
  const res = await axios.get(`${API_BASE}/history/${userId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  return res.data;
};
