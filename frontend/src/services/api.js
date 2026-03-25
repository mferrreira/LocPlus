import axios from "axios";

// Singleton do Axios para conexão com a API Node/FastAPI
export const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "Content-Type": "application/json"
  }
});

// Gestão manual e ultra-simples de cache e JWT
export const StorageService = {
  setToken: (token) => localStorage.setItem("locplus_token", token),
  getToken: () => localStorage.getItem("locplus_token"),
  logout: () => localStorage.removeItem("locplus_token")
};
