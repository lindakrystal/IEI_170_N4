import { useEffect, useState } from 'react';
import api from '../api';

export default function ProductosPage() {
  const [productos, setProductos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [nuevo, setNuevo] = useState({
    sku: '',
    nombre: '',
    descripcion: '',
    categoria: '',
    proveedor: '',
    stock_minimo: 0,
    precio: 0,
  });
  const [error, setError] = useState('');

  const cargarProductos = async () => {
    setLoading(true);
    try {
      const res = await api.get('/api/productos/');
      setProductos(res.data.results || res.data);
    } catch (err) {
      console.error(err.response?.data || err);
      setError('Error al cargar productos');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarProductos();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNuevo(prev => ({ ...prev, [name]: value }));
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    try {
      await api.post('/api/productos/', {
        sku: nuevo.sku,
        nombre: nuevo.nombre,
        descripcion: nuevo.descripcion,
        categoria: nuevo.categoria,
        proveedor: nuevo.proveedor,
        stock_minimo: Number(nuevo.stock_minimo),
        precio: Number(nuevo.precio),
      });

      setNuevo({
        sku: '',
        nombre: '',
        descripcion: '',
        categoria: '',
        proveedor: '',
        stock_minimo: 0,
        precio: 0,
      });

      cargarProductos();
    } catch (err) {
      console.error(err.response?.data || err);
      setError('Error al crear producto (IDs de categoría o proveedor incorrectos)');
    }
  };

  return (
    <div style={{ padding: '1.5rem' }}>
      <h2>Productos</h2>

      <section style={{ marginBottom: '2rem' }}>
        <h3>Nuevo producto</h3>
        <form onSubmit={handleCreate} style={{ display: 'grid', gap: '0.5rem', maxWidth: 500 }}>
          <input name="sku" placeholder="SKU" value={nuevo.sku} onChange={handleChange} />
          <input name="nombre" placeholder="Nombre" value={nuevo.nombre} onChange={handleChange} />
          <textarea name="descripcion" placeholder="Descripción" value={nuevo.descripcion} onChange={handleChange} />
          <input name="categoria" placeholder="ID categoría" value={nuevo.categoria} onChange={handleChange} />
          <input name="proveedor" placeholder="ID proveedor" value={nuevo.proveedor} onChange={handleChange} />
          <input name="stock_minimo" type="number" placeholder="Stock mínimo" value={nuevo.stock_minimo} onChange={handleChange} />
          <input name="precio" type="number" placeholder="Precio" value={nuevo.precio} onChange={handleChange} />

          {error && <p style={{ color: 'red' }}>{error}</p>}
          <button type="submit">Guardar producto</button>
        </form>
      </section>

      <section>
        <h3>Listado de productos</h3>
        {loading ? (
          <p>Cargando...</p>
        ) : (
          <table border="1" cellPadding="6">
            <thead>
              <tr>
                <th>ID</th>
                <th>SKU</th>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Proveedor</th>
                <th>Stock</th>
                <th>Stock mínimo</th>
                <th>Precio</th>
              </tr>
            </thead>
            <tbody>
              {productos.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.sku}</td>
                  <td>{p.nombre}</td>
                  <td>{p.categoria_nombre}</td>
                  <td>{p.proveedor_nombre}</td>
                  <td>{p.stock}</td>
                  <td>{p.stock_minimo}</td>
                  <td>{p.precio}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  );
}
