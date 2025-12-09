import { useEffect, useState } from "react";
import { getProductos, crearProducto } from "./api";

export default function ProductosPage() {
  const [productos, setProductos] = useState([]);
  const [form, setForm] = useState({});
  const [error, setError] = useState("");

  useEffect(() => {
    cargarProductos();
  }, []);

  const cargarProductos = async () => {
    try {
      const data = await getProductos();
      setProductos(data);
      setError("");
    } catch {
      setError("Error al cargar productos");
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await crearProducto(form);
      cargarProductos();
    } catch {
      setError("Error al guardar producto");
    }
  };

  return (
    <div className="min-h-screen bg-[#0f1117] text-gray-100 p-10">

      <h1 className="text-4xl font-bold mb-10 text-center">
        Sistema Inventario PYMEs 🛒
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

        <div className="bg-[#1a1d27] p-6 rounded-xl border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">Agregar producto</h2>

          <div className="grid grid-cols-1 gap-4">
            {[ 
              ["sku", "SKU"],
              ["nombre", "Nombre"],
              ["descripcion", "Descripción"],
              ["categoria", "ID Categoría"],
              ["proveedor", "ID Proveedor"],
              ["stock_minimo", "Stock mínimo"],
              ["precio", "Precio"],
            ].map(([campo, label]) => (
              <input
                key={campo}
                name={campo}
                placeholder={label}
                onChange={handleChange}
                className="p-3 rounded-lg bg-[#11131a] border border-gray-700 focus:ring focus:ring-blue-500 outline-none"
              />
            ))}

            <button
              onClick={handleSubmit}
              className="bg-blue-600 py-3 rounded-lg font-medium hover:bg-blue-700 transition"
            >
              Guardar producto
            </button>

            {error && (
              <p className="text-red-400 text-sm mt-2">{error}</p>
            )}
          </div>
        </div>

        <div className="bg-[#1a1d27] p-6 rounded-xl border border-gray-800">
          <h2 className="text-xl font-semibold mb-4">Productos registrados</h2>

          <div className="overflow-x-auto">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-[#11131a] text-gray-300">
                  {[
                    "ID",
                    "SKU",
                    "Nombre",
                    "Categoría",
                    "Proveedor",
                    "Stock mín",
                    "Precio",
                  ].map((th) => (
                    <th key={th} className="p-3 border-b border-gray-700">
                      {th}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {productos.map((p) => (
                  <tr
                    key={p.id}
                    className="hover:bg-[#161922] transition border-b border-gray-800"
                  >
                    <td className="p-3">{p.id}</td>
                    <td className="p-3">{p.sku}</td>
                    <td className="p-3">{p.nombre}</td>
                    <td className="p-3">{p.categoria}</td>
                    <td className="p-3">{p.proveedor}</td>
                    <td className="p-3">{p.stock_minimo}</td>
                    <td className="p-3">${p.precio}</td>
                  </tr>
                ))}

                {productos.length === 0 && (
                  <tr>
                    <td
                      className="text-center py-4 text-gray-400"
                      colSpan="7"
                    >
                      No hay productos registrados.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>
    </div>
  );
}
