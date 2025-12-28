// ==========================
// GRÁFICOS (Chart.js)
// ==========================
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend
);

// ==========================
// REACT + API
// ==========================
import { useEffect, useState } from "react";
import {
  getProductos,
  crearProducto,
  getIAReposicion,
} from "./api";

export default function ProductosPage() {
  const [productos, setProductos] = useState([]);
  const [reposicion, setReposicion] = useState([]);
  const [form, setForm] = useState({});
  const [error, setError] = useState("");

  // ==========================
  // CARGA INICIAL
  // ==========================
  useEffect(() => {
    cargarProductos();
    cargarIAReposicion();
  }, []);

  // ==========================
  // PRODUCTOS
  // ==========================
  const cargarProductos = async () => {
    try {
      const data = await getProductos();
      setProductos(data);
      setError("");
    } catch (e) {
      console.error(e);
      setError("Error al cargar productos");
    }
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    try {
      await crearProducto(form);
      setForm({});
      cargarProductos();
      cargarIAReposicion(); // recalcula IA
    } catch (e) {
      console.error(e);
      setError("Error al guardar producto");
    }
  };

  // ==========================
  // IA – REPOSICIÓN
  // ==========================
  const cargarIAReposicion = async () => {
    try {
      const data = await getIAReposicion();
      setReposicion(data);
    } catch (e) {
      console.error(e);
    }
  };

  // ==========================
  // COLORES POR NIVEL
  // ==========================
  const colorNivel = (nivel) => {
    switch (nivel) {
      case "critico":
        return "bg-red-900/40 text-red-300 border-red-800";
      case "atencion":
        return "bg-yellow-900/40 text-yellow-300 border-yellow-800";
      case "ok":
        return "bg-green-900/40 text-green-300 border-green-800";
      default:
        return "bg-gray-800 text-gray-300 border-gray-700";
    }
  };

  // ==========================
  // DATOS GRÁFICO IA
  // ==========================
  const dataGrafico = {
    labels: reposicion.map((r) => r.nombre),
    datasets: [
      {
        label: "Reposición sugerida",
        data: reposicion.map((r) => r.reponer_sugerido),
        backgroundColor: "#3b82f6",
      },
    ],
  };

  // ==========================
  // RENDER
  // ==========================
  return (
    <div className="min-h-screen bg-[#0f1117] text-gray-100 p-10">

      {/* ================= TÍTULO ================= */}
      <h1 className="text-4xl font-bold mb-10 text-center">
        Sistema Inventario PYMEs 🛒
      </h1>

      {/* ================= GRID ================= */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10">

        {/* ================= FORMULARIO ================= */}
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
                value={form[campo] || ""}
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

        {/* ================= TABLA PRODUCTOS ================= */}
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

      {/* ================= IA + GRÁFICO ================= */}
      <div className="mt-12 bg-[#1a1d27] p-6 rounded-xl border border-gray-800">
        <h2 className="text-xl font-semibold mb-6">
          🤖 Reposición sugerida por IA
        </h2>

        {reposicion.length === 0 && (
          <p className="text-gray-400 text-sm">
            La IA aún no tiene suficiente información.
          </p>
        )}

        {reposicion.length > 0 && (
          <>
            <div className="mb-8">
              <Bar data={dataGrafico} />
            </div>

            <div className="space-y-3">
              {reposicion.map((r) => (
                <div
                  key={r.producto_id}
                  className={`flex justify-between items-center p-3 rounded-lg border ${colorNivel(
                    r.nivel
                  )}`}
                >
                  <span>
                    <strong>{r.nombre}</strong>{" "}
                    <span className="opacity-70 text-sm">({r.sku})</span>
                  </span>

                  <span className="text-sm font-semibold">
                    Reponer: {r.reponer_sugerido}
                  </span>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
}
