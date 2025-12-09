import { useState } from "react";
import { login, setAuthToken } from "./api";

export default function Login({ onLogin }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // Llama a la función login definida en api.js
      const res = await login(form.username, form.password);

      // res = { token: "xxxx" }
      const token = res.token;

      // Guarda token en localStorage + axios
      setAuthToken(token);

      // Cambia estado a logueado en App.jsx
      onLogin();

    } catch (err) {
      console.error("Error login:", err);
      setError("Usuario o contraseña incorrectos");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0f1117]">
      <form
        onSubmit={handleSubmit}
        className="bg-[#1a1d27] p-6 rounded-xl border border-gray-700 w-80 text-white"
      >
        <h2 className="text-xl mb-4 text-center">Iniciar sesión</h2>

        <input
          name="username"
          placeholder="Usuario"
          onChange={handleChange}
          className="w-full p-3 mb-3 bg-[#11131a] border border-gray-700 rounded"
        />

        <input
          type="password"
          name="password"
          placeholder="Contraseña"
          onChange={handleChange}
          className="w-full p-3 mb-3 bg-[#11131a] border border-gray-700 rounded"
        />

        {error && <p className="text-red-400 text-sm mb-2">{error}</p>}

        <button
          type="submit"
          className="w-full bg-blue-600 py-2 rounded hover:bg-blue-700"
        >
          Entrar
        </button>
      </form>
    </div>
  );
}
