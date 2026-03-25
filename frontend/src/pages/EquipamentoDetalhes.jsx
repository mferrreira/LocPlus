import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { api, StorageService } from '../services/api'
import { ArrowLeft, CheckCircle, AlertTriangle, ShieldCheck } from 'lucide-react'

export default function EquipamentoDetalhes() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [eq, setEq] = useState(null)
  const [loading, setLoading] = useState(true)
  const token = StorageService.getToken()

  useEffect(() => {
    api.get(`/equipamentos/${id}`)
      .then(res => {
        setEq(res.data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [id])

  if (loading) return <div className="text-center mt-20"><div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600 mx-auto"></div></div>
  if (!eq) return <div className="text-center mt-20 font-bold text-red-600">Equipamento não encontrado.</div>

  const isLocado = eq.quantidade_disponivel === 0

  return (
    <div className="max-w-5xl mx-auto mt-4 mb-20">
      <button onClick={() => navigate(-1)} className="flex items-center text-blue-600 hover:text-blue-800 font-bold mb-6 transition-colors">
        <ArrowLeft className="w-5 h-5 mr-2" /> Voltar para o Catálogo
      </button>

      <div className="bg-white rounded-2xl shadow-lg border border-gray-100 overflow-hidden">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-0">
          {/* 1. Área de Imagem */}
          <div className="bg-gray-50 h-64 md:h-full min-h-[400px] flex items-center justify-center">
             {eq.foto_visao_geral ? (
               <img src={eq.foto_visao_geral} alt={eq.nome} className="w-full h-full object-cover" />
             ) : (
               <div className="text-gray-400 font-bold">FOTO DO MINIO AQUI</div>
             )}
          </div>

          {/* 2. Área de Texto e Checkout */}
          <div className="p-8 md:p-12 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start mb-4">
                <span className="bg-blue-100 text-blue-800 text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wide">{eq.categoria.replace('_', ' ')}</span>
                {isLocado ? (
                  <span className="flex items-center text-red-600 font-bold text-sm"><AlertTriangle className="w-4 h-4 mr-1"/> INDISPONÍVEL</span>
                ) : (
                  <span className="flex items-center text-green-600 font-bold text-sm"><CheckCircle className="w-4 h-4 mr-1"/> PRONTO PARA USO</span>
                )}
              </div>
              
              <h1 className="text-3xl font-extrabold text-gray-900 mb-2">{eq.nome}</h1>
              <p className="text-gray-500 mb-6">Nº de Frota: <span className="font-mono font-bold text-gray-700">{eq.numero_serie_patrimonio || 'N/A'}</span></p>
              
              <div className="border-t border-b py-4 my-6">
                <p className="text-gray-700 text-lg leading-relaxed">{eq.descricao}</p>
                
                <div className="grid grid-cols-2 gap-4 mt-6 text-sm text-gray-600">
                  <div><strong className="block text-gray-800">Marca</strong> {eq.marca || '-'}</div>
                  <div><strong className="block text-gray-800">Modelo</strong> {eq.modelo || '-'}</div>
                  <div><strong className="block text-gray-800">Ano</strong> {eq.ano_fabricacao || '-'}</div>
                </div>
              </div>
            </div>

            <div className="bg-gray-50 p-6 rounded-xl border">
              <p className="text-gray-500 text-sm font-bold uppercase mb-1">Valor Custo Diária</p>
              <p className="text-4xl font-extrabold text-blue-600 mb-4">
                R$ {eq.valor_diaria.toFixed(2).replace('.', ',')}
              </p>
              
              {!token ? (
                <Link to="/login" className="block w-full text-center bg-gray-800 hover:bg-gray-900 text-white font-bold py-4 rounded-lg transition">
                  Fazer Login para Alugar
                </Link>
              ) : (
                <button disabled={isLocado} className={`w-full py-4 rounded-lg font-extrabold text-lg transition shadow-md flex items-center justify-center ${isLocado ? 'bg-gray-300 text-gray-500 cursor-not-allowed' : 'bg-green-500 hover:bg-green-600 text-white'}`}>
                  <ShieldCheck className="w-6 h-6 mr-2" /> 
                  {isLocado ? 'Máquina Ocupada no Campo' : 'Assinar Contrato Agora'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
