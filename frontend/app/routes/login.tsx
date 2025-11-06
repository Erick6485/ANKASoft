import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
import { authService } from '../services/api';
import './login.css';

export default function Login() {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    nombre_completo: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        // Login
        await authService.login(formData.username, formData.password);
        navigate('/dashboard');
      } else {
        // Register
        await authService.register({
          username: formData.username,
          email: formData.email,
          password: formData.password,
          nombre_completo: formData.nombre_completo,
          rol: 'vendedor',
        });
        setIsLogin(true);
        setError('Usuario creado exitosamente. Ahora puedes iniciar sesión.');
      }
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 'Error al procesar la solicitud'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-content">
        <div className="login-header">
          <h1>Inventario Retail</h1>
          <p>Sistema de Gestión y Análisis de Inventario</p>
        </div>

        <div className="login-tabs">
          <button
            className={`tab ${isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(true)}
          >
            Iniciar Sesión
          </button>
          <button
            className={`tab ${!isLogin ? 'active' : ''}`}
            onClick={() => setIsLogin(false)}
          >
            Registrarse
          </button>
        </div>

        <div className="login-card">
          <form onSubmit={handleSubmit}>
            {!isLogin && (
              <div className="form-group">
                <label>Nombre Completo</label>
                <input
                  type="text"
                  placeholder="Tu nombre completo"
                  value={formData.nombre_completo}
                  onChange={(e) =>
                    setFormData({ ...formData, nombre_completo: e.target.value })
                  }
                  required={!isLogin}
                />
              </div>
            )}

            {!isLogin && (
              <div className="form-group">
                <label>Correo Electrónico</label>
                <input
                  type="email"
                  placeholder="tu@email.com"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  required={!isLogin}
                />
              </div>
            )}

            <div className="form-group">
              <label>{isLogin ? 'Usuario' : 'Nombre de Usuario'}</label>
              <input
                type="text"
                placeholder={isLogin ? 'tu usuario' : 'usuario123'}
                value={formData.username}
                onChange={(e) =>
                  setFormData({ ...formData, username: e.target.value })
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Contraseña</label>
              <input
                type="password"
                placeholder="••••••"
                value={formData.password}
                onChange={(e) =>
                  setFormData({ ...formData, password: e.target.value })
                }
                required
              />
            </div>

            {error && (
              <div className={`error-message ${error.includes('exitosamente') ? 'success' : ''}`}>
                {error}
              </div>
            )}

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? 'Procesando...' : isLogin ? 'Iniciar Sesión' : 'Registrarse'}
            </button>
          </form>

          {isLogin && (
            <div className="test-credentials">
              <div className="test-label">Prueba con:</div>
              <div className="test-item">
                <span className="test-icon">👤</span>
                <span>admin / admin123</span>
              </div>
              <div className="test-item">
                <span className="test-icon">👤</span>
                <span>gerente / gerente123</span>
              </div>
              <div className="test-item">
                <span className="test-icon">👤</span>
                <span>vendedor / vendedor123</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

