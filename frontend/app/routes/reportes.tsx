import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { FiFileText, FiDownload, FiFilter, FiBarChart, FiPieChart, FiTrendingUp } from 'react-icons/fi';
import './reportes.css';

interface ReporteDashboard {
  periodo: string;
  resumen_general: {
    ventas: {
      total_transacciones: number;
      total_ingresos: string;
      ticket_promedio: string;
    };
    inventario: {
      total_productos: number;
      valor_inventario: string;
      productos_criticos: number;
      nivel_servicio: string;
    };
    operaciones: {
      sucursales_activas: number;
      ventas_por_sucursal: string;
    };
  };
  reportes_disponibles: string[];
}

export default function Reportes() {
  const [reporteData, setReporteData] = useState<ReporteDashboard | null>(null);
  const [cargando, setCargando] = useState(true);
  const [reporteSeleccionado, setReporteSeleccionado] = useState('');

  useEffect(() => {
    cargarDashboardReportes();
  }, []);

  const cargarDashboardReportes = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/reportes/dashboard', {
        headers: {
          'X-API-Key': 'retail_hackaton_2025_fup'
        }
      });
      const data = await response.json();
      setReporteData(data);
    } catch (error) {
      console.error('Error cargando dashboard reportes:', error);
    } finally {
      setCargando(false);
    }
  };

  const generarReporte = (tipo: string) => {
    setReporteSeleccionado(tipo);
    console.log(`Generando reporte: ${tipo}`);
    // Aquí se haría la descarga real del reporte
    setTimeout(() => {
      alert(`Reporte "${tipo}" generado exitosamente (Demo)`);
      setReporteSeleccionado('');
    }, 1000);
  };

  if (cargando) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando dashboard de reportes...</p>
        </div>
      </Layout>
    );
  }

  if (!reporteData) {
    return (
      <Layout>
        <div className="error-container">
          <p>Error al cargar reportes. Verifica que el backend esté corriendo.</p>
        </div>
      </Layout>
    );
  }

  const { resumen_general } = reporteData;

  return (
    <Layout>
      <div className="reportes-container">
        <div className="reportes-header">
          <h1> Centro de Reportes</h1>
          <p>Genera y descarga reportes completos del sistema</p>
          <span className="periodo-badge">{reporteData.periodo}</span>
        </div>

        {/* Resumen Ejecutivo */}
        <div className="resumen-ejecutivo">
          <h3 className="section-title"> Resumen Ejecutivo</h3>
          
          <div className="resumen-grid">
            {/* Ventas */}
            <div className="resumen-card ventas">
              <h4> Ventas</h4>
              <div className="resumen-items">
                <div className="resumen-item">
                  <span className="item-label">Transacciones:</span>
                  <span className="item-value">{resumen_general.ventas?.total_transacciones || 0}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Ingresos:</span>
                  <span className="item-value highlight">{resumen_general.ventas?.total_ingresos || '$0.00'}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Ticket Promedio:</span>
                  <span className="item-value">{resumen_general.ventas?.ticket_promedio || '$0.00'}</span>
                </div>
              </div>
            </div>

            {/* Inventario */}
            <div className="resumen-card inventario">
              <h4> Inventario</h4>
              <div className="resumen-items">
                <div className="resumen-item">
                  <span className="item-label">Total Productos:</span>
                  <span className="item-value">{resumen_general.inventario?.total_productos || 0}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Valor Total:</span>
                  <span className="item-value highlight">{resumen_general.inventario?.valor_inventario || '$0.00'}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Nivel Servicio:</span>
                  <span className="item-value">{resumen_general.inventario?.nivel_servicio || '0%'}</span>
                </div>
              </div>
            </div>

            {/* Operaciones */}
            <div className="resumen-card operaciones">
              <h4> Operaciones</h4>
              <div className="resumen-items">
                <div className="resumen-item">
                  <span className="item-label">Sucursales Activas:</span>
                  <span className="item-value">{resumen_general.operaciones?.sucursales_activas || 0}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Productos Críticos:</span>
                  <span className="item-value critical">{resumen_general.inventario?.productos_criticos || 0}</span>
                </div>
                <div className="resumen-item">
                  <span className="item-label">Ventas/Sucursal:</span>
                  <span className="item-value">{resumen_general.operaciones?.ventas_por_sucursal || '0'}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Reportes Disponibles */}
        <div className="reportes-section">
          <h3 className="section-title">
            <FiFileText />
            Reportes Disponibles para Generar
          </h3>

          <div className="reportes-grid">
            {/* Reporte de Ventas */}
            <div className="reporte-card">
              <div className="reporte-icon ventas">
                <FiBarChart />
              </div>
              <div className="reporte-content">
                <h4>Reporte Completo de Ventas</h4>
                <p>Análisis detallado de ventas por categoría, género y sucursal</p>
                <ul className="reporte-incluye">
                  <li> Ventas por categoría</li>
                  <li> Distribución por género</li>
                  <li> Performance por sucursal</li>
                  <li> Top productos vendidos</li>
                </ul>
              </div>
              <button 
                className="btn-generar"
                onClick={() => generarReporte('Ventas Completo')}
                disabled={reporteSeleccionado === 'Ventas Completo'}
              >
                <FiDownload />
                {reporteSeleccionado === 'Ventas Completo' ? 'Generando...' : 'Generar PDF'}
              </button>
            </div>

            {/* Reporte de Inventario */}
            <div className="reporte-card">
              <div className="reporte-icon inventario">
                <FiPieChart />
              </div>
              <div className="reporte-content">
                <h4>Reporte de Inventario</h4>
                <p>Estado completo del inventario con valorización</p>
                <ul className="reporte-incluye">
                  <li> Estado por categoría</li>
                  <li> Valorización total</li>
                  <li> Productos críticos</li>
                  <li> Métricas de rotación</li>
                </ul>
              </div>
              <button 
                className="btn-generar"
                onClick={() => generarReporte('Inventario')}
                disabled={reporteSeleccionado === 'Inventario'}
              >
                <FiDownload />
                {reporteSeleccionado === 'Inventario' ? 'Generando...' : 'Generar Excel'}
              </button>
            </div>

            {/* Reporte de Rendimiento por Sucursales */}
            <div className="reporte-card">
              <div className="reporte-icon sucursales">
                <FiTrendingUp />
              </div>
              <div className="reporte-content">
                <h4>Rendimiento por Sucursales</h4>
                <p>Comparativa y ranking de sucursales</p>
                <ul className="reporte-incluye">
                    <li> Ranking de sucursales</li>
                  <li> KPIs por ubicación</li>
                  <li> Top productos por tienda</li>
                  <li> Comparativa mensual</li>
                </ul>
              </div>
              <button 
                className="btn-generar"
                onClick={() => generarReporte('Sucursales')}
                disabled={reporteSeleccionado === 'Sucursales'}
              >
                <FiDownload />
                {reporteSeleccionado === 'Sucursales' ? 'Generando...' : 'Generar PDF'}
              </button>
            </div>

            {/* Reporte de Análisis Temporal */}
            <div className="reporte-card">
              <div className="reporte-icon temporal">
                <FiBarChart />
              </div>
              <div className="reporte-content">
                <h4>Análisis Temporal</h4>
                <p>Tendencias y patrones a lo largo del tiempo</p>
                <ul className="reporte-incluye">
                  <li> Ventas diarias/semanales</li>  
                  <li> Estacionalidad</li>
                  <li> Proyecciones</li>
                  <li> Comparativas históricas</li>
                </ul>
              </div>
              <button 
                className="btn-generar"
                onClick={() => generarReporte('Análisis Temporal')}
                disabled={reporteSeleccionado === 'Análisis Temporal'}
              >
                <FiDownload />
                {reporteSeleccionado === 'Análisis Temporal' ? 'Generando...' : 'Generar Excel'}
              </button>
            </div>
          </div>
        </div>

        {/* Accesos Rápidos */}
        <div className="accesos-rapidos">
          <h3 className="section-title">⚡ Accesos Rápidos a Endpoints</h3>
          <div className="endpoints-grid">
            {reporteData.reportes_disponibles?.map((endpoint, index) => (
              <div key={index} className="endpoint-card">
                <code>{endpoint}</code>
                <button 
                  className="btn-api"
                  onClick={() => window.open(`http://localhost:8000${endpoint}`, '_blank')}
                >
                  Abrir API
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </Layout>
  );
}
