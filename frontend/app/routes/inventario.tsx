import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { FiPackage, FiAlertCircle, FiCheckCircle, FiTrendingUp, FiDollarSign } from 'react-icons/fi';
import './inventario.css';

interface InventarioDashboard {
  resumen: {
    total_productos: number;
    productos_stock_bajo: number;
    productos_proximos_agotar: number;
    valor_total_inventario: string;
    nivel_servicio: string;
  };
  metricas_clave: {
    indice_rotacion: number;
    cobertura_inventario: number;
    eficiencia_espacio: number;
  };
}

export default function Inventario() {
  const [inventarioData, setInventarioData] = useState<InventarioDashboard | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarDashboardInventario();
  }, []);

  const cargarDashboardInventario = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/inventario/dashboard-inventario', {
        headers: {
          'X-API-Key': 'retail_hackaton_2025_fup'
        }
      });
      const data = await response.json();
      setInventarioData(data);
    } catch (error) {
      console.error('Error cargando dashboard inventario:', error);
    } finally {
      setCargando(false);
    }
  };

  if (cargando) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando dashboard de inventario...</p>
        </div>
      </Layout>
    );
  }

  if (!inventarioData) {
    return (
      <Layout>
        <div className="error-container">
          <p>Error al cargar inventario. Verifica que el backend esté corriendo.</p>
        </div>
      </Layout>
    );
  }

  const resumen = inventarioData.resumen || {};
  const metricas_clave = inventarioData.metricas_clave || {};

  return (
    <Layout>
      <div className="inventario-container">
        <div className="inventario-header">
          <h1>📦 Dashboard de Inventario</h1>
          <p>Control completo de stock y métricas de eficiencia</p>
        </div>

        {/* Resumen Principal */}
        <div className="resumen-grid">
          <div className="resumen-card total">
            <div className="resumen-icon">
              <FiPackage />
            </div>
            <div className="resumen-content">
              <span className="resumen-label">Total Productos</span>
              <span className="resumen-value">{resumen.total_productos || 0}</span>
              <span className="resumen-desc">SKUs únicos en catálogo</span>
            </div>
          </div>

          <div className="resumen-card valor">
            <div className="resumen-icon">
              <FiDollarSign />
            </div>
            <div className="resumen-content">
              <span className="resumen-label">Valor Inventario</span>
              <span className="resumen-value">{resumen.valor_total_inventario || '$0.00'}</span>
              <span className="resumen-desc">Valorización total</span>
            </div>
          </div>

          <div className="resumen-card critico">
            <div className="resumen-icon">
              <FiAlertCircle />
            </div>
            <div className="resumen-content">
              <span className="resumen-label">Stock Bajo</span>
              <span className="resumen-value">{resumen.productos_stock_bajo || 0}</span>
              <span className="resumen-desc">Productos críticos</span>
            </div>
          </div>

          <div className="resumen-card servicio">
            <div className="resumen-icon">
              <FiCheckCircle />
            </div>
            <div className="resumen-content">
              <span className="resumen-label">Nivel de Servicio</span>
              <span className="resumen-value">{resumen.nivel_servicio || '0%'}</span>
              <span className="resumen-desc">Disponibilidad</span>
            </div>
          </div>
        </div>

        {/* Métricas Clave */}
        <div className="metricas-section">
          <h3 className="section-title">
            <FiTrendingUp />
            Métricas de Desempeño
          </h3>
          <div className="metricas-grid">
            <div className="metrica-card">
              <div className="metrica-header">
                <h4>Índice de Rotación</h4>
                <span className={`metrica-badge ${(metricas_clave.indice_rotacion || 0) > 2 ? 'bueno' : 'regular'}`}>
                  {(metricas_clave.indice_rotacion || 0) > 2 ? 'BUENO' : 'REGULAR'}
                </span>
              </div>
              <div className="metrica-valor">{(metricas_clave.indice_rotacion || 0).toFixed(2)}</div>
              <div className="metrica-barra">
                <div 
                  className="metrica-fill rotacion"
                  style={{width: `${Math.min((metricas_clave.indice_rotacion || 0) / 5 * 100, 100)}%`}}
                ></div>
              </div>
              <p className="metrica-descripcion">
                Veces que rota el inventario. Óptimo: 2-4 para retail
              </p>
            </div>

            <div className="metrica-card">
              <div className="metrica-header">
                <h4>Cobertura de Inventario</h4>
                <span className={`metrica-badge ${(metricas_clave.cobertura_inventario || 0) > 80 ? 'bueno' : 'regular'}`}>
                  {(metricas_clave.cobertura_inventario || 0) > 80 ? 'BUENO' : 'REGULAR'}
                </span>
              </div>
              <div className="metrica-valor">{(metricas_clave.cobertura_inventario || 0).toFixed(1)}%</div>
              <div className="metrica-barra">
                <div 
                  className="metrica-fill cobertura"
                  style={{width: `${metricas_clave.cobertura_inventario || 0}%`}}
                ></div>
              </div>
              <p className="metrica-descripcion">
                Porcentaje de productos con stock disponible
              </p>
            </div>

            <div className="metrica-card">
              <div className="metrica-header">
                <h4>Eficiencia de Espacio</h4>
                <span className={`metrica-badge ${(metricas_clave.eficiencia_espacio || 0) > 60 ? 'bueno' : 'regular'}`}>
                  {(metricas_clave.eficiencia_espacio || 0) > 60 ? 'BUENO' : 'REGULAR'}
                </span>
              </div>
              <div className="metrica-valor">{(metricas_clave.eficiencia_espacio || 0).toFixed(1)}%</div>
              <div className="metrica-barra">
                <div 
                  className="metrica-fill eficiencia"
                  style={{width: `${metricas_clave.eficiencia_espacio || 0}%`}}
                ></div>
              </div>
              <p className="metrica-descripcion">
                Productos con stock óptimo (ni bajo ni excesivo)
              </p>
            </div>
          </div>
        </div>

        {/* Alertas Resumen */}
        <div className="alertas-resumen-section">
          <h3 className="section-title">
            <FiAlertCircle />
            Resumen de Alertas
          </h3>
          <div className="alertas-quick">
            <div className="alerta-quick critico">
              <div className="alerta-numero">{resumen.productos_proximos_agotar}</div>
              <div className="alerta-texto">
                <strong>Próximos a Agotar</strong>
                <p>Stock menor a 5 unidades</p>
              </div>
            </div>

            <div className="alerta-quick bajo">
              <div className="alerta-numero">{resumen.productos_stock_bajo}</div>
              <div className="alerta-texto">
                <strong>Stock Bajo</strong>
                <p>Por debajo del mínimo</p>
              </div>
            </div>

            <div className="alerta-quick bien">
              <div className="alerta-numero">{resumen.total_productos - resumen.productos_stock_bajo}</div>
              <div className="alerta-texto">
                <strong>Stock Normal</strong>
                <p>Nivel adecuado</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </Layout>
  );
}
