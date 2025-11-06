import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { analyticsService } from '../services/api';
import { FiAlertTriangle, FiPackage } from 'react-icons/fi';
import './alertas.css';

interface Alerta {
  id: number;
  nombre: string;
  categoria: string;
  genero_cliente: string;
  talla: string;
  stock_actual: number;
  stock_minimo: number;
  estado: string;
}

export default function Alertas() {
  const [alertas, setAlertas] = useState<Alerta[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarAlertas();
  }, []);

  const cargarAlertas = async () => {
    try {
      const data = await analyticsService.getAlertasStock();
      setAlertas(data.alertas || []);
    } catch (error) {
      console.error('Error cargando alertas:', error);
    } finally {
      setCargando(false);
    }
  };

  const alertasCriticas = alertas.filter(a => a.stock_actual === 0);
  const alertasBajas = alertas.filter(a => a.stock_actual > 0);

  if (cargando) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando alertas...</p>
      </div>
    );
  }

  return (
    <Layout>
      <div className="alertas-container">
        <div className="alertas-header">
          <h1>⚠️ Alertas de Stock</h1>
          <p>Monitoreo de productos con inventario crítico</p>
        </div>

      {/* Resumen */}
      <div className="alertas-resumen">
        <div className="resumen-card critico">
          <FiAlertTriangle className="resumen-icon" />
          <div className="resumen-content">
            <span className="resumen-value">{alertasCriticas.length}</span>
            <span className="resumen-label">Alertas Críticas</span>
            <span className="resumen-desc">Stock agotado</span>
          </div>
        </div>
        <div className="resumen-card bajo">
          <FiPackage className="resumen-icon" />
          <div className="resumen-content">
            <span className="resumen-value">{alertasBajas.length}</span>
            <span className="resumen-label">Stock Bajo</span>
            <span className="resumen-desc">Por debajo del mínimo</span>
          </div>
        </div>
        <div className="resumen-card total">
          <FiPackage className="resumen-icon" />
          <div className="resumen-content">
            <span className="resumen-value">{alertas.length}</span>
            <span className="resumen-label">Total Alertas</span>
            <span className="resumen-desc">Requieren atención</span>
          </div>
        </div>
      </div>

      {/* Alertas Críticas */}
      {alertasCriticas.length > 0 && (
        <div className="alertas-section">
          <h3 className="section-title critico">
            <FiAlertTriangle />
            Alertas Críticas - Stock Agotado
          </h3>
          <div className="alertas-grid">
            {alertasCriticas.map((alerta) => (
              <div key={alerta.id} className="alerta-card critico">
                <div className="alerta-badge">CRÍTICO</div>
                <h4 className="alerta-nombre">{alerta.nombre}</h4>
                <div className="alerta-detalles">
                  <div className="detalle-item">
                    <span className="detalle-label">Categoría:</span>
                    <span className="detalle-value">{alerta.categoria}</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-label">Género:</span>
                    <span className={`genero-badge ${alerta.genero_cliente}`}>
                      {alerta.genero_cliente}
                    </span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-label">Talla:</span>
                    <span className="detalle-value">{alerta.talla}</span>
                  </div>
                  <div className="detalle-item stock">
                    <span className="detalle-label">Stock:</span>
                    <span className="stock-critico">{alerta.stock_actual} / {alerta.stock_minimo}</span>
                  </div>
                </div>
                <div className="alerta-accion">
                  <button className="btn-reponer">Reponer Ahora</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alertas Bajas */}
      {alertasBajas.length > 0 && (
        <div className="alertas-section">
          <h3 className="section-title bajo">
            <FiPackage />
            Stock Bajo - Requiere Atención
          </h3>
          <div className="alertas-grid">
            {alertasBajas.map((alerta) => (
              <div key={alerta.id} className="alerta-card bajo">
                <div className="alerta-badge bajo">BAJO</div>
                <h4 className="alerta-nombre">{alerta.nombre}</h4>
                <div className="alerta-detalles">
                  <div className="detalle-item">
                    <span className="detalle-label">Categoría:</span>
                    <span className="detalle-value">{alerta.categoria}</span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-label">Género:</span>
                    <span className={`genero-badge ${alerta.genero_cliente}`}>
                      {alerta.genero_cliente}
                    </span>
                  </div>
                  <div className="detalle-item">
                    <span className="detalle-label">Talla:</span>
                    <span className="detalle-value">{alerta.talla}</span>
                  </div>
                  <div className="detalle-item stock">
                    <span className="detalle-label">Stock:</span>
                    <span className="stock-bajo">{alerta.stock_actual} / {alerta.stock_minimo}</span>
                  </div>
                </div>
                <div className="alerta-accion">
                  <button className="btn-programar">Programar Reposición</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {alertas.length === 0 && (
        <div className="empty-state">
          <FiPackage className="empty-icon" />
          <h3>¡Todo en orden!</h3>
          <p>No hay productos con stock crítico o bajo en este momento.</p>
        </div>
      )}
      </div>
    </Layout>
  );
}

