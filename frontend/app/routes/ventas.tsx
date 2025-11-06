import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { FiShoppingCart, FiDollarSign, FiTrendingUp, FiCalendar, FiBarChart2 } from 'react-icons/fi';
import './ventas.css';

interface VentaDashboard {
  hoy: {
    ventas: number;
    ingresos: string;
    ticket_promedio: string;
  };
  mes_actual: {
    ventas: number;
    ingresos: string;
    ticket_promedio: string;
  };
  tendencia_7_dias: Array<{
    fecha: string;
    total: number;
  }>;
}

export default function Ventas() {
  const [ventasData, setVentasData] = useState<VentaDashboard | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarDashboardVentas();
  }, []);

  const cargarDashboardVentas = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/ventas/dashboard-ventas', {
        headers: {
          'X-API-Key': 'retail_hackaton_2025_fup'
        }
      });
      const data = await response.json();
      setVentasData(data);
    } catch (error) {
      console.error('Error cargando dashboard ventas:', error);
    } finally {
      setCargando(false);
    }
  };

  if (cargando) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando dashboard de ventas...</p>
        </div>
      </Layout>
    );
  }

  if (!ventasData) {
    return (
      <Layout>
        <div className="error-container">
          <p>Error al cargar ventas. Verifica que el backend esté corriendo.</p>
        </div>
      </Layout>
    );
  }

  const tendencia = ventasData.tendencia_7_dias || [];
  const maxVenta = tendencia.length > 0 ? Math.max(...tendencia.map(v => v.total)) : 1;

  return (
    <Layout>
      <div className="ventas-container">
        <div className="ventas-header">
          <h1>📋 Dashboard de Ventas</h1>
          <p>Monitoreo en tiempo real de transacciones y rendimiento</p>
        </div>

        {/* Métricas del Día */}
        <div className="metricas-section">
          <h3 className="section-title">📅 Ventas de Hoy</h3>
          <div className="metricas-grid">
            <div className="metrica-card hoy">
              <div className="metrica-icon">
                <FiShoppingCart />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Transacciones</span>
                <span className="metrica-value">{ventasData.hoy?.ventas || 0}</span>
              </div>
            </div>

            <div className="metrica-card hoy">
              <div className="metrica-icon">
                <FiDollarSign />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Ingresos</span>
                <span className="metrica-value">{ventasData.hoy?.ingresos || '$0.00'}</span>
              </div>
            </div>

            <div className="metrica-card hoy">
              <div className="metrica-icon">
                <FiTrendingUp />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Ticket Promedio</span>
                <span className="metrica-value">{ventasData.hoy?.ticket_promedio || '$0.00'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Métricas del Mes */}
        <div className="metricas-section">
          <h3 className="section-title">📊 Ventas del Mes Actual</h3>
          <div className="metricas-grid">
            <div className="metrica-card mes">
              <div className="metrica-icon">
                <FiShoppingCart />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Transacciones</span>
                <span className="metrica-value">{ventasData.mes_actual?.ventas || 0}</span>
              </div>
            </div>

            <div className="metrica-card mes">
              <div className="metrica-icon">
                <FiDollarSign />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Ingresos</span>
                <span className="metrica-value">{ventasData.mes_actual?.ingresos || '$0.00'}</span>
              </div>
            </div>

            <div className="metrica-card mes">
              <div className="metrica-icon">
                <FiTrendingUp />
              </div>
              <div className="metrica-content">
                <span className="metrica-label">Ticket Promedio</span>
                <span className="metrica-value">{ventasData.mes_actual?.ticket_promedio || '$0.00'}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Tendencia 7 Días */}
        <div className="tendencia-section">
          <h3 className="section-title">
            <FiBarChart2 />
            Tendencia Últimos 7 Días
          </h3>
          <div className="chart-card">
            {tendencia.length > 0 ? (
              <div className="chart-bars">
                {tendencia.map((dia, index) => (
                  <div key={index} className="chart-bar-container">
                    <div className="chart-bar-wrapper">
                      <div 
                        className="chart-bar"
                        style={{
                          height: `${(dia.total / maxVenta) * 100}%`,
                          minHeight: '20px'
                        }}
                      >
                        <span className="bar-value">${dia.total.toFixed(0)}</span>
                      </div>
                    </div>
                    <div className="chart-label">
                      {new Date(dia.fecha).toLocaleDateString('es-ES', { 
                        weekday: 'short',
                        day: 'numeric'
                      })}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <p>No hay datos de tendencia disponibles</p>
              </div>
            )}
          </div>
        </div>

      </div>
    </Layout>
  );
}
