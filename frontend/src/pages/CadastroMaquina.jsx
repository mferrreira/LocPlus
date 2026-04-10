import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { PlusCircle } from 'lucide-react'

export default function CadastroMaquina() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState(false)
  const [form, setForm] = useState({
    nome: '', descricao: '', categoria: 'linha_pesada', marca: '', modelo: '', ano_fabricacao: '',
    valor_diaria: '', valor_semana: '', valor_quinzena: '', valor_mes: '',
    quantidade_total: 1, numero_serie_patrimonio: '', empresa_id: 1 // mock locador_id por simplicidade
  })

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setErro('')
    try {
      await api.post('/equipamentos/', {
        ...form, 
        ano_fabricacao: parseInt(form.ano_fabricacao) || null,
        valor_diaria: parseFloat(form.valor_diaria),
        valor_semana: form.valor_semana ? parseFloat(form.valor_semana) : null,
        valor_quinzena: form.valor_quinzena ? parseFloat(form.valor_quinzena) : null,
        valor_mes: form.valor_mes ? parseFloat(form.valor_mes) : null,
        empresa_id: parseInt(form.empresa_id)
      })
      setSucesso(true)
      setTimeout(() => navigate('/'), 2500)
    } catch (err) {
      setErro(err.response?.data?.detail || 'Erro ao registrar máquina.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-8 rounded-xl shadow border mb-20">
       <div className="flex items-center mb-6 border-b pb-4">
         <PlusCircle className="w-8 h-8 text-blue-600 mr-2" />
         <h2 className="text-2xl font-bold">Cadastrar Novo Equipamento</h2>
       </div>
       {erro && <div className="bg-red-50 text-red-600 p-3 rounded mb-4 text-sm font-bold">{erro}</div>}
       {sucesso && <div className="bg-green-50 text-green-600 p-3 rounded mb-4 text-sm font-bold">Máquina cadastrada com sucesso! Retornando ao catálogo...</div>}
       
       <form onSubmit={handleSubmit} className="space-y-6">
         <div className="bg-gray-50 p-5 rounded-lg border space-y-4">
           <h3 className="font-bold text-gray-700 border-b pb-2">Identificação Base</h3>
           <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
             <div className="col-span-2">
               <label className="block text-sm font-medium text-gray-700">Nome Resumido *</label>
               <input name="nome" value={form.nome} onChange={handleChange} required className="mt-1 w-full rounded border p-2 focus:ring-blue-500" />
             </div>
             <div>
                <label className="block text-sm font-medium text-gray-700">Categoria *</label>
                <select name="categoria" value={form.categoria} onChange={handleChange} className="mt-1 w-full rounded border p-2">
                  <option value="linha_pesada">Linha Pesada (Tratores, Munck)</option>
                  <option value="linha_leve">Linha Leve (Betoneiras, Andaimes)</option>
                  <option value="veiculos">Veículos de Apoio Logístico</option>
                  <option value="mensalistas">Estruturas Fixas Mensalistas</option>
                  <option value="diversos">Ferramentas Industriais & Gerais</option>
                </select>
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Número de Frota</label>
               <input name="numero_serie_patrimonio" value={form.numero_serie_patrimonio} onChange={handleChange} className="mt-1 w-full rounded border p-2 focus:ring-blue-500" />
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Marca</label>
               <input name="marca" value={form.marca} onChange={handleChange} className="mt-1 w-full rounded border p-2 focus:ring-blue-500" />
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Modelo</label>
               <input name="modelo" value={form.modelo} onChange={handleChange} className="mt-1 w-full rounded border p-2 focus:ring-blue-500" />
             </div>
             
             <div className="col-span-2">
               <label className="block text-sm font-medium text-gray-700">Descrição Técnica *</label>
               <textarea name="descricao" value={form.descricao} onChange={handleChange} rows="3" placeholder="Ex: Capacidade 500L, voltagem 220V..." className="mt-1 w-full rounded border p-2 focus:ring-blue-500"></textarea>
             </div>
           </div>
         </div>
         
         <div className="bg-blue-50 p-5 rounded-lg border border-blue-200 space-y-4">
           <h3 className="font-bold text-blue-800 border-b border-blue-200 pb-2">Precificação Modular</h3>
           <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
             <div>
               <label className="block text-sm font-medium text-gray-700">Diária (R$) *</label>
               <input type="number" step="0.01" name="valor_diaria" value={form.valor_diaria} onChange={handleChange} required className="mt-1 w-full rounded border p-2 font-bold text-blue-700" />
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Semana (R$)</label>
               <input type="number" step="0.01" name="valor_semana" value={form.valor_semana} onChange={handleChange} className="mt-1 w-full rounded border p-2" />
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Quinzena (R$)</label>
               <input type="number" step="0.01" name="valor_quinzena" value={form.valor_quinzena} onChange={handleChange} className="mt-1 w-full rounded border p-2" />
             </div>
             <div>
               <label className="block text-sm font-medium text-gray-700">Mês (R$)</label>
               <input type="number" step="0.01" name="valor_mes" value={form.valor_mes} onChange={handleChange} className="mt-1 w-full rounded border p-2" />
             </div>
           </div>
         </div>
         
         <button type="submit" disabled={loading} className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-lg shadow">
           {loading ? 'Sincronizando...' : 'Publicar Equipamento'}
         </button>
       </form>
    </div>
  )
}
