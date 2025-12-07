// src/api.js
import axios from "axios";

const API_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ---------------------------
// TOKEN: guardar / cargar
// ---------------------------

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

// Al iniciar la app, si hay token guardado → usarlo
const stored = getStoredToken();
if (stored) {
  api.defaults.headers.common["Authorization"] = `Token ${stored}`;
}

// ---------------------------
//         LOGIN
// ---------------------------

export const login = async (username, password) => {
  const res = await api.post("/api/token/login/", {
    username,
    password,
  });

  const token = res.data.token;
  setAuthToken(token);

  return res.data;
};

// ---------------------------
//        PRODUCTOS
// ---------------------------

export const getProductos = async () => {
  const res = await api.get("/api/productos/");
  return res.data.results || [];
};

export const crearProducto = async (data) => {
  const res = await api.post("/api/productos/", data);
  return res.data;
};
