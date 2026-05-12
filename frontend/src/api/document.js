import axios from "axios";
import { API_BASE } from "./config";

// 1️ Upload document
export const uploadDocument = async (file, userId, token) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(
    `${API_BASE}/document/upload?user_id=${userId}`,
    formData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return res.data;
};


// 2️ Fetch documents for user
export const fetchDocuments = async (userId, token) => {
  const res = await axios.get(`${API_BASE}/document/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

// 3️ Delete document
export const deleteDocument = async (docId, token) => {
  const res = await axios.delete(`${API_BASE}/document/delete/${docId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};
