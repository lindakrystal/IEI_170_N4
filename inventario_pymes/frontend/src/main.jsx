import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import { setAuthToken, getStoredToken } from "./api";

// 🔥 Cargar token desde localStorage o establecer uno manualmente
const token = getStoredToken();

if (token) {
  // Ya existe token guardado
  setAuthToken(token);
} else {
  // ❗️PON AQUÍ TU TOKEN REAL
  const tokenManual = "PEGAR_AQUI_TU_TOKEN_REAL";

  if (tokenManual && tokenManual !== "PEGAR_AQUI_TU_TOKEN_REAL") {
    setAuthToken(tokenManual);
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>
)
