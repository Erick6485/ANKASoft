import React from 'react';
import { useNavigate, useLocation } from 'react-router';
import { authService } from '../services/api';
import {
  FaHome,
  FaCube,
  FaBox,
  FaList,
  FaBrain,
  FaChartBar,
  FaTachometerAlt,
  FaExclamationTriangle,
  FaFileAlt,
  FaCog,
  FaSignOutAlt,
  FaBell,
  FaUser,
} from 'react-icons/fa';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = React.useState<any>(null);
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => {
    setMounted(true);
    const currentUser = authService.getCurrentUser();
    setUser(currentUser);
  }, []);

  const handleLogout = () => {
    authService.logout();
    navigate('/');
  };

  const isActive = (path: string) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <div className="app-layout">
      {/* Barra lateral */}
      <div className="sidebar">
        <div className="sidebar-icons">
          <div className="sidebar-icon" title="Retail Analytics">
            <FaCube />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/dashboard')}`}
            onClick={() => navigate('/dashboard')}
            title="Dashboard"
          >
            <FaHome />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/inventario')}`}
            onClick={() => navigate('/inventario')}
            title="Inventario"
          >
            <FaBox />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/ventas')}`}
            onClick={() => navigate('/ventas')}
            title="Ventas"
          >
            <FaList />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/patrones')}`}
            onClick={() => navigate('/patrones')}
            title="Patrones de Compra"
          >
            <FaBrain />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/analytics')}`}
            onClick={() => navigate('/analytics')}
            title="Analytics"
          >
            <FaChartBar />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/kpis')}`}
            onClick={() => navigate('/kpis')}
            title="KPIs"
          >
            <FaTachometerAlt />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/alertas')}`}
            onClick={() => navigate('/alertas')}
            title="Alertas"
          >
            <FaExclamationTriangle />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/reportes')}`}
            onClick={() => navigate('/reportes')}
            title="Reportes"
          >
            <FaFileAlt />
          </div>
          <div 
            className={`sidebar-icon ${isActive('/configuracion')}`}
            onClick={() => navigate('/configuracion')}
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
      <div className="main-layout-content">
        {/* Header */}
        <div className="top-header">
          <div className="search-bar">
            <input
              type="text"
              placeholder="Buscar productos, tallas, categorías..."
            />
          </div>
          <div className="header-actions">
            <div className="notification-bell">
              <FaBell />
              <span className="notification-badge">5</span>
            </div>
            <div className="user-profile">
              <FaUser />
              <span className="user-name">{mounted && user ? (user.nombre_completo || 'Usuario') : 'Cargando...'}</span>
            </div>
          </div>
        </div>

        {/* Contenido de la página */}
        <div className="page-content">
          {children}
        </div>
      </div>
    </div>
  );
}

