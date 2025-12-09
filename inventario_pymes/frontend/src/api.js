import axios from "axios";

// URL backend Django
const API_URL = "http://127.0.0.1:8000";

// Instancia de axios
const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Obtener token guardado
export function getStoredToken() {
  return localStorage.getItem("token");
}

// Guardar token y aplicarlo
export function setAuthToken(token) {
  localStorage.setItem("token", token);
  api.defaults.headers.common["Authorization"] = `Token ${token}`;
}

// Cargar token si ya existe
const token = getStoredToken();
if (token) {
  api.defaults.headers.common["Authorization"] = `Token ${token}`;
}

// --------------------
// LOGIN
// --------------------
export async function login(username, password) {
  const response = await api.post("/api/login/", { username, password });
  return response.data; // { token: "..." }
}

// --------------------
// PRODUCTOS
// --------------------
export async function getProductos() {
  const response = await api.get("/api/productos/");
  return response.data;
}

export async function crearProducto(data) {
  const response = await api.post("/api/productos/", data);
  return response.data;
}

export default api;
