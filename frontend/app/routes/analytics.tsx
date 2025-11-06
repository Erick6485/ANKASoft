import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { analyticsService } from '../services/api';
import { FiFilter, FiTrendingUp, FiPackage } from 'react-icons/fi';
import './analytics.css';

interface Producto {
  producto_id: number;
  nombre: string;
  categoria: string;
  genero_cliente: string;
  talla: string;
  total_vendido: number;
  ingreso_total: number;
}

interface Talla {
  talla: string;
  genero_cliente: string;
  total_vendido: number;
  num_ventas: number;
}

export default function Analytics() {
  const [productos, setProductos] = useState<Producto[]>([]);
  const [tallas, setTallas] = useState<Talla[]>([]);
  const [cargando, setCargando] = useState(false);

  // Filtros
  const [mes, setMes] = useState<number | ''>('');
  const [categoria, setCategoria] = useState('');
  const [genero, setGenero] = useState('');
  const [limite, setLimite] = useState(10);

  useEffect(() => {
    cargarProductos();
    cargarTallas();
  }, []);

  const cargarProductos = async () => {
    setCargando(true);
    try {
      const data = await analyticsService.getProductosMasVendidos(
        mes || undefined,
        categoria || undefined,
        limite
      );
      setProductos(data.productos || []);
    } catch (error) {
      console.error('Error cargando productos:', error);
    } finally {
      setCargando(false);
    }
  };

  const cargarTallas = async () => {
    try {
      const data = await analyticsService.getRotacionTallas(genero || undefined);
      setTallas(data.rotacion_tallas || []);
    } catch (error) {
      console.error('Error cargando tallas:', error);
    }
  };

  const aplicarFiltros = () => {
    cargarProductos();
    cargarTallas();
  };

  const limpiarFiltros = () => {
    setMes('');
    setCategoria('');
    setGenero('');
    setLimite(10);
  };

  const meses = [
    { value: 1, label: 'Enero' },
    { value: 2, label: 'Febrero' },
    { value: 3, label: 'Marzo' },
    { value: 4, label: 'Abril' },
    { value: 5, label: 'Mayo' },
    { value: 6, label: 'Junio' },
    { value: 7, label: 'Julio' },
    { value: 8, label: 'Agosto' },
    { value: 9, label: 'Septiembre' },
    { value: 10, label: 'Octubre' },
    { value: 11, label: 'Noviembre' },
    { value: 12, label: 'Diciembre' },
  ];

  const categorias = ['ABRIGO', 'BERMUDA', 'BUZOS', 'CAMISAS', 'FALDA', 'JEANS TERMINADOS', 'PANTALONES', 'VESTIDOS', 'POLOS'];
  const generos = ['mujer', 'hombre', 'niño', 'niña'];

  return (
    <Layout>
      <div className="analytics-container">
        {/* Header */}
        <div className="analytics-header">
          <h1>📈 Analytics Profundo</h1>
          <p>Análisis detallado de ventas, productos y tendencias</p>
        </div>

      {/* Filtros */}
      <div className="filtros-panel">
        <div className="filtros-header">
          <FiFilter className="filter-icon" />
          <h3>Filtros de Búsqueda</h3>
        </div>
        
        <div className="filtros-grid">
          <div className="filter-group">
            <label>Mes</label>
            <select value={mes} onChange={(e) => setMes(e.target.value ? Number(e.target.value) : '')}>
              <option value="">Todos los meses</option>
              {meses.map(m => (
                <option key={m.value} value={m.value}>{m.label}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Categoría</label>
            <select value={categoria} onChange={(e) => setCategoria(e.target.value)}>
              <option value="">Todas las categorías</option>
              {categorias.map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Género</label>
            <select value={genero} onChange={(e) => setGenero(e.target.value)}>
              <option value="">Todos los géneros</option>
              {generos.map(gen => (
                <option key={gen} value={gen}>{gen.charAt(0).toUpperCase() + gen.slice(1)}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Límite de Resultados</label>
            <select value={limite} onChange={(e) => setLimite(Number(e.target.value))}>
              <option value={5}>5 productos</option>
              <option value={10}>10 productos</option>
              <option value={20}>20 productos</option>
              <option value={50}>50 productos</option>
            </select>
          </div>
        </div>

        <div className="filtros-actions">
          <button className="btn-aplicar" onClick={aplicarFiltros}>
            <FiTrendingUp />
            Aplicar Filtros
          </button>
          <button className="btn-limpiar" onClick={limpiarFiltros}>
            Limpiar
          </button>
        </div>
      </div>

      {/* Resultados */}
      <div className="analytics-content">
        {/* Productos Más Vendidos */}
        <div className="analytics-section">
          <div className="section-card">
            <h3 className="section-title">
              <FiPackage className="title-icon" />
              Productos Más Vendidos
            </h3>

            {cargando ? (
              <div className="loading-small">
                <div className="spinner-small"></div>
                <p>Cargando datos...</p>
              </div>
            ) : (
              <div className="productos-table">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Producto</th>
                      <th>Categoría</th>
                      <th>Género</th>
                      <th>Talla</th>
                      <th>Unidades</th>
                      <th>Ingresos</th>
                    </tr>
                  </thead>
                  <tbody>
                    {productos.map((producto, index) => (
                      <tr key={producto.producto_id}>
                        <td>
                          <span className="rank-badge">{index + 1}</span>
                        </td>
                        <td className="producto-nombre">{producto.nombre}</td>
                        <td>{producto.categoria}</td>
                        <td>
                          <span className={`genero-badge ${producto.genero_cliente}`}>
                            {producto.genero_cliente}
                          </span>
                        </td>
                        <td>{producto.talla}</td>
                        <td className="text-center">{producto.total_vendido}</td>
                        <td className="text-right ingreso">${producto.ingreso_total.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>

                {productos.length === 0 && (
                  <div className="empty-state">
                    <p>No se encontraron productos con los filtros seleccionados</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Rotación por Tallas */}
        <div className="analytics-section">
          <div className="section-card">
            <h3 className="section-title">
              <FiTrendingUp className="title-icon" />
              Rotación por Tallas
            </h3>

            <div className="tallas-grid">
              {tallas.slice(0, 12).map((talla, index) => (
                <div key={index} className="talla-card">
                  <div className="talla-header">
                    <span className="talla-size">{talla.talla}</span>
                    <span className={`talla-genero ${talla.genero_cliente}`}>
                      {talla.genero_cliente}
                    </span>
                  </div>
                  <div className="talla-stats">
                    <div className="stat-item">
                      <span className="stat-label">Vendidas</span>
                      <span className="stat-value">{talla.total_vendido}</span>
                    </div>
                    <div className="stat-item">
                      <span className="stat-label">Ventas</span>
                      <span className="stat-value">{talla.num_ventas}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {tallas.length === 0 && (
              <div className="empty-state">
                <p>No hay datos de rotación de tallas disponibles</p>
              </div>
            )}
          </div>
        </div>
      </div>

      </div>
    </Layout>
  );
}

