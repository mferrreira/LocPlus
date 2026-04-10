import { useState, useEffect } from 'react'
import { api, StorageService } from '../services/api'
import { Shield, Upload, MapPin, Plus, CheckCircle, Clock } from 'lucide-react'

export default function Perfil() {
  const [docs, setDocs] = useState([])
  const [enderecos, setEnderecos] = useState([])
  const [loading, setLoading] = useState(true)
  const [fotoUpload, setFotoUpload] = useState(null)
  const [fotoTipo, setFotoTipo] = useState('cnh')
  
  const token = StorageService.getToken()

  const carregarDashboard = async () => {
    try {
      const [resKyc, resEnd] = await Promise.all([
        api.get('/kyc'),
        api.get('/enderecos')
      ])
      setDocs(resKyc.data)
      setEnderecos(resEnd.data)
      setLoading(false)
    } catch (err) {
      console.error(err)
      setLoading(false)
    }
  }

  useEffect(() => {
    if (token) carregarDashboard()
  }, [token])

  const handleUploadKyc = async (e) => {
    e.preventDefault()
    if (!fotoUpload) return alert('Selecione um arquivo PDF ou Imagem!')

    const formData = new FormData()
    formData.append('tipo', fotoTipo)
    formData.append('file', fotoUpload)

    try {
      await api.post('/kyc/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      alert('Documento enviado para análise com sucesso!')
      setFotoUpload(null)
      carregarDashboard()
    } catch (err) {
      alert('Erro ao enviar documento. Tente novamente.')
    }
  }

  if (loading) return <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto mt-20"></div>

  const contaAprovada = docs.some(d => d.status === 'aprovado')

  return (
    <div className="max-w-6xl mx-auto p-6 mt-6 space-y-8 animate-fade-in">
      
      {/* HEADER DE SAÚDE DA CONTA */}
      <div className="bg-white rounded-2xl p-8 shadow-sm border flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-gray-900">Meu Painel B2B</h1>
          <p className="text-gray-500 mt-2">Gerencie a confiança fiscal e a logística da sua frota.</p>
        </div>
        <div className={`px-6 py-3 rounded-full flex items-center font-bold shadow-sm ${contaAprovada ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
          {contaAprovada ? <CheckCircle className="w-5 h-5 mr-2"/> : <Clock className="w-5 h-5 mr-2"/>}
          {contaAprovada ? 'Conta Verificada KYC' : 'Em Análise de Risco'}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        
        {/* PAINE: DOCUMENTOS KYC */}
        <div className="bg-white rounded-2xl shadow-sm border p-8">
           <div className="flex items-center mb-6">
             <Shield className="w-8 h-8 text-blue-600 mr-3" />
             <h2 className="text-2xl font-bold text-gray-900">Documentos KYC</h2>
           </div>
           <p className="text-gray-500 mb-6">Faça o upload do seu RG/CNH ou Contrato Social para desbloquear aluguéis de máquinas pesadas.</p>
           
           <form onSubmit={handleUploadKyc} className="bg-gray-50 p-6 rounded-xl border border-gray-200 mb-8 space-y-4">
             <div>
               <label className="block text-sm font-bold text-gray-700">Tipo de Documento</label>
               <select value={fotoTipo} onChange={e => setFotoTipo(e.target.value)} className="w-full mt-1 p-2 rounded border focus:ring-blue-500">
                 <option value="cnh">CNH Motorista</option>
                 <option value="rg">RG Identidade</option>
                 <option value="contrato_social">Contrato Social (PJ)</option>
                 <option value="comprovante_residencia">Comprovante de Endereço</option>
               </select>
             </div>
             <div>
               <input type="file" onChange={e => setFotoUpload(e.target.files[0])} className="w-full mt-1 p-2 bg-white rounded border focus:ring-blue-500" />
             </div>
             <button type="submit" className="w-full flex justify-center items-center py-3 bg-gray-900 hover:bg-black text-white font-bold rounded-lg transition">
               <Upload className="w-5 h-5 mr-2"/> Enviar para o S3 MinIO
             </button>
           </form>

           <div className="space-y-3">
             {docs.map(doc => (
               <div key={doc.id} className="flex justify-between items-center p-4 border rounded-xl">
                 <span className="uppercase font-bold text-gray-700 text-sm">{doc.tipo_documento.replace('_', ' ')}</span>
                 <span className={`px-3 py-1 rounded-full text-xs font-bold ${doc.status === 'aprovado' ? 'bg-green-100 text-green-700' : doc.status === 'rejeitado' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                   {doc.status}
                 </span>
               </div>
             ))}
             {docs.length === 0 && <p className="text-center text-gray-400 font-medium py-4">Nenhum documento enviado ainda.</p>}
           </div>
        </div>

        {/* PAINE: ENDEREÇOS B2B */}
        <div className="bg-white rounded-2xl shadow-sm border p-8">
           <div className="flex items-center justify-between mb-6">
             <div className="flex items-center">
               <MapPin className="w-8 h-8 text-green-600 mr-3" />
               <h2 className="text-2xl font-bold text-gray-900">Meus Canteiros</h2>
             </div>
             <button className="flex items-center text-blue-600 hover:text-blue-800 font-bold bg-blue-50 px-4 py-2 rounded-lg transition">
               <Plus className="w-5 h-5 mr-1"/> Canteiro
             </button>
           </div>
           <p className="text-gray-500 mb-6">Cadastre as Obras, Galpões ou Sedes para onde o maquinário será roteirizado nos fretes.</p>

           <div className="space-y-4">
             {enderecos.map(end => (
               <div key={end.id} className="p-4 border rounded-xl hover:shadow-md transition relative overflow-hidden">
                 {end.is_padrao && <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>}
                 <div className="flex justify-between">
                   <h3 className="font-bold text-gray-900 uppercase tracking-wide">{end.tipo.replace('_', ' ')}</h3>
                   {end.is_padrao && <span className="text-xs text-blue-600 font-bold bg-blue-50 px-2 py-1 rounded">PADRÃO</span>}
                 </div>
                 <p className="text-gray-600 text-sm mt-1">{end.logradouro}, {end.numero}</p>
                 <p className="text-gray-500 text-sm">{end.bairro} - {end.cidade}/{end.estado} • CEP: {end.cep}</p>
               </div>
             ))}
             {enderecos.length === 0 && (
               <div className="text-center p-8 border-2 border-dashed rounded-xl">
                  <p className="text-gray-500 font-medium mb-4">Nenhum endereço logístico cadastrado.</p>
               </div>
             )}
           </div>
        </div>

      </div>
    </div>
  )
}
