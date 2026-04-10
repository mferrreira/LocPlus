import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { PackageOpen, Activity, AlertCircle, PlusCircle, CheckCircle2 } from 'lucide-react';
import ModalCadastroMaquina from '../components/ModalCadastroMaquina';
import ModalDevolucao from '../components/ModalDevolucao';

export default function Dashboard() {
  const { user } = useAuth();
  const [equipamentos, setEquipamentos] = useState([]);
  const [locacoes, setLocacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');
  
  const [isModalMaquinaOpen, setIsModalMaquinaOpen] = useState(false);
  const [isModalDevolucaoOpen, setIsModalDevolucaoOpen] = useState(false);
  const [selectedLocacao, setSelectedLocacao] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [resEquip, resLoc] = await Promise.all([
        api.get('/equipamentos/'),
        api.get('/locacoes/')
      ]);
      setEquipamentos(resEquip.data);
      setLocacoes(resLoc.data);
    } catch (err) {
      setErro('Erro ao carregar o seu painel.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header Saudação */}
      <div className="flex flex-col sm:flex-row sm:items-end justify-between border-b border-gray-200 pb-5">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Painel B2B</h1>
          <p className="text-gray-500 mt-1 text-lg">
            Olá, <span className="font-semibold text-gray-800">{user?.nome || 'Gestor'}</span>. Bem-vindo(a) ao seu centro de comando.
          </p>
        </div>
        
        <button 
          onClick={() => setIsModalMaquinaOpen(true)}
          className="mt-4 sm:mt-0 bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg font-medium flex items-center shadow-sm transition-colors cursor-pointer"
        >
          <PlusCircle className="w-5 h-5 mr-2" />
          Anunciar Nova Máquina
        </button>
      </div>

      {erro && (
        <div className="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-sm flex items-center">
          <AlertCircle className="w-5 h-5 mr-2" />
          {erro}
        </div>
      )}

      {/* Cards de Resumo */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500 uppercase tracking-widest mb-1">Total de Ativos</p>
              <h2 className="text-4xl font-black text-gray-900">{loading ? '-' : equipamentos.length}</h2>
            </div>
            <div className="bg-blue-50 p-3 rounded-lg">
              <PackageOpen className="w-6 h-6 text-blue-600" />
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-4 font-medium border-t border-gray-100 pt-3">
            Ativos físicos cadastrados.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500 uppercase tracking-widest mb-1">Inventário Ativo</p>
              <h2 className="text-4xl font-black text-gray-900">
                {loading ? '-' : equipamentos.filter(e => e.quantidade_disponivel > 0).length}
              </h2>
            </div>
            <div className="bg-emerald-50 p-3 rounded-lg">
              <Activity className="w-6 h-6 text-emerald-600" />
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-4 font-medium border-t border-gray-100 pt-3">
            Ociosos no seu pátio/estoque.
          </p>
        </div>

        {/* Novo Card - Contratos Ativos */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 flex flex-col justify-between">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-sm font-medium text-gray-500 uppercase tracking-widest mb-1">Contratos Ativos</p>
              <h2 className="text-4xl font-black text-gray-900">
                {loading ? '-' : locacoes.filter(l => l.status === 'ativo').length}
              </h2>
            </div>
            <div className="bg-orange-50 p-3 rounded-lg">
              <CheckCircle2 className="w-6 h-6 text-orange-600" />
            </div>
          </div>
          <p className="text-xs text-gray-400 mt-4 font-medium border-t border-gray-100 pt-3">
            Aluguéis em andamento.
          </p>
        </div>
      </div>

      {/* Grid Duplo para Tabelas */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
        
        {/* Tabela de Maquinas (Locações reduzidas colunas) */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center shrink-0">
            <h3 className="font-bold text-gray-800">Seu Estoque</h3>
          </div>
          
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-gray-50/50 text-gray-500 uppercase tracking-wider text-xs border-b border-gray-100">
                <tr>
                  <th className="px-6 py-4 font-medium">Equipamento</th>
                  <th className="px-6 py-4 font-medium text-center">Disp / Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {loading ? (
                  <tr>
                    <td colSpan="2" className="px-6 py-8 text-center text-gray-400">
                      Carregando inventário...
                    </td>
                  </tr>
                ) : equipamentos.length === 0 ? (
                  <tr>
                    <td colSpan="2" className="px-6 py-8 text-center text-gray-500">
                      Nenhum equipamento cadastrado ainda.
                    </td>
                  </tr>
                ) : (
                  equipamentos.map((eq) => (
                    <tr key={eq.id} className="hover:bg-gray-50/50 transition-colors">
                      <td className="px-6 py-3 font-bold text-gray-800">
                        {eq.nome}
                        <span className="block text-xs font-normal text-gray-500">{new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(eq.valor_diaria)}</span>
                      </td>
                      <td className="px-6 py-3 text-center border-l border-gray-50">
                        <span className={`font-bold ${eq.quantidade_disponivel > 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                          {eq.quantidade_disponivel}
                        </span> 
                        <span className="text-gray-400 mx-1">/</span> 
                        <span className="text-gray-600">{eq.quantidade_total}</span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Nossa Nova aba Operações Ativas */}
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
          <div className="bg-slate-50 px-6 py-4 border-b border-gray-200 flex justify-between items-center shrink-0">
            <h3 className="font-bold text-slate-800">Operações e Contratos</h3>
          </div>
          
          <div className="overflow-x-auto flex-1">
            <table className="w-full text-left text-sm whitespace-nowrap">
              <thead className="bg-slate-50/50 text-slate-500 uppercase tracking-wider text-xs border-b border-slate-100">
                <tr>
                  <th className="px-6 py-4 font-medium">Contrato</th>
                  <th className="px-6 py-4 font-medium">Status / Fim</th>
                  <th className="px-6 py-4 font-medium text-right">Ação</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {loading ? (
                  <tr>
                    <td colSpan="3" className="px-6 py-8 text-center text-slate-400">
                      Sincronizando contratos...
                    </td>
                  </tr>
                ) : locacoes.length === 0 ? (
                  <tr>
                    <td colSpan="3" className="px-6 py-8 text-center text-slate-500">
                      Sua locadora ainda não realizou aluguéis.
                    </td>
                  </tr>
                ) : (
                  locacoes.map((loc) => {
                    const isAtivo = loc.status === 'ativo';
                    return (
                      <tr key={loc.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="px-6 py-3">
                          <span className="font-bold text-slate-800 block">ID #{loc.id} - {loc.equipamento?.nome.split(' ')[0]}</span>
                          <span className="text-xs text-slate-500">Cliente {loc.cliente_id}</span>
                        </td>
                        <td className="px-6 py-3">
                           {isAtivo ? (
                             <span className="inline-block bg-amber-100 text-amber-800 text-[10px] px-2 py-0.5 rounded font-bold mb-1 border border-amber-200 uppercase tracking-widest">Ativo</span>
                           ) : (
                             <span className="inline-block bg-slate-100 text-slate-600 text-[10px] px-2 py-0.5 rounded font-bold mb-1 border border-slate-200 uppercase tracking-widest">Finalizado</span>
                           )}
                           <span className="block text-xs text-slate-500 font-medium">Até {new Date(loc.data_fim_prevista).toLocaleDateString()}</span>
                        </td>
                        <td className="px-6 py-3 text-right">
                          {isAtivo ? (
                            <button 
                              onClick={() => { setSelectedLocacao(loc); setIsModalDevolucaoOpen(true); }}
                              className="text-white bg-slate-800 hover:bg-slate-900 border border-slate-900 px-3 py-1.5 rounded-lg font-semibold text-xs shadow-sm transition-colors"
                            >
                              Devolução
                            </button>
                          ) : (
                            <span className="text-xs font-bold text-slate-300">FECHADO</span>
                          )}
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <ModalCadastroMaquina 
        isOpen={isModalMaquinaOpen} 
        onClose={() => setIsModalMaquinaOpen(false)} 
        onSuccess={fetchData} 
      />

      <ModalDevolucao 
        isOpen={isModalDevolucaoOpen} 
        onClose={() => setIsModalDevolucaoOpen(false)} 
        locacao={selectedLocacao}
        onSuccess={fetchData} 
      />
    </div>
  );
}
