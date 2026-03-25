import { Link } from 'react-router-dom'

export default function EquipamentoCard({ equipamento }) {
  // Trata disponibilidade visual (Passo 6.3.3)
  const disponivel = equipamento.quantidade_disponivel > 0
  
  return (
    <div className={`bg-white rounded-xl shadow-sm overflow-hidden border transition-all hover:shadow-md ${!disponivel ? 'opacity-75 grayscale' : 'border-gray-200'}`}>
      {/* Imagem S3 Nativa ou Placeholder Estilizado */}
      <div className="h-48 bg-gray-100 w-full relative">
        {equipamento.foto_visao_geral ? (
          <img src={equipamento.foto_visao_geral} alt={equipamento.nome} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-400 font-medium bg-gray-200">
            Sem Imagem
          </div>
        )}
        
        {!disponivel && (
           <div className="absolute top-2 right-2 bg-red-600 text-white text-xs px-3 py-1 rounded-full font-bold shadow">
             ALUGADA
           </div>
        )}
      </div>

      <div className="p-5">
        <div className="mb-2">
          <span className="text-xs font-bold text-gray-400 uppercase tracking-wider">
            {equipamento.categoria.replace('_', ' ')}
          </span>
          <h3 className="text-lg font-bold text-gray-900 line-clamp-1 mt-1">{equipamento.nome}</h3>
        </div>
        
        <p className="text-sm text-gray-600 mb-5 line-clamp-2 min-h-10">
          {equipamento.descricao || 'Nenhuma descrição técnica informada.'}
        </p>
        
        <div className="flex justify-between items-center bg-gray-50 p-4 rounded-lg text-sm border">
          <div>
            <p className="text-gray-500 text-xs font-medium mb-1">Valor Diária</p>
            <p className="text-xl font-bold text-blue-700">
              {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(equipamento.valor_diaria)}
            </p>
          </div>
          <Link to={`/equipamentos/${equipamento.id}`} className="bg-white border-2 border-blue-600 text-blue-600 hover:bg-blue-50 px-4 py-2 rounded-lg transition-colors text-sm font-bold shadow-sm">
            Detalhes
          </Link>
        </div>
      </div>
    </div>
  )
}
