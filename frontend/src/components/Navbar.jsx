import { Link } from 'react-router-dom'
import { StorageService } from '../services/api'

export default function Navbar() {
  const token = StorageService.getToken()

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-blue-600">LocPlus</Link>
        <div className="space-x-4 flex items-center">
          <Link to="/" className="text-gray-600 hover:text-blue-600 font-medium">Vitrine</Link>
          {token ? (
             <>
              <Link to="/add-maquina" className="text-gray-600 hover:text-blue-600 font-medium">+ Frota</Link>
              <Link to="/terminal-vistoria" className="text-gray-600 hover:text-blue-600 font-medium">Vistorias</Link>
              <button onClick={() => { StorageService.logout(); window.location.reload(); }} className="text-gray-600 hover:text-red-600 font-medium ml-4">Sair</button>
             </>
          ) : (
             <Link to="/login" className="bg-blue-600 text-white px-4 py-2 rounded">Entrar / Cadastro</Link>
          )}
        </div>
      </div>
    </nav>
  )
}
