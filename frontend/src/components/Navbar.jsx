import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">LocPlus</Link>
        <div className="space-x-4 flex items-center">
          <Link to="/catalogo" className="text-gray-600 hover:text-blue-600 font-semibold transition-colors mr-2">
            Catálogo
          </Link>
          
          {isAuthenticated ? (
            <div className="flex items-center space-x-4">
              {user?.cliente_id && (
                <Link to="/minhas-locacoes" className="text-gray-600 hover:text-blue-600 font-semibold transition-colors">
                  Meus Aluguéis
                </Link>
              )}
              <Link to="/dashboard" className="text-blue-700 bg-blue-50 px-4 py-2 rounded-lg font-bold hover:bg-blue-100 transition-colors">
                Meu Painel
              </Link>
              <button onClick={handleLogout} className="bg-red-50 text-red-600 px-4 py-2 rounded-lg font-bold hover:bg-red-100 transition-colors">
                Sair
              </button>
            </div>
          ) : (
            <Link to="/login" className="bg-blue-600 text-white px-4 py-2 rounded">Entrar / Cadastro</Link>
          )}
        </div>
      </div>
    </nav>
  )
}
