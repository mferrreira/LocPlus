import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api';

const AuthContext = createContext({});

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Restaurar sessão silenciosamente quando abrir o navegador
    const storedUser = localStorage.getItem('@LocPlus:user');
    const storedToken = localStorage.getItem('@LocPlus:token');

    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
    }
    
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      // O FastAPI OAuth2 exige que seja Form-Data, não JSON (Body puro)
      const formData = new FormData();
      formData.append('username', email); // FASTAPI USA a chave username na documentação OAuth2, nós passamos o e-mail por ela!
      formData.append('password', password);
  
      // Esse POST NÃO passa interceptor ainda, se passar vai varrer localstorage em cima
      const response = await api.post('/usuarios/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
  
      const { access_token, refresh_token, tipo_entidade, objetivo, nome, cliente_id } = response.data;
  
      localStorage.setItem('@LocPlus:token', access_token);
      localStorage.setItem('@LocPlus:refresh_token', refresh_token);
      
      const userData = { nome, tipo_entidade, objetivo, cliente_id };
      localStorage.setItem('@LocPlus:user', JSON.stringify(userData));
      
      setUser(userData);
      
      return { success: true };
    } catch (error) {
      console.error("Erro no login:", error);
      return { 
        success: false, 
        message: error.response?.data?.detail || "Erro de conexão ao servidor." 
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('@LocPlus:token');
    localStorage.removeItem('@LocPlus:refresh_token');
    localStorage.removeItem('@LocPlus:user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated: !!user,
      user,
      login,
      logout,
      loading
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};
