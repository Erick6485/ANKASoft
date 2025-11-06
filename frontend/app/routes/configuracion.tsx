import React, { useState } from 'react';
import Layout from '../components/Layout';
import { FiUser, FiBell, FiLock, FiDatabase, FiSettings, FiSave } from 'react-icons/fi';
import './configuracion.css';

export default function Configuracion() {
  const [configuracion, setConfiguracion] = useState({
    // Notificaciones
    notificaciones_stock: true,
    notificaciones_ventas: true,
    notificaciones_email: false,
    
    // Umbrales
    stock_minimo_default: 5,
    stock_critico: 2,
    
    // Sistema
    idioma: 'es',
    zona_horaria: 'America/Bogota',
    moneda: 'COP',
  });

  const [guardado, setGuardado] = useState(false);

  const handleChange = (campo: string, valor: any) => {
    setConfiguracion({
      ...configuracion,
      [campo]: valor
    });
    setGuardado(false);
  };

  const guardarConfiguracion = () => {
    // Aquí normalmente se enviaría al backend
    console.log('Guardando configuración:', configuracion);
    setGuardado(true);
    setTimeout(() => setGuardado(false), 3000);
  };

  return (
    <Layout>
      <div className="config-container">
        <div className="config-header">
          <h1>⚙️ Configuración del Sistema</h1>
          <p>Personaliza el comportamiento de la plataforma</p>
        </div>

        {/* Notificaciones */}
        <div className="config-section">
          <div className="section-header">
            <FiBell className="section-icon" />
            <h3>Notificaciones y Alertas</h3>
          </div>
          
          <div className="config-options">
            <div className="config-item">
              <div className="config-label">
                <span>Alertas de Stock Bajo</span>
                <p>Recibe notificaciones cuando el stock esté por debajo del mínimo</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={configuracion.notificaciones_stock}
                  onChange={(e) => handleChange('notificaciones_stock', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="config-item">
              <div className="config-label">
                <span>Alertas de Ventas Altas</span>
                <p>Notifica cuando las ventas superen el promedio</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={configuracion.notificaciones_ventas}
                  onChange={(e) => handleChange('notificaciones_ventas', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>

            <div className="config-item">
              <div className="config-label">
                <span>Notificaciones por Email</span>
                <p>Enviar resumen diario por correo electrónico</p>
              </div>
              <label className="toggle">
                <input
                  type="checkbox"
                  checked={configuracion.notificaciones_email}
                  onChange={(e) => handleChange('notificaciones_email', e.target.checked)}
                />
                <span className="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        {/* Umbrales de Inventario */}
        <div className="config-section">
          <div className="section-header">
            <FiDatabase className="section-icon" />
            <h3>Umbrales de Inventario</h3>
          </div>
          
          <div className="config-options">
            <div className="config-item">
              <div className="config-label">
                <span>Stock Mínimo por Defecto</span>
                <p>Cantidad mínima para generar alertas</p>
              </div>
              <input
                type="number"
                className="config-input"
                value={configuracion.stock_minimo_default}
                onChange={(e) => handleChange('stock_minimo_default', parseInt(e.target.value))}
                min="1"
                max="50"
              />
            </div>

            <div className="config-item">
              <div className="config-label">
                <span>Nivel Crítico</span>
                <p>Cantidad que marca stock en estado crítico</p>
              </div>
              <input
                type="number"
                className="config-input"
                value={configuracion.stock_critico}
                onChange={(e) => handleChange('stock_critico', parseInt(e.target.value))}
                min="0"
                max="10"
              />
            </div>
          </div>
        </div>

        {/* Configuración General */}
        <div className="config-section">
          <div className="section-header">
            <FiSettings className="section-icon" />
            <h3>Configuración General</h3>
          </div>
          
          <div className="config-options">
            <div className="config-item">
              <div className="config-label">
                <span>Idioma</span>
                <p>Idioma de la interfaz</p>
              </div>
              <select
                className="config-select"
                value={configuracion.idioma}
                onChange={(e) => handleChange('idioma', e.target.value)}
              >
                <option value="es">Español</option>
                <option value="en">English</option>
                <option value="pt">Português</option>
              </select>
            </div>

            <div className="config-item">
              <div className="config-label">
                <span>Zona Horaria</span>
                <p>Zona horaria para reportes y fechas</p>
              </div>
              <select
                className="config-select"
                value={configuracion.zona_horaria}
                onChange={(e) => handleChange('zona_horaria', e.target.value)}
              >
                <option value="America/Bogota">Bogotá (GMT-5)</option>
                <option value="America/Mexico_City">México (GMT-6)</option>
                <option value="America/Santiago">Santiago (GMT-3)</option>
                <option value="America/Buenos_Aires">Buenos Aires (GMT-3)</option>
              </select>
            </div>

            <div className="config-item">
              <div className="config-label">
                <span>Moneda</span>
                <p>Moneda para mostrar precios</p>
              </div>
              <select
                className="config-select"
                value={configuracion.moneda}
                onChange={(e) => handleChange('moneda', e.target.value)}
              >
                <option value="COP">Peso Colombiano (COP)</option>
                <option value="USD">Dólar (USD)</option>
                <option value="EUR">Euro (EUR)</option>
                <option value="MXN">Peso Mexicano (MXN)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Botón Guardar */}
        <div className="config-actions">
          <button 
            className={`btn-guardar ${guardado ? 'guardado' : ''}`}
            onClick={guardarConfiguracion}
          >
            <FiSave />
            {guardado ? '✅ Configuración Guardada' : 'Guardar Cambios'}
          </button>
        </div>

        {/* Info */}
        <div className="config-info">
          <p>
            💡 <strong>Nota:</strong> Los cambios se aplicarán inmediatamente en toda la plataforma.
            Algunos cambios pueden requerir recargar la página.
          </p>
        </div>
      </div>
    </Layout>
  );
}

