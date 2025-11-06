import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { FiTrendingUp, FiTrendingDown, FiDollarSign, FiShoppingCart, FiPackage, FiPercent } from 'react-icons/fi';
import './kpis.css';

interface KPI {
  valor: string;
  variacion?: string;
  tendencia?: string;
  descripcion?: string;
}

interface KPIData {
  periodo: string;
  kpis_principales: {
    ventas_totales: KPI;
    num_transacciones: KPI;
    ticket_promedio: KPI;
    tasa_conversion: KPI;
    valor_promedio_cliente: KPI;
    rotacion_inventario: KPI;
  };
}

export default function KPIs() {
  const [kpiData, setKpiData] = useState<KPIData | null>(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarKPIs();
  }, []);

  const cargarKPIs = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/kpis/dashboard', {
        headers: {
          'X-API-Key': 'retail_hackaton_2025_fup'
        }
      });
      const data = await response.json();
      setKpiData(data);
    } catch (error) {
      console.error('Error cargando KPIs:', error);
    } finally {
      setCargando(false);
    }
  };

  if (cargando) {
    return (
      <Layout>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Cargando KPIs...</p>
        </div>
      </Layout>
    );
  }

  if (!kpiData) {
    return (
      <Layout>
        <div className="error-container">
          <p>Error al cargar los KPIs. Verifica que el backend esté corriendo.</p>
        </div>
      </Layout>
    );
  }

  const kpis = kpiData.kpis_principales || {};
  
  // Validar que todos los KPIs existan
  if (!kpis.ventas_totales || !kpis.num_transacciones || !kpis.ticket_promedio) {
    return (
      <Layout>
        <div className="error-container">
          <p>Datos de KPIs incompletos. Verifica el backend.</p>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="kpis-container">
        <div className="kpis-header">
          <h1> Indicadores Clave de Rendimiento (KPIs)</h1>
          <p>Métricas principales con comparativa vs período anterior</p>
          <span className="periodo-badge">{kpiData.periodo}</span>
        </div>

        {/* KPIs Grid Principal */}
        <div className="kpis-grid">
          {/* Ventas Totales */}
          <div className="kpi-card ventas">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper ventas">
                <FiDollarSign />
              </div>
              <div className="kpi-info">
                <h3>Ventas Totales</h3>
                <div className="kpi-value">{kpis.ventas_totales.valor}</div>
              </div>
            </div>
            <div className={`kpi-variacion ${kpis.ventas_totales.tendencia}`}>
              {kpis.ventas_totales.tendencia === 'positiva' ? <FiTrendingUp /> : <FiTrendingDown />}
              <span>{kpis.ventas_totales.variacion} vs período anterior</span>
            </div>
          </div>

          {/* Número de Transacciones */}
          <div className="kpi-card transacciones">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper transacciones">
                <FiShoppingCart />
              </div>
              <div className="kpi-info">
                <h3>Transacciones</h3>
                <div className="kpi-value">{kpis.num_transacciones.valor}</div>
              </div>
            </div>
            <div className={`kpi-variacion ${kpis.num_transacciones.tendencia}`}>
              {kpis.num_transacciones.tendencia === 'positiva' ? <FiTrendingUp /> : <FiTrendingDown />}
              <span>{kpis.num_transacciones.variacion} vs período anterior</span>
            </div>
          </div>

          {/* Ticket Promedio */}
          <div className="kpi-card ticket">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper ticket">
                <FiDollarSign />
              </div>
              <div className="kpi-info">
                <h3>Ticket Promedio</h3>
                <div className="kpi-value">{kpis.ticket_promedio.valor}</div>
              </div>
            </div>
            <div className={`kpi-variacion ${kpis.ticket_promedio.tendencia}`}>
              {kpis.ticket_promedio.tendencia === 'positiva' ? <FiTrendingUp /> : <FiTrendingDown />}
              <span>{kpis.ticket_promedio.variacion} vs período anterior</span>
            </div>
          </div>

          {/* Tasa de Conversión */}
          <div className="kpi-card conversion">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper conversion">
                <FiPercent />
              </div>
              <div className="kpi-info">
                <h3>Tasa de Conversión</h3>
                <div className="kpi-value">{kpis.tasa_conversion.valor}</div>
              </div>
            </div>
            <div className="kpi-descripcion">
              {kpis.tasa_conversion.descripcion}
            </div>
          </div>

          {/* Valor Promedio Cliente */}
          <div className="kpi-card cliente">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper cliente">
                <FiDollarSign />
              </div>
              <div className="kpi-info">
                <h3>Valor Promedio Cliente</h3>
                <div className="kpi-value">{kpis.valor_promedio_cliente.valor}</div>
              </div>
            </div>
            <div className="kpi-descripcion">
              {kpis.valor_promedio_cliente.descripcion}
            </div>
          </div>

          {/* Rotación de Inventario */}
          <div className="kpi-card rotacion">
            <div className="kpi-header">
              <div className="kpi-icon-wrapper rotacion">
                <FiPackage />
              </div>
              <div className="kpi-info">
                <h3>Rotación de Inventario</h3>
                <div className="kpi-value">{kpis.rotacion_inventario.valor}</div>
              </div>
            </div>
            <div className="kpi-descripcion">
              {kpis.rotacion_inventario.descripcion}
            </div>
          </div>
        </div>

        {/* Sección de Insights */}
        <div className="insights-section">
          <h3> Insights y Recomendaciones</h3>
          <div className="insights-grid">
            {parseFloat(kpis.ventas_totales.variacion || '0') > 0 && (
              <div className="insight-card positivo">
                <FiTrendingUp className="insight-icon" />
                <div className="insight-content">
                  <h4>Tendencia Positiva en Ventas</h4>
                  <p>Las ventas aumentaron {kpis.ventas_totales.variacion}. Mantén las estrategias actuales y considera ampliar el stock de productos top.</p>
                </div>
              </div>
            )}
            
            {parseFloat(kpis.ticket_promedio.variacion || '0') > 0 && (
              <div className="insight-card positivo">
                <FiDollarSign className="insight-icon" />
                <div className="insight-content">
                  <h4>Aumento en Ticket Promedio</h4>
                  <p>El ticket promedio creció {kpis.ticket_promedio.variacion}. Los clientes están comprando más por transacción.</p>
                </div>
              </div>
            )}

            <div className="insight-card info">
              <FiPackage className="insight-icon" />
              <div className="insight-content">
                <h4>Rotación de Inventario</h4>
                <p>Índice actual: {kpis.rotacion_inventario.valor}. Un índice óptimo está entre 2-4 para retail de ropa.</p>
              </div>
            </div>

            <div className="insight-card accion">
              <FiPercent className="insight-icon" />
              <div className="insight-content">
                <h4>Tasa de Conversión</h4>
                <p>{kpis.tasa_conversion.valor} de productos tienen ventas. Considera promociones para productos sin movimiento.</p>
              </div>
            </div>
          </div>
        </div>

      </div>
    </Layout>
  );
}
