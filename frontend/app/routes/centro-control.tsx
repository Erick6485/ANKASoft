import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import Layout from '../components/Layout';
import { analyticsService } from '../services/api';
import './centro-control.css';

export default function CentroControl() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [alertas, setAlertas] = useState<any[]>([]);
  const [recomendaciones, setRecomendaciones] = useState<any[]>([]);
  const [predicciones, setPredicciones] = useState<any[]>([]);
  const [reglas, setReglas] = useState<any[]>([]);
  const [stats, setStats] = useState({
    alertasCriticas: 0,
    accionesRecomendadas: 0,
    patronesDescubiertos: 0,
    prediccionVentas: 0
  });

  useEffect(() => {
    cargarDatos();
    // Auto-refresh cada 30 segundos
    const interval = setInterval(() => {
      cargarDatos();
    }, 30000);
    return () => clearInterval(interval);
  }, []);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      
      // Cargar alertas
      const alertasRes = await analyticsService.getAlertasStock();
      setAlertas(alertasRes.alertas || []);
      
      // Cargar recomendaciones
      const recomendacionesRes = await analyticsService.getRecomendaciones();
      setRecomendaciones(recomendacionesRes.recomendaciones || []);
      
      // Cargar predicciones
      const prediccionesRes = await analyticsService.getPredicciones();
      setPredicciones(prediccionesRes.predicciones || []);
      
      // Cargar reglas de asociación
      const reglasRes = await analyticsService.getReglasAsociacion(0.3, 0.05);
      setReglas(reglasRes.reglas || []);
      
      // Calcular estadísticas
      setStats({
        alertasCriticas: alertasRes.alertas?.filter((a: any) => a.estado === 'CRÍTICO').length || 0,
        accionesRecomendadas: recomendacionesRes.recomendaciones?.length || 0,
        patronesDescubiertos: reglasRes.reglas?.length || 0,
        prediccionVentas: prediccionesRes.predicciones?.reduce((sum: number, p: any) => 
          sum + (p.prediccion_proximo_mes || 0), 0) || 0
      });
      
    } catch (error) {
      console.error('Error cargando datos:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="centro-control-container">
          <div className="loading-center">
            <div className="spinner"></div>
            <p>Cargando Centro de Control...</p>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="centro-control-container">
        {/* Header */}
        <div className="control-header">
          <div className="header-left">
            <h1>🎯 Centro de Control Inteligente</h1>
            <p className="subtitle">Monitoreo en tiempo real con IA</p>
          </div>
          <div className="header-right">
            <div className="status-indicator online">
              <span className="pulse"></span>
              Sistema Activo
            </div>
            <button className="refresh-btn" onClick={cargarDatos}>
              🔄 Actualizar
            </button>
          </div>
        </div>

        {/* Métricas Principales */}
        <div className="metrics-grid">
          <div className="metric-card critical">
            <div className="metric-icon">🚨</div>
            <div className="metric-content">
              <div className="metric-value">{stats.alertasCriticas}</div>
              <div className="metric-label">Alertas Críticas</div>
            </div>
          </div>
          
          <div className="metric-card warning">
            <div className="metric-icon">💡</div>
            <div className="metric-content">
              <div className="metric-value">{stats.accionesRecomendadas}</div>
              <div className="metric-label">Acciones Recomendadas</div>
            </div>
          </div>
          
          <div className="metric-card info">
            <div className="metric-icon">🔍</div>
            <div className="metric-content">
              <div className="metric-value">{stats.patronesDescubiertos}</div>
              <div className="metric-label">Patrones Descubiertos</div>
            </div>
          </div>
          
          <div className="metric-card success">
            <div className="metric-icon">📈</div>
            <div className="metric-content">
              <div className="metric-value">{Math.round(stats.prediccionVentas)}</div>
              <div className="metric-label">Predicción Unidades/Mes</div>
            </div>
          </div>
        </div>

        {/* Grid Principal */}
        <div className="control-grid">
          {/* Alertas Críticas */}
          <div className="control-panel critical-panel">
            <div className="panel-header">
              <h3>🚨 Alertas Críticas</h3>
              <span className="badge critical">{alertas.length}</span>
            </div>
            <div className="panel-content">
              {alertas.slice(0, 5).map((alerta, idx) => (
                <div key={idx} className={`alert-item ${alerta.estado.toLowerCase()}`}>
                  <div className="alert-left">
                    <div className="alert-icon">
                      {alerta.estado === 'CRÍTICO' ? '🔴' : '🟡'}
                    </div>
                    <div className="alert-info">
                      <div className="alert-name">{alerta.nombre}</div>
                      <div className="alert-category">{alerta.categoria}</div>
                    </div>
                  </div>
                  <div className="alert-right">
                    <div className="alert-stock">
                      Stock: <strong>{alerta.stock_actual}</strong>
                    </div>
                    <div className="alert-status">{alerta.estado}</div>
                  </div>
                </div>
              ))}
              {alertas.length === 0 && (
                <div className="empty-state">
                  ✅ No hay alertas críticas
                </div>
              )}
            </div>
          </div>

          {/* Recomendaciones Inteligentes */}
          <div className="control-panel recommendations-panel">
            <div className="panel-header">
              <h3>💡 Recomendaciones IA</h3>
              <span className="badge warning">{recomendaciones.length}</span>
            </div>
            <div className="panel-content">
              {recomendaciones.slice(0, 4).map((rec, idx) => (
                <div key={idx} className={`recommendation-item priority-${rec.prioridad?.toLowerCase()}`}>
                  <div className="rec-header">
                    <span className="rec-type">{rec.tipo}</span>
                    <span className={`rec-priority ${rec.prioridad?.toLowerCase()}`}>
                      {rec.prioridad}
                    </span>
                  </div>
                  <div className="rec-product">{rec.producto_nombre}</div>
                  <div className="rec-action">{rec.accion_sugerida}</div>
                </div>
              ))}
              {recomendaciones.length === 0 && (
                <div className="empty-state">
                  ℹ️ No hay recomendaciones pendientes
                </div>
              )}
            </div>
          </div>

          {/* Patrones de Compra */}
          <div className="control-panel patterns-panel">
            <div className="panel-header">
              <h3>🔍 Patrones Descubiertos</h3>
              <span className="badge info">{reglas.length}</span>
            </div>
            <div className="panel-content">
              {reglas.slice(0, 3).map((regla, idx) => (
                <div key={idx} className="pattern-item">
                  <div className="pattern-rule">
                    <span className="pattern-from">
                      {regla.antecedente.join(' + ')}
                    </span>
                    <span className="pattern-arrow">→</span>
                    <span className="pattern-to">
                      {regla.consecuente.join(' + ')}
                    </span>
                  </div>
                  <div className="pattern-stats">
                    <div className="pattern-confidence">
                      Confianza: <strong>{regla.confianza}%</strong>
                    </div>
                    <div className="pattern-support">
                      Soporte: <strong>{regla.soporte}%</strong>
                    </div>
                  </div>
                </div>
              ))}
              {reglas.length === 0 && (
                <div className="empty-state">
                  🔎 Analizando patrones...
                </div>
              )}
              <button 
                className="view-all-btn"
                onClick={() => navigate('/patrones')}
              >
                Ver Todos los Patrones →
              </button>
            </div>
          </div>

          {/* Predicciones */}
          <div className="control-panel predictions-panel">
            <div className="panel-header">
              <h3>📈 Predicciones</h3>
              <span className="badge success">{predicciones.length}</span>
            </div>
            <div className="panel-content">
              {predicciones.slice(0, 4).map((pred, idx) => (
                <div key={idx} className="prediction-item">
                  <div className="pred-category">{pred.categoria}</div>
                  <div className="pred-stats">
                    <div className="pred-stat">
                      <span className="pred-label">Promedio Actual:</span>
                      <span className="pred-value">
                        {Math.round(pred.promedio_ventas_mensual)} unidades
                      </span>
                    </div>
                    <div className="pred-stat">
                      <span className="pred-label">Predicción:</span>
                      <span className="pred-value highlight">
                        {Math.round(pred.prediccion_proximo_mes)} unidades
                      </span>
                    </div>
                  </div>
                  <div className={`pred-trend ${pred.tendencia?.toLowerCase()}`}>
                    {pred.tendencia === 'CRECIMIENTO' ? '📈 Crecimiento' : '📊 Estable'}
                  </div>
                </div>
              ))}
              {predicciones.length === 0 && (
                <div className="empty-state">
                  📊 Generando predicciones...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Acción Rápida */}
        <div className="quick-actions">
          <h3>⚡ Acciones Rápidas</h3>
          <div className="actions-grid">
            <button className="action-btn" onClick={() => navigate('/inventario')}>
              📦 Gestionar Inventario
            </button>
            <button className="action-btn" onClick={() => navigate('/ventas')}>
              💰 Ver Ventas
            </button>
            <button className="action-btn" onClick={() => navigate('/alertas')}>
              🔔 Ver Todas las Alertas
            </button>
            <button className="action-btn" onClick={() => navigate('/patrones')}>
              🧠 Análisis Profundo
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}

