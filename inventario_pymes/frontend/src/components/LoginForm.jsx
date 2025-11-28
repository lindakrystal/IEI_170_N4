import { useState } from 'react';
import api, { setAuthToken } from '../api';

export default function LoginForm({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    console.log("🔍 Enviando login con:", { username, password });

    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const res = await api.post(
        '/api/token/',
        params,
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );

      console.log("✔ Token recibido:", res.data);

      const token = res.data.token;
      setAuthToken(token);
      onLogin(token);

    } catch (err) {
      console.error("❌ Error en login:", err.response?.data || err);
      setError('Usuario o contraseña incorrectos');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <h2>Iniciar sesión</h2>
      <form onSubmit={handleSubmit}>

        <div style={{ marginBottom: '1rem' }}>
          <label>Usuario</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <label>Contraseña</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          />
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <button type="submit" style={{ padding: '10px 16px' }}>
          Entrar
        </button>
      </form>
    </div>
  );
}

