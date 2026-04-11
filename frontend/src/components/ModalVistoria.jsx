import React, { useState } from 'react';
import { X, UploadCloud, CheckCircle2, Factory } from 'lucide-react';
import api from '../services/api';

export default function ModalVistoria({ isOpen, onClose, locacao, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [horimetro, setHorimetro] = useState('');
  const [checklist, setChecklist] = useState('');
  const [foto, setFoto] = useState(null);

  if (!isOpen || !locacao) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!foto) {
      setError("A foto da devolução é obrigatória pelo processo do LocPlus!");
      setLoading(false);
      return;
    }

    try {
      const formData = new FormData();
      // Campos exigidos pela nova rota da Vistoria (Locador)
      formData.append('horimetro_final', parseFloat(horimetro) || 0);
      formData.append('checklist_status', checklist);
      formData.append('fotos', foto); // API suporta List[UploadFile] mas usamos apenas 1 aqui
      
      await api.post(`/vistorias/${locacao.id}/devolucao`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      alert('Estoque Recuperado! A máquina voltou para a garagem de ativos.');
      onSuccess();
      onClose();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Erro ao registrar devolução.');
    } finally {
      setLoading(false);
    }
  };

  const equipamento = locacao.equipamento || {};

  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-xl overflow-hidden flex flex-col">
        
        {/* Header Modal */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-slate-50/50">
          <div className="flex items-center">
            <Factory className="w-5 h-5 text-slate-600 mr-2" />
            <h2 className="text-xl font-bold text-gray-800">Check-in de Máquina</h2>
          </div>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto max-h-[80vh]">
          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-lg text-sm font-medium border border-red-100">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </div>
          )}

          <div className="bg-slate-100 p-4 rounded-xl border border-slate-200 mb-6 text-sm flex justify-between items-center">
            <div>
              <p className="text-slate-500 font-medium">Equipamento a Devolver</p>
              <h3 className="font-bold text-slate-800 text-lg">{equipamento.nome || `Equipamento ID #${locacao.equipamento_id}`}</h3>
            </div>
            <div className="bg-white px-3 py-1.5 rounded border border-slate-200 text-slate-700 font-bold">
               Contrato #{locacao.id}
            </div>
          </div>

          <form id="devolucao-form" onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Horímetro / KM Final *</label>
              <input
                type="number"
                step="0.1"
                required
                value={horimetro}
                onChange={(e) => setHorimetro(e.target.value)}
                placeholder="Ex: 12500"
                className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-slate-500/50 focus:border-slate-500"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Condição de Recebimento (Parecer) *</label>
              <textarea
                required
                rows="3"
                value={checklist}
                onChange={(e) => setChecklist(e.target.value)}
                placeholder="Máquina retornou íntegra. Arranhões no braço hidráulico..."
                className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-slate-500/50 focus:border-slate-500 resize-none"
              ></textarea>
            </div>

            <div className="mt-2 text-center bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
              <label className="block text-sm font-bold text-yellow-800 mb-2">Comprovação Visual Obrigatória</label>
              <label 
                htmlFor="file-devolucao" 
                className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-yellow-300 rounded-xl bg-white hover:bg-yellow-100 hover:border-yellow-400 cursor-pointer transition-colors"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <UploadCloud className={`w-8 h-8 mb-2 ${foto ? 'text-blue-500' : 'text-yellow-600'}`} />
                  {foto ? (
                    <p className="text-sm text-blue-600 font-medium">{foto.name}</p>
                  ) : (
                    <p className="text-sm text-yellow-700"><span className="font-semibold underline">Anexe a foto</span> da situação da devolutiva</p>
                  )}
                </div>
                <input 
                  id="file-devolucao" 
                  type="file" 
                  accept="image/png, image/jpeg, image/jpg" 
                  className="hidden" 
                  onChange={(e) => setFoto(e.target.files[0])}
                />
              </label>
            </div>

          </form>
        </div>

        {/* Footer actions */}
        <div className="px-6 py-4 border-t border-gray-100 flex justify-end gap-3 bg-slate-50/50">
          <button 
            type="button" 
            onClick={onClose}
            className="px-5 py-2.5 text-sm font-medium text-gray-600 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            form="devolucao-form"
            disabled={loading}
            className="px-6 py-2.5 text-sm font-bold text-white bg-slate-800 hover:bg-slate-900 rounded-lg shadow-sm flex items-center transition-colors disabled:opacity-50"
          >
            {loading ? 'Subindo evidência...' : 'Efetivar Devolução'}
            {!loading && <CheckCircle2 className="w-4 h-4 ml-2 text-emerald-400" />}
          </button>
        </div>

      </div>
    </div>
  );
}
