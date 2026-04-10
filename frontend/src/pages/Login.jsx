import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Building2, KeyRound } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const res = await login(email, senha);
    if (res.success) {
      navigate('/painel');
    } else {
      setError(res.message);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="bg-gray-900 border border-gray-800 p-8 rounded-xl shadow-2xl w-full max-w-md">
        <div className="flex flex-col items-center mb-8">
          <div className="bg-emerald-500/10 p-4 rounded-full mb-4">
            <Building2 className="w-8 h-8 text-emerald-500" />
          </div>
          <h1 className="text-2xl font-bold text-white text-center">LocPlus Enterprise</h1>
          <p className="text-gray-400 text-sm mt-1">Acesso exclusivo para parceiros B2B</p>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-3 rounded-lg mb-6 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">E-mail Corporativo</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
              placeholder="contato@locadora.com"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">Senha de Acesso</label>
            <div className="relative">
              <input
                type="password"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
                className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-colors"
                placeholder="••••••••"
              />
              <KeyRound className="absolute right-3 top-3.5 w-5 h-5 text-gray-600" />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 rounded-lg transition-colors disabled:opacity-50 mt-4"
          >
            {loading ? 'Autenticando...' : 'Acessar Central'}
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-gray-800 text-center">
          <p className="text-gray-400 text-sm">
            Não tem uma conta em nossa rede?{' '}
            <Link to="/cadastro" className="text-emerald-500 hover:text-emerald-400 font-medium">
              Cadastre sua Locadora
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
