import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Search, MapPin, Building2, PackageCheck } from 'lucide-react';
import ModalAluguel from '../components/ModalAluguel';

export default function Catalogo() {
  const [maquinas, setMaquinas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');
  
  // Controle de Modal de Aluguel
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedMaquina, setSelectedMaquina] = useState(null);

  const fetchCatalogo = async () => {
    try {
      const response = await api.get('/catalogo/maquinas');
      setMaquinas(response.data);
    } catch (err) {
      setErro('Erro ao carregar o catálogo de máquinas.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCatalogo();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Search/Header Area */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Marketplace de Máquinas</h1>
        <p className="text-gray-500 mb-6">Busque, encontre e alugue os melhores equipamentos direto com os fornecedores da sua região.</p>
        
        <div className="flex bg-gray-50 border border-gray-200 rounded-lg p-2 max-w-2xl">
          <div className="flex-1 flex items-center px-4">
            <Search className="w-5 h-5 text-gray-400 mr-2" />
            <input 
              type="text" 
              placeholder="Ex: Trator, Betoneira, Andaime..." 
              className="bg-transparent w-full outline-none text-gray-700"
            />
          </div>
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-md font-medium transition-colors">
            Buscar
          </button>
        </div>
      </div>

      {erro && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg font-medium">
          {erro}
        </div>
      )}

      {/* Grid de Máquinas */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {maquinas.map((maq) => {
          const isDisponivel = maq.quantidade_disponivel > 0;

          return (
            <div 
              key={maq.id} 
              className={`bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col transition-all ${!isDisponivel ? 'opacity-60 grayscale-[0.5]' : 'hover:shadow-md hover:border-blue-300'}`}
            >
              {/* Image Placeholder */}
              <div className="bg-gray-200 h-48 w-full relative flex items-center justify-center">
                <span className="text-gray-400 font-medium font-mono text-sm uppercase tracking-widest">{maq.categoria?.replace('_', ' ')}</span>
                
                {/* Status Tag */}
                <div className="absolute top-3 right-3">
                  {isDisponivel ? (
                    <span className="bg-emerald-100 text-emerald-800 text-xs px-3 py-1 rounded-full font-bold flex items-center shadow-sm">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span>
                      Disponível
                    </span>
                  ) : (
                    <span className="bg-red-100 text-red-800 text-xs px-3 py-1 rounded-full font-bold shadow-sm border border-red-200">
                      Alugada
                    </span>
                  )}
                </div>
              </div>

              <div className="p-5 flex flex-col flex-1">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-bold text-gray-900 line-clamp-1" title={maq.nome}>{maq.nome}</h3>
                </div>
                
                {/* Locadora Info */}
                <div className="flex items-center text-sm text-gray-500 mb-4 bg-gray-50 p-2 rounded border border-gray-100">
                  <Building2 className="w-4 h-4 mr-2 text-blue-500" />
                  <span className="font-medium text-gray-700 truncate" title={maq.empresa?.nome_fantasia}>
                    {maq.empresa?.nome_fantasia || 'Locadora Padrão'}
                  </span>
                  {maq.empresa?.avaliacao && (
                    <span className="ml-auto flex items-center text-amber-500 text-xs font-bold">
                      ★ {maq.empresa.avaliacao.toFixed(1)}
                    </span>
                  )}
                </div>

                <div className="mt-auto pt-4 border-t border-gray-100 flex justify-between items-end">
                  <div>
                    <p className="text-xs text-gray-500 font-medium uppercase tracking-wider mb-1">Valor Diária</p>
                    <p className="text-2xl font-black text-blue-700">
                      {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(maq.valor_diaria)}
                    </p>
                  </div>
                  <button 
                    disabled={!isDisponivel}
                    onClick={() => { setSelectedMaquina(maq); setIsModalOpen(true); }}
                    className={`px-4 py-2 rounded-lg font-bold transition-colors ${
                      isDisponivel 
                      ? 'bg-blue-50 text-blue-700 hover:bg-blue-600 hover:text-white border border-blue-200 hover:border-transparent' 
                      : 'bg-gray-100 text-gray-400 cursor-not-allowed border border-gray-200'
                    }`}
                  >
                    Alugar
                  </button>
                </div>
              </div>
            </div>
          );
        })}

        {maquinas.length === 0 && !loading && !erro && (
           <div className="col-span-full py-12 text-center text-gray-500">
             <PackageCheck className="w-12 h-12 mx-auto mb-3 text-gray-300" />
             <p className="text-lg font-medium">Nenhum equipamento logado nesta região.</p>
           </div>
        )}
      </div>

      <ModalAluguel
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        maquina={selectedMaquina}
        onSuccess={fetchCatalogo}
      />
    </div>
  );
}
