import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { analyticsService, authService } from '../services/api';
import {
  FaShoppingCart,
  FaBox,
  FaChartLine,
  FaExclamationTriangle,
  FaHome,
  FaCube,
  FaList,
  FaChartBar,
  FaTachometerAlt,
  FaFileAlt,
  FaCog,
  FaSignOutAlt,
  FaBell,
  FaRobot,
  FaBrain,
} from 'react-icons/fa';
import './dashboard.css';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<any>(null);
  const [chatMessage, setChatMessage] = useState('');
  const [chatOpen, setChatOpen] = useState(false);
  const [activeSection, setActiveSection] = useState('dashboard');
  const navigate = useNavigate();

  useEffect(() => {
    const currentUser = authService.getCurrentUser();
    if (!currentUser) {
      navigate('/login');
      return;
    }
    setUser(currentUser);
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await analyticsService.getDashboard();
      setDashboardData(data);
    } catch (error) {
      console.error('Error al cargar dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Cargando dashboard...</p>
      </div>
    );
  }

  const resumen = dashboardData?.resumen_general || {};
  const productos = dashboardData?.productos_destacados || [];
  const comparativo = dashboardData?.comparativo_generos || [];
  const alertas = dashboardData?.alertas_prioritarias || [];

  return (
    <div className="dashboard-layout">
      {/* Barra lateral */}
      <div className="sidebar">
        <div className="sidebar-icons">
          <div className="sidebar-icon" onClick={() => setActiveSection('brand')} title="Retail Analytics">
            <FaCube />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'dashboard' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('dashboard');
              navigate('/dashboard');
            }}
            title="Dashboard"
          >
            <FaHome />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'centro-control' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('centro-control');
              navigate('/centro-control');
            }}
            title="Centro de Control IA"
          >
            <FaRobot />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'inventario' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('inventario');
              navigate('/inventario');
            }}
            title="Inventario"
          >
            <FaBox />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'ventas' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('ventas');
              navigate('/ventas');
            }}
            title="Ventas"
          >
            <FaList />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'patrones' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('patrones');
              navigate('/patrones');
            }}
            title="Patrones de Compra"
          >
            <FaBrain />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'analytics' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('analytics');
              navigate('/analytics');
            }}
            title="Analytics"
          >
            <FaChartBar />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'kpis' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('kpis');
              navigate('/kpis');
            }}
            title="KPIs"
          >
            <FaTachometerAlt />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'alertas' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('alertas');
              navigate('/alertas');
            }}
            title="Alertas"
          >
            <FaExclamationTriangle />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'reportes' ? 'active' : ''}`}
            onClick={() => {
              setActiveSection('reportes');
              navigate('/reportes');
            }}
            title="Reportes"
          >
            <FaFileAlt />
          </div>
          <div 
            className={`sidebar-icon ${activeSection === 'configuracion' ? 'active' : ''}`}
            onClick={() => setActiveSection('configuracion')}
            title="Configuración"
          >
            <FaCog />
          </div>
          <div className="sidebar-icon logout" onClick={handleLogout} title="Cerrar Sesión">
            <FaSignOutAlt />
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="main-content">
        {/* Header */}
        <div className="top-header">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Buscar productos, tallas, categorías..."
            />
          </div>
          <div className="header-actions">
            <div className="notification-icon">
              <FaBell />
              <span className="notification-badge">{alertas.length}</span>
            </div>
            <div className="user-info">
              <span>{user?.nombre_completo || user?.username}</span>
            </div>
          </div>
        </div>

        {/* Dashboard content */}
        <div className="dashboard-content">
          <div className="dashboard-title">
            <h1>Dashboard</h1>
            <p>Bienvenido al sistema de gestión de inventario</p>
          </div>

          {/* Tarjetas de métricas */}
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="metric-icon blue">
                <FaShoppingCart />
              </div>
              <div className="metric-info">
                <h3>Ventas Totales</h3>
                <p className="metric-value">{resumen.total_ventas_mes || 0}</p>
                <p className="metric-change positive">+12.5% vs período anterior</p>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon blue">
                <FaBox />
              </div>
              <div className="metric-info">
                <h3>Productos en Stock</h3>
                <p className="metric-value">{resumen.total_productos || 0}</p>
                <p className="metric-change positive">+5.2% vs período anterior</p>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon blue">
                <FaChartLine />
              </div>
              <div className="metric-info">
                <h3>Tasa de Rotación</h3>
                <p className="metric-value">78%</p>
                <p className="metric-change positive">+8.1% vs período anterior</p>
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-icon red">
                <FaExclamationTriangle />
              </div>
              <div className="metric-info">
                <h3>Alertas Activas</h3>
                <p className="metric-value">{resumen.alertas_activas || 0}</p>
                <p className="metric-change negative">-3.2% vs período anterior</p>
              </div>
            </div>
          </div>

          {/* Gráficos */}
          <div className="charts-grid">
            <div className="chart-card">
              <div className="chart-header">
                <h3>Productos Destacados</h3>
                <select className="chart-filter">
                  <option>Última semana</option>
                  <option>Último mes</option>
                  <option>Último trimestre</option>
                </select>
              </div>
              <div className="chart-content">
                <div className="products-list">
                  {productos.slice(0, 5).map((producto: any, index: number) => (
                    <div key={index} className="product-item">
                      <div className="product-rank">{index + 1}</div>
                      <div className="product-details">
                        <div className="product-name">{producto.nombre}</div>
                        <div className="product-category">{producto.categoria}</div>
                      </div>
                      <div className="product-value">
                        ${producto.ingreso_total?.toFixed(2) || 0}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header">
                <h3>Ventas por Género</h3>
                <select className="chart-filter">
                  <option>Comparativa: Ventas vs Stock</option>
                </select>
              </div>
              <div className="chart-content">
                <div className="bar-chart">
                  {comparativo.map((item: any, index: number) => (
                    <div key={index} className="bar-item">
                      <div className="bar-label">{item.genero}</div>
                      <div className="bar-container">
                        <div
                          className="bar-fill"
                          style={{
                            width: `${(item.total_unidades / 1000) * 100}%`,
                            maxWidth: '100%',
                          }}
                        ></div>
                      </div>
                      <div className="bar-value">{item.total_unidades}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Alertas */}
          {alertas.length > 0 && (
            <div className="chart-card full-width">
              <div className="chart-header">
                <h3>Alertas de Stock Crítico</h3>
              </div>
              <div className="chart-content">
                <div className="alerts-list">
                  {alertas.map((alerta: any, index: number) => (
                    <div key={index} className="alert-item">
                      <div className="alert-icon">
                        <FaExclamationTriangle />
                      </div>
                      <div className="alert-details">
                        <div className="alert-product">{alerta.producto}</div>
                        <div className="alert-info">
                          Stock: {alerta.stock_actual} / Mínimo: {alerta.stock_minimo}
                        </div>
                      </div>
                      <div className={`alert-badge ${alerta.estado.toLowerCase()}`}>
                        {alerta.estado}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Botón flotante de chatbot */}
      <button className="chatbot-fab" onClick={() => setChatOpen(!chatOpen)}>
        <FaRobot />
      </button>

      {/* Panel de chatbot */}
      {chatOpen && (
        <div className="chatbot-panel">
          <div className="chatbot-header">
            <h3>Asistente Virtual</h3>
            <button onClick={() => setChatOpen(false)}>✕</button>
          </div>
          <div className="chatbot-messages">
            <div className="chatbot-message bot">
              Hola! Pregúntame sobre productos, ventas o recomendaciones.
            </div>
          </div>
          <div className="chatbot-input">
            <input
              type="text"
              placeholder="Escribe tu pregunta..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
            />
            <button>Enviar</button>
          </div>
        </div>
      )}
    </div>
  );
}

