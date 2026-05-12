import axios from "axios";

const API = "http://127.0.0.1:8000";

export const signupUser = async (username, email, password) => {
  const res = await axios.post(`${API}/auth/signup`, {
    username,
    email,
    password,
  });
  return res.data;
};

export const loginUser = async (email, password) => {
  const res = await axios.post(`${API}/auth/login`, {
    email,
    password,
  });
  return res.data;
};
