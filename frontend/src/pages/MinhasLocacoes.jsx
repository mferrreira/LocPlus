import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { FileText, CalendarCheck, PackageX } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function MinhasLocacoes() {
  const [locacoes, setLocacoes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState('');

  const fetchLocacoes = async () => {
    try {
      const response = await api.get('/locacoes/meus');
      setLocacoes(response.data);
    } catch (err) {
      setErro('Você ainda não realizou ou não tem acesso ao painel de locatário cruzado.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocacoes();
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Meus Equipamentos Alugados</h1>
        <p className="text-gray-500 mt-1 text-lg">Acompanhe suas reservas e diárias.</p>
      </div>

      {erro && (
        <div className="bg-red-50 text-red-600 p-4 rounded-lg font-medium border border-red-100">
          {erro}
        </div>
      )}

      <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden mt-8">
        <div className="bg-indigo-50/50 px-6 py-4 border-b border-gray-100 flex items-center">
          <FileText className="w-5 h-5 text-indigo-600 mr-2" />
          <h3 className="font-bold text-indigo-900">Histórico de Contratos</h3>
        </div>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm whitespace-nowrap">
            <thead className="bg-gray-50 text-gray-500 uppercase tracking-wider text-xs border-b border-gray-200">
              <tr>
                <th className="px-6 py-4 font-bold">Máquina Arrendada</th>
                <th className="px-6 py-4 font-bold">Período Previsto</th>
                <th className="px-6 py-4 font-bold text-center">Status</th>
                <th className="px-6 py-4 font-bold text-right">Ticket Médio</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {loading ? (
                <tr>
                  <td colSpan="4" className="px-6 py-12 text-center text-gray-400">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-indigo-600 mb-2"></div>
                    <p>Buscando registros...</p>
                  </td>
                </tr>
              ) : locacoes.length === 0 ? (
                <tr>
                  <td colSpan="4" className="px-6 py-12 text-center text-gray-500">
                    <PackageX className="w-10 h-10 mx-auto text-gray-300 mb-2" />
                    Você ainda não alugou nenhuma máquina do nosso Hub.
                    <br />
                    <Link to="/catalogo" className="text-indigo-600 font-bold mt-2 inline-block">Ir para a Vitrine Livre</Link>
                  </td>
                </tr>
              ) : (
                locacoes.map((loc) => {
                  const valorTotalEstimado = (loc.equipamento?.valor_diaria || 0); // No backend real isso deve vir pre-calculado, mock simples UI
                  // Calculo rápido frontend (ideal seria a API devolver o montante)
                  const diffTime = Math.abs(new Date(loc.data_fim_prevista) - new Date(loc.data_inicio || Date.now()));
                  const dias = Math.max(1, Math.ceil(diffTime / (1000 * 60 * 60 * 24)));
                  const vFinanceiro = dias * (loc.equipamento?.valor_diaria || 0);

                  return (
                    <tr key={loc.id} className="hover:bg-gray-50/50 transition-colors">
                      <td className="px-6 py-4">
                        <span className="font-bold text-gray-900 block">{loc.equipamento?.nome || `Equipamento #${loc.equipamento_id}`}</span>
                        <span className="text-xs text-gray-400">{loc.equipamento?.empresa?.nome_fantasia || ''}</span>
                      </td>
                      <td className="px-6 py-4 text-gray-600 flex items-center">
                        <CalendarCheck className="w-4 h-4 mr-2 text-indigo-400" />
                        {new Date(loc.data_inicio || Date.now()).toLocaleDateString()} a {new Date(loc.data_fim_prevista).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 text-center">
                        {loc.status === 'ativo' ? (
                          <span className="bg-emerald-100 text-emerald-800 text-xs px-3 py-1.5 rounded-full font-bold border border-emerald-200">
                            ATIVO
                          </span>
                        ) : (
                          <span className="bg-gray-100 text-gray-600 text-xs px-3 py-1.5 rounded-full font-bold border border-gray-200">
                            FINALIZADO
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 text-right font-bold text-gray-900 border-l border-gray-50">
                        {new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(vFinanceiro)}
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
