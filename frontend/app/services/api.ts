import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';
const API_KEY = 'retail_hackaton_2025_fup';

// Configurar axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
});

// Interceptor para agregar el token a todas las peticiones
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    // Siempre incluir API Key
    config.headers['X-API-Key'] = API_KEY;
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Servicios de Autenticación
export const authService = {
  login: async (username: string, password: string) => {
    const response = await api.post('/api/auth/login-json', { username, password });
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
    }
    return response.data;
  },

  register: async (userData: any) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },

  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },

  getCurrentUser: () => {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('access_token');
  },
};

// Servicios de Analytics
export const analyticsService = {
  getDashboard: async (mes?: number) => {
    const response = await api.get('/api/analytics/dashboard-resumen', {
      params: { mes },
    });
    return response.data;
  },

  getProductosMasVendidos: async (mes?: number, categoria?: string, limite = 10) => {
    const response = await api.get('/api/analytics/productos-mas-vendidos', {
      params: { mes, categoria, limite },
    });
    return response.data;
  },

  getRotacionTallas: async (genero?: string) => {
    const response = await api.get('/api/analytics/rotacion-tallas', {
      params: { genero },
    });
    return response.data;
  },

  getAlertasStock: async () => {
    const response = await api.get('/api/analytics/alertas-stock');
    return response.data;
  },

  getComparativoGeneros: async (fechaInicio?: string, fechaFin?: string) => {
    const response = await api.get('/api/analytics/comparativo-generos', {
      params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin },
    });
    return response.data;
  },

  getRecomendaciones: async () => {
    const response = await api.get('/api/analytics/recomendaciones-inteligentes');
    return response.data;
  },

  getPredicciones: async (categoria?: string) => {
    const response = await api.get('/api/analytics/prediccion-ventas', {
      params: { categoria },
    });
    return response.data;
  },

  getReglasAsociacion: async (confianzaMinima = 0.5, soporteMinimo = 0.1) => {
    const response = await api.get('/api/analytics/reglas-asociacion', {
      params: { confianza_minima: confianzaMinima, soporte_minimo: soporteMinimo },
    });
    return response.data;
  },

  getRecomendacionesCruzadas: async (categoria: string) => {
    const response = await api.get(`/api/analytics/recomendaciones-cruzadas/${categoria}`);
    return response.data;
  },
};

// Servicio de Chatbot
export const chatbotService = {
  enviarMensaje: async (mensaje: string) => {
    const response = await api.post('/api/chatbot/mensaje', { mensaje });
    return response.data;
  },

  obtenerEjemplos: async () => {
    const response = await api.get('/api/chatbot/ejemplos');
    return response.data;
  },
};

export default api;

