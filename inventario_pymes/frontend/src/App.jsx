import { useEffect, useState } from "react";
import Login from "./Login";
import ProductosPage from "./ProductosPage";
import { getStoredToken } from "./api";

export default function App() {
  const [logueado, setLogueado] = useState(false);

  useEffect(() => {
    const token = getStoredToken();
    if (token) {
      setLogueado(true);
    }
  }, []);

  if (!logueado) {
    return <Login onLogin={() => setLogueado(true)} />;
  }

  return <ProductosPage />;
}

