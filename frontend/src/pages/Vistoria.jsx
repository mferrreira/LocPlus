import { useState } from 'react'
import { api } from '../services/api'
import { Camera, Upload, ShieldCheck } from 'lucide-react'

export default function Vistoria() {
  const [foto, setFoto] = useState(null)
  const [tipo, setTipo] = useState('entrega')
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({ locacao_id: '', horimetro_odometro: '', nivel_combustivel: 'Cheio', observacoes: '' })
  const [checks, setChecks] = useState({ pneus: true, vidros: true, lataria: true, painel: true, hidraulica: true })
  const [status, setStatus] = useState('')

  const handleText = e => setForm({...form, [e.target.name]: e.target.value})
  const handleCheck = e => setChecks({...checks, [e.target.name]: e.target.checked})
  
  const submitVistoria = async (e) => {
    e.preventDefault()
    setStatus('')
    setLoading(true)
    
    try {
      const formPayload = new FormData()
      formPayload.append('locacao_id', form.locacao_id)
      formPayload.append('tipo', tipo)
      if (form.horimetro_odometro) formPayload.append('horimetro_odometro', form.horimetro_odometro)
      formPayload.append('nivel_combustivel', form.nivel_combustivel)
      formPayload.append('observacoes', form.observacoes)
      formPayload.append('check_pneus', checks.pneus)
      formPayload.append('check_vidros', checks.vidros)
      formPayload.append('check_lataria', checks.lataria)
      formPayload.append('check_painel', checks.painel)
      formPayload.append('check_hidraulica', checks.hidraulica)
      
      if (foto) formPayload.append('foto', foto)
      
      await api.post('/vistorias/', formPayload, { headers: { 'Content-Type': 'multipart/form-data' } })
      setStatus('✅ Vistoria registrada! Foto enviada para a nuvem.')
      // Limpa pra próxima máquina da fila
      setFoto(null)
      setForm({...form, horimetro_odometro: '', observacoes: ''})
    } catch (err) {
      setStatus('❌ Erro: ' + (err.response?.data?.detail || 'Verifique o ID da locação.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto bg-white p-8 rounded-xl shadow-lg border">
       <div className="flex items-center justify-between mb-8 border-b pb-4">
         <div className="flex items-center">
           <ShieldCheck className="w-10 h-10 text-green-600 mr-3" />
           <h2 className="text-2xl font-bold">Câmera de Vistoria</h2>
         </div>
         <span className="bg-gray-100 text-gray-600 px-3 py-1 rounded text-sm font-bold">App Field</span>
       </div>

       {status && <div className={`p-4 rounded-lg mb-6 font-bold text-center ${status.includes('❌') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-700'}`}>{status}</div>}

       <form onSubmit={submitVistoria} className="space-y-6">
         <div className="grid grid-cols-2 gap-4">
           <div>
             <label className="block text-sm font-medium text-gray-700 mb-1">Contrato (ID HASH)</label>
             <input type="number" name="locacao_id" value={form.locacao_id} onChange={handleText} required className="w-full border-2 border-gray-200 rounded-lg p-3 focus:border-green-600 outline-none font-mono text-center text-lg" placeholder="0000" />
           </div>
           <div>
             <label className="block text-sm font-medium text-gray-700 mb-1">Etapa do Contrato</label>
             <select value={tipo} onChange={e=>setTipo(e.target.value)} className="w-full border-2 border-gray-200 rounded-lg p-3 focus:border-green-600 outline-none font-bold">
               <option value="entrega">Saída (Locador)</option>
               <option value="devolucao">Retorno (Devolução)</option>
             </select>
           </div>
         </div>

         <div className="bg-gray-50 border p-5 rounded-xl space-y-4">
            <h3 className="font-bold text-gray-800">Métricas e Conformidade Físicas</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm text-gray-600 font-medium">Horímetro / Odômetro</label>
                <input type="number" step="0.1" name="horimetro_odometro" value={form.horimetro_odometro} onChange={handleText} className="w-full border rounded p-2 mt-1" placeholder="Ex: 1205.5" />
              </div>
              <div>
                <label className="text-sm text-gray-600 font-medium">Tanque de Combustível</label>
                <select name="nivel_combustivel" value={form.nivel_combustivel} onChange={handleText} className="w-full border rounded p-2 mt-1">
                  <option value="Cheio">Cheio</option><option value="3/4">3/4</option><option value="1/2">Meio-Tanque (1/2)</option><option value="1/4">1/4</option><option value="Reserva">Reserva</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mt-5">
              <label className="flex items-center space-x-2 bg-white border p-3 rounded-lg shadow-sm cursor-pointer hover:bg-gray-50">
                <input type="checkbox" name="pneus" checked={checks.pneus} onChange={handleCheck} className="w-4 h-4" /> <span className="text-sm font-medium">Pneus OK</span>
              </label>
              <label className="flex items-center space-x-2 bg-white border p-3 rounded-lg shadow-sm cursor-pointer hover:bg-gray-50">
                <input type="checkbox" name="vidros" checked={checks.vidros} onChange={handleCheck} className="w-4 h-4" /> <span className="text-sm font-medium">Vidros OK</span>
              </label>
              <label className="flex items-center space-x-2 bg-white border p-3 rounded-lg shadow-sm cursor-pointer hover:bg-gray-50">
                <input type="checkbox" name="lataria" checked={checks.lataria} onChange={handleCheck} className="w-4 h-4" /> <span className="text-sm font-medium">Lataria OK</span>
              </label>
              <label className="flex items-center space-x-2 bg-white border p-3 rounded-lg shadow-sm cursor-pointer hover:bg-gray-50">
                <input type="checkbox" name="painel" checked={checks.painel} onChange={handleCheck} className="w-4 h-4" /> <span className="text-sm font-medium">Painel OK</span>
              </label>
              <label className="flex items-center space-x-2 bg-white border p-3 rounded-lg shadow-sm cursor-pointer hover:bg-gray-50">
                <input type="checkbox" name="hidraulica" checked={checks.hidraulica} onChange={handleCheck} className="w-4 h-4" /> <span className="text-sm font-medium">Cilindros OK</span>
              </label>
            </div>
         </div>

         <div className="border-2 border-dashed border-gray-300 bg-gray-50 p-8 rounded-xl text-center hover:bg-blue-50 transition-colors relative overflow-hidden">
            <div className="flex flex-col items-center">
              <Camera className="h-12 w-12 text-gray-400 mb-2" />
              <p className="font-bold text-gray-700">Acionar Câmera Nativa</p>
              <p className="text-xs text-gray-500 mt-1">Abre nativamente em Celulares e Tablets</p>
            </div>
            {/* Input Oculto mas expandido sob toda a div */}
            <input type="file" onChange={e=>setFoto(e.target.files[0])} accept="image/*" capture="environment" className="absolute inset-0 w-full h-full opacity-0 cursor-pointer" />
            {foto && <div className="absolute bottom-0 inset-x-0 bg-green-500 text-white text-sm py-1 font-bold">Arquivo Atachado: {foto.name}</div>}
         </div>

         <div>
           <label className="block text-sm font-medium text-gray-700 mb-1">Ressalvas Estruturais</label>
           <textarea name="observacoes" value={form.observacoes} onChange={handleText} className="w-full border rounded-lg p-3 outline-none focus:border-green-600" rows="2" placeholder="Ex: Retrovisor descascado."></textarea>
         </div>

         <button type="submit" disabled={loading} className="w-full bg-green-600 hover:bg-green-700 text-white font-extrabold py-4 rounded-xl shadow-lg transition-transform hover:scale-[1.02]">
           {loading ? 'Subindo Cloud...' : 'Validar Auto-Vistoria Digitally'}
         </button>
       </form>
    </div>
  )
}
