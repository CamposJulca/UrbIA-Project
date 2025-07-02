import axios from 'axios';

// Base URL configurable desde variable de entorno o fallback local
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Crear instancia de Axios
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para incluir token JWT si existe
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // si estás usando auth
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// =======================
// Funciones API disponibles
// =======================

export const fetchDevices = async () => {
  const response = await api.get('/api/devices');
  return response.data;
};

export const fetchTelemetry = async (deviceId) => {
  const response = await api.get(`/api/devices/${deviceId}/telemetry`);
  return response.data;
};

export default api;
