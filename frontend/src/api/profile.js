import axios from "axios";
import { API_BASE } from "./config";

export const getProfile = async (userId, token) => {
  const res = await axios.get(`${API_BASE}/profile/${userId}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.data;
};

export const updateProfile = async (userId, data, token) => {
  const res = await axios.put(`${API_BASE}/profile/${userId}`, data, {
    headers: { Authorization: `Bearer ${token}` }
  });
  return res.data;
};
