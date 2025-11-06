import React, { useState, useEffect } from 'react';
import Layout from '../components/Layout';
import { analyticsService } from '../services/api';
import { FiPackage, FiTrendingUp, FiZap, FiShoppingCart, FiArrowRight } from 'react-icons/fi';
import './patrones.css';

interface Regla {
  antecedente: string[];
  consecuente: string[];
  soporte: number;
  confianza: number;
  lift: number;
}

export default function PatronesCompra() {
  const [reglas, setReglas] = useState<Regla[]>([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    cargarReglasAsociacion();
  }, []);

  const cargarReglasAsociacion = async () => {
    try {
      // Usar parámetros más bajos para encontrar patrones con los datos actuales
      const data = await analyticsService.getReglasAsociacion(0.2, 0.01);
      setReglas(data.reglas || []);
    } catch (error) {
      console.error('Error cargando reglas:', error);
    } finally {
      setCargando(false);
    }
  };

  const obtenerRecomendacion = (regla: Regla) => {
    const productos = [...regla.antecedente, ...regla.consecuente];
    
    if (regla.confianza > 60) {
      return `🎯 Crear combo promocional: ${productos.join(' + ')} con 15% de descuento`;
    } else if (regla.confianza > 40) {
      return `📍 Ubicar ${productos.join(' y ')} juntos en la tienda`;
    } else {
      return `💡 Considerar cross-selling entre ${productos.join(' y ')}`;
    }
  };

  if (cargando) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando patrones de compra...</p>
      </div>
    );
  }

  const maxConfianza = reglas.length > 0 ? Math.max(...reglas.map(r => r.confianza)) : 0;
  const patronesFuertes = reglas.filter(r => r.confianza > 60).length;

  return (
    <Layout>
      <div className="patrones-container">
        {/* Header */}
        <div className="patrones-header">
          <h1>🧠 Análisis de Patrones de Compra</h1>
          <p>Descubre qué productos se venden juntos y optimiza tu estrategia comercial</p>
        </div>

      {/* Estadísticas */}
      <div className="stats-grid">
        <div className="stat-card blue">
          <div className="stat-icon">
            <FiPackage />
          </div>
          <div className="stat-content">
            <div className="stat-value">{reglas.length}</div>
            <div className="stat-label">Patrones Descubiertos</div>
          </div>
        </div>

        <div className="stat-card green">
          <div className="stat-icon">
            <FiTrendingUp />
          </div>
          <div className="stat-content">
            <div className="stat-value">{maxConfianza.toFixed(0)}%</div>
            <div className="stat-label">Máxima Confianza</div>
          </div>
        </div>

        <div className="stat-card purple">
          <div className="stat-icon">
            <FiZap />
          </div>
          <div className="stat-content">
            <div className="stat-value">{patronesFuertes}</div>
            <div className="stat-label">Patrones Fuertes</div>
          </div>
        </div>
      </div>

      {/* Contenido Principal */}
      <div className="patrones-content">
        {/* Reglas de Asociación */}
        <div className="reglas-section">
          <div className="section-card">
            <h3 className="section-title">
              <FiShoppingCart className="title-icon" />
              Patrones de Compra Descubiertos
            </h3>
            
            {reglas.length === 0 ? (
              <div className="empty-state">
                <p>No se encontraron patrones. Intenta ajustar los filtros.</p>
              </div>
            ) : (
              <div className="reglas-list">
                {reglas.map((regla, index) => (
                  <div key={index} className="regla-card">
                    <div className="regla-header">
                      <div className="regla-pattern">
                        <span className="antecedente">{regla.antecedente.join(' + ')}</span>
                        <FiArrowRight className="arrow-icon" />
                        <span className="consecuente">{regla.consecuente.join(' + ')}</span>
                      </div>
                      <span className="confidence-badge">
                        {regla.confianza}% confianza
                      </span>
                    </div>
                    
                    <p className="regla-stats">
                      📊 {regla.soporte}% de los clientes compran estos productos juntos
                    </p>
                    
                    <div className="regla-action">
                      <strong>💡 Acción recomendada:</strong>
                      <p>{obtenerRecomendacion(regla)}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Visualización de Confianza */}
        <div className="graficas-section">
          <div className="section-card">
            <h3 className="section-title">
              <FiTrendingUp className="title-icon" />
              Visualización de Confianza
            </h3>
            
            {reglas.length > 0 ? (
              <div className="confianza-chart">
                {reglas.slice(0, 8).map((regla, index) => {
                  const productos = [...regla.antecedente, ...regla.consecuente].join(' + ');
                  return (
                    <div key={index} className="chart-row">
                      <div className="chart-label">
                        <span className="chart-rank">#{index + 1}</span>
                        <span className="chart-productos">{productos}</span>
                      </div>
                      <div className="chart-bar-container">
                        <div 
                          className="chart-bar-fill"
                          style={{ width: `${regla.confianza}%` }}
                        >
                          <span className="bar-percentage">{regla.confianza}%</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="empty-state">
                <p>No hay datos para visualizar</p>
              </div>
            )}
          </div>
        </div>

        {/* Distribución de Soporte */}
        <div className="graficas-section">
          <div className="section-card">
            <h3 className="section-title">
              <FiPackage className="title-icon" />
              Distribución de Soporte
            </h3>
            
            {reglas.length > 0 ? (
              <div className="soporte-grid">
                {reglas.slice(0, 6).map((regla, index) => {
                  const color = regla.soporte > 2 ? '#00b341' : regla.soporte > 1.5 ? '#f59e0b' : '#4a7fa7';
                  return (
                    <div key={index} className="soporte-card">
                      <div className="soporte-header">
                        <span className="soporte-productos">
                          {[...regla.antecedente, ...regla.consecuente].join(' → ')}
                        </span>
                      </div>
                      <div className="soporte-circle" style={{ borderColor: color }}>
                        <span className="soporte-value" style={{ color }}>{regla.soporte}%</span>
                        <span className="soporte-label">Soporte</span>
                      </div>
                      <div className="soporte-footer">
                        <span>Confianza: {regla.confianza}%</span>
                        <span>Lift: {regla.lift}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="empty-state">
                <p>No hay datos para visualizar</p>
              </div>
            )}
          </div>
        </div>
      </div>

      </div>
    </Layout>
  );
}

