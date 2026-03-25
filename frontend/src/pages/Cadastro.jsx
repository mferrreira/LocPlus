import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { api } from '../services/api'
import { UserPlus } from 'lucide-react'

export default function Cadastro() {
  const navigate = useNavigate()
  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState(false)
  
  const [formData, setFormData] = useState({
    nome_completo: '', email: '', senha: '', objetivo: 'alugar_maquinas', tipo_entidade: 'pessoa_fisica',
    documento: '', telefone_celular: '', 
    rg: '', data_nascimento: '',
    razao_social: '', nome_fantasia: '', inscricao_estadual: ''
  })

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value})
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro('')
    try {
      // Filtramos dinamicamente porque o pydantic do backend fará model_validator de PF e PJ
      const payload = { ...formData }
      if (payload.tipo_entidade === 'pessoa_fisica') {
        delete payload.razao_social
        delete payload.nome_fantasia
        delete payload.inscricao_estadual
      } else {
        delete payload.rg
        delete payload.data_nascimento
      }
      
      await api.post('/usuarios/cadastro', payload)
      setSucesso(true)
      setTimeout(() => navigate('/login'), 2000)
    } catch (err) {
      setErro(err.response?.data?.detail || 'Verifique seus dados obrigatórios no formulário.')
    }
  }

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded shadow-sm border border-gray-100 mt-10">
      <div className="flex items-center mb-6 border-b pb-4">
        <UserPlus className="w-8 h-8 text-blue-600 mr-2" />
        <h2 className="text-2xl font-bold">Criar nova conta</h2>
      </div>
      
      {erro && <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm">{erro}</div>}
      {sucesso && <div className="bg-green-50 text-green-600 p-3 rounded mb-4 text-sm">Conta criada com sucesso! Redirecionando...</div>}
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Objetivo na Plataforma</label>
            <select name="objetivo" value={formData.objetivo} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border">
              <option value="alugar_maquinas">Quero Alugar Máquinas</option>
              <option value="disponibilizar_maquinas">Quero Disponibilizar Máquinas</option>
            </select>
          </div>
          <div>
             <label className="block text-sm font-medium text-gray-700">Tipo de Entidade</label>
             <select name="tipo_entidade" value={formData.tipo_entidade} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border">
               <option value="pessoa_fisica">Pessoa Física</option>
               <option value="pessoa_juridica">Pessoa Jurídica</option>
             </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nome Completo</label>
            <input type="text" name="nome_completo" value={formData.nome_completo} onChange={handleChange} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">E-mail</label>
            <input type="email" name="email" value={formData.email} onChange={handleChange} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:border-blue-500" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Senha Segura</label>
            <input type="password" name="senha" value={formData.senha} onChange={handleChange} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" minLength={6} />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Documento (CPF/CNPJ)</label>
            <input type="text" name="documento" value={formData.documento} onChange={handleChange} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
          </div>
        </div>

        <div>
           <label className="block text-sm font-medium text-gray-700">Celular (WhatsApp)</label>
           <input type="text" name="telefone_celular" value={formData.telefone_celular} onChange={handleChange} required className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
        </div>

        {formData.tipo_entidade === 'pessoa_fisica' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-50 p-4 rounded border">
            <div>
              <label className="block text-sm font-medium text-gray-700">RG</label>
              <input type="text" name="rg" value={formData.rg} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Data de Nascimento</label>
              <input type="date" name="data_nascimento" value={formData.data_nascimento} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
            </div>
          </div>
        )}

        {formData.tipo_entidade === 'pessoa_juridica' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-gray-50 p-4 rounded border">
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700">Razão Social</label>
              <input type="text" name="razao_social" value={formData.razao_social} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Nome Fantasia</label>
              <input type="text" name="nome_fantasia" value={formData.nome_fantasia} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Inscrição Estadual</label>
              <input type="text" name="inscricao_estadual" value={formData.inscricao_estadual} onChange={handleChange} className="mt-1 block w-full rounded border-gray-300 shadow-sm p-2 border focus:ring-blue-500" />
            </div>
          </div>
        )}

        <button type="submit" className="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-4 rounded transition-colors mt-6">
          Finalizar Cadastro
        </button>
      </form>
    </div>
  )
}
