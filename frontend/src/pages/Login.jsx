import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api, StorageService } from '../services/api'
import { LogIn } from 'lucide-react'

export default function Login() {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    setErro('')
    try {
      const res = await api.post('/usuarios/login', { email, senha })
      StorageService.setToken(res.data.access_token)
      window.location.href = '/' // Quick force refresh to update Navbar
    } catch (err) {
      setErro(err.response?.data?.detail || 'Erro na comunicação de Auth')
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white p-8 rounded shadow-sm border border-gray-100 mt-10">
      <div className="flex items-center justify-center mb-6">
        <LogIn className="w-8 h-8 text-blue-600 mr-2" />
        <h2 className="text-2xl font-bold">Acessar LocPlus</h2>
      </div>
      
      {erro && <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm">{erro}</div>}
      
      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">E-mail Corporativo/Pessoal</label>
          <input type="email" value={email} onChange={e=>setEmail(e.target.value)} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Senha de Acesso</label>
          <input type="password" value={senha} onChange={e=>setSenha(e.target.value)} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500 focus:border-blue-500" />
        </div>
        <button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded transition-colors">
          Entrar no Catálogo
        </button>
      </form>
      
      <div className="mt-6 text-center text-sm text-gray-600">
        Ainda não tem conta na Plataforma? <Link to="/cadastro" className="text-blue-600 hover:underline">Crie sua jornada LocPlus</Link>
      </div>
    </div>
  )
}
