// src/api.js
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

// Guarda y carga token desde localStorage
export const setAuthToken = (token) => {
  if (token) {
    localStorage.setItem("token", token);
    api.defaults.headers.common["Authorization"] = `Token ${token}`;
  } else {
    localStorage.removeItem("token");
    delete api.defaults.headers.common["Authorization"];
  }
};

export const getStoredToken = () => {
  return localStorage.getItem("token");
};

// Si tu token REAL es fijo, colócalo aquí temporalmente
const TOKEN = "56819e91f76401ddc6cf5331987f6c28b21ea04f";

// Crear cliente axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    Authorization: `Token ${TOKEN}`,
    "Content-Type": "application/json",
  },
});

export default api;

// ---------------- API PRODUCTOS ---------------- //

export const getProductos = async () => {
  const res = await api.get("/api/productos/");
  return res.data.results || [];
};

export const crearProducto = async (data) => {
  const res = await api.post("/api/productos/", data);
  return res.data;
};
