import axios from 'axios';

// URL base do backend rodando no Docker
const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de Request: Injeta o Access Token em toda requisição (exceto login/cadastro caso omitido automaticamente no backend)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('@LocPlus:token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor de Response: A Mágica do Refresh Token
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    // Se o erro foi 401 (Não autorizado) e ainda não tentamos dar retry nesta request...
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Tenta buscar o refresh_token do storage
        const refreshToken = localStorage.getItem('@LocPlus:refresh_token');

        if (!refreshToken) {
          // Sem refresh ou token ausente. Força logout limpando o localstorage
          localStorage.removeItem('@LocPlus:token');
          localStorage.removeItem('@LocPlus:refresh_token');
          localStorage.removeItem('@LocPlus:user');
          window.location.href = '/login';
          return Promise.reject(error);
        }

        // Bate silenciosamente na API na rota de Refresh
        // Usamos post global (axios.post) para evitar loops infinitos dentro dessa mesma instancia api interceptada
        const response = await axios.post(`${API_URL}/usuarios/refresh`, {
          refresh_token: refreshToken
        });

        const { access_token } = response.data;

        // Salva o novo access token
        localStorage.setItem('@LocPlus:token', access_token);

        // Atualiza a request original estancada e a refaz!
        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);

      } catch (refreshError) {
        // Se a própria requisição de refresh falhar (Refresh Token já expirou nos 7 dias também)
        localStorage.removeItem('@LocPlus:token');
        localStorage.removeItem('@LocPlus:refresh_token');
        localStorage.removeItem('@LocPlus:user');
        
        // Empurra para  a tela de login e encerra
        window.location.href = '/login'; 
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
