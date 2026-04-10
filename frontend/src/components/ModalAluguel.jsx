import React, { useState, useEffect } from 'react';
import { X, Calendar, CheckCircle2 } from 'lucide-react';
import api from '../services/api';

import { useAuth } from '../contexts/AuthContext';

export default function ModalAluguel({ isOpen, onClose, maquina, onSuccess }) {
  const { user } = useAuth();
  const [dataInicio, setDataInicio] = useState('');
  const [dataFim, setDataFim] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Reatividade de cálculo
  const [diasEstimados, setDiasEstimados] = useState(1);
  const [valorTotalEstimado, setValorTotalEstimado] = useState(0);

  useEffect(() => {
    if (dataInicio && dataFim && maquina) {
      const start = new Date(dataInicio);
      const end = new Date(dataFim);
      
      // Diferença em milissegundos convertida para dias
      const diffTime = Math.abs(end - start);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
      
      // Regra de ouro Backend: Mínimo 1 diária caso comece e termine no mesmo dia (math.ceil = 0 cai no min(1))
      const diasCobrados = Math.max(1, diffDays);
      setDiasEstimados(diasCobrados);
      setValorTotalEstimado(diasCobrados * maquina.valor_diaria);
    } else if (maquina) {
      setDiasEstimados(1);
      setValorTotalEstimado(maquina.valor_diaria);
    }
  }, [dataInicio, dataFim, maquina]);

  if (!isOpen || !maquina) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!user?.cliente_id) {
       setError("Sua sessão é inválida para realizar aluguéis automáticos. Relogue.");
       setLoading(false);
       return;
    }

    // Prepara payload pro backend
    const payload = {
      equipamento_id: maquina.id,
      cliente_id: user.cliente_id, // Usando locatário verificado da sessão
      empresa_id: 0,
      data_inicio: new Date(dataInicio).toISOString(),
      data_fim_prevista: new Date(dataFim).toISOString()
    };

    try {
      await api.post('/locacoes/', payload);
      alert('Máquina reservada com sucesso no sistema!');
      onSuccess();
      onClose();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Não foi possível reservar essa máquina. Verifique datas ou estoque.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-lg overflow-hidden flex flex-col">
        
        {/* Header Modal */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <h2 className="text-xl font-bold text-gray-800">Checkout Automático</h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6">
          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-lg text-sm font-medium border border-red-100">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </div>
          )}

          {/* Machine Header */}
          <div className="flex items-start gap-4 mb-8 bg-gray-50 p-4 rounded-xl border border-gray-200 shadow-sm">
             <div className="w-20 h-20 bg-gray-200 rounded-lg overflow-hidden shrink-0 flex items-center justify-center border border-gray-300">
               {maquina.foto_visao_geral ? (
                 <img src={maquina.foto_visao_geral} alt="maquina" className="w-full h-full object-cover" />
               ) : (
                 <span className="text-xs font-bold text-gray-400">NO FOTO</span>
               )}
             </div>
             <div>
               <h3 className="font-bold text-gray-900 text-lg">{maquina.nome}</h3>
               <p className="text-sm text-gray-500">Fornecida por: <span className="font-semibold">{maquina.empresa?.nome_fantasia || 'Locadora Local'}</span></p>
               <p className="mt-2 text-blue-700 font-black">
                 {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(maquina.valor_diaria)} <span className="text-xs font-normal text-gray-500 line-through">/dia</span>
               </p>
             </div>
          </div>

          <form id="form-aluguel" onSubmit={handleSubmit} className="space-y-5">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Início da Locação *</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
                  <input
                    type="date"
                    required
                    value={dataInicio}
                    onChange={(e) => setDataInicio(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-lg pl-10 pr-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Devolução *</label>
                <div className="relative">
                  <Calendar className="absolute left-3 top-2.5 w-5 h-5 text-gray-400" />
                  <input
                    type="date"
                    required
                    min={dataInicio}
                    value={dataFim}
                    onChange={(e) => setDataFim(e.target.value)}
                    className="w-full bg-white border border-gray-300 rounded-lg pl-10 pr-3 py-2 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                  />
                </div>
              </div>
            </div>

            {/* Calculadora em Tempo Real */}
            <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-5 mt-6 relative overflow-hidden">
               <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
               <div className="flex justify-between items-center mb-1">
                 <span className="text-blue-800 font-medium">Tempo de Contrato Estimado</span>
                 <span className="font-bold text-gray-900">{diasEstimados} diária(s)</span>
               </div>
               <div className="flex justify-between items-end border-t border-blue-200/50 pt-3 mt-3">
                 <span className="text-blue-900 font-bold tracking-tight">Valor Total Estimado</span>
                 <span className="text-3xl font-black text-blue-700 tracking-tight">
                   {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valorTotalEstimado)}
                 </span>
               </div>
            </div>
          </form>
        </div>

        {/* Footer actions */}
        <div className="px-6 py-4 border-t border-gray-100 flex justify-end gap-3 bg-gray-50/50">
          <button 
            type="button" 
            onClick={onClose}
            className="px-5 py-2.5 text-sm font-medium text-gray-600 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors"
          >
            Voltar
          </button>
          <button 
            type="submit" 
            form="form-aluguel"
            disabled={loading || !dataInicio || !dataFim}
            className="px-6 py-2.5 text-sm font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow flex items-center transition-colors disabled:opacity-50"
          >
            {loading ? 'Processando Contrato...' : 'Confirmar Locação'}
            {!loading && <CheckCircle2 className="w-4 h-4 ml-2" />}
          </button>
        </div>

      </div>
    </div>
  );
}
