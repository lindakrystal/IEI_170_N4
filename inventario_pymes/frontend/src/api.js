import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export function getStoredToken() {
  return localStorage.getItem("token");
}

export function setAuthToken(token) {
  localStorage.setItem("token", token);
  api.defaults.headers.common["Authorization"] = `Token ${token}`;
}

const token = getStoredToken();
if (token) {
  api.defaults.headers.common["Authorization"] = `Token ${token}`;
}

// LOGIN
export async function login(username, password) {
  const res = await api.post("/login/", { username, password });
  return res.data;
}

// PRODUCTOS
export async function getProductos() {
  const res = await api.get("/productos/");
  return res.data;
}

export async function crearProducto(data) {
  const res = await api.post("/productos/", data);
  return res.data;
}

// IA
export async function getIAReposicion() {
  const res = await api.get("/ia/reposicion/");
  return res.data;
}

export async function getIAAnomalias() {
  const res = await api.get("/ia/anomalias/");
  return res.data;
}

export async function sugerirCategoria(nombre, descripcion) {
  const res = await api.post("/ia/sugerir-categoria/", {
    nombre,
    descripcion,
  });
  return res.data;
}

export default api;
