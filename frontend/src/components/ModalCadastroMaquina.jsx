import React, { useState } from 'react';
import { X, UploadCloud, CheckCircle2 } from 'lucide-react';
import api from '../services/api';

export default function ModalCadastroMaquina({ isOpen, onClose, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    nome: '',
    descricao: '',
    categoria: 'linha_pesada',
    valor_diaria: '',
    quantidade_total: 1,
  });
  
  const [foto, setFoto] = useState(null);

  if (!isOpen) return null;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // O FastAPI no backend (/equipamentos/) espera um Payload JSON (Pydantic Model)
      const equipamentoBody = {
        nome: formData.nome,
        descricao: formData.descricao,
        categoria: formData.categoria,
        valor_diaria: parseFloat(formData.valor_diaria),
        quantidade_total: parseInt(formData.quantidade_total),
        empresa_id: 0 // Ignorado pelo backend (substituído pelo current_tenant.id do JWT)
      };

      // PASSO 1: Cria o equipamento
      const responseEq = await api.post('/equipamentos/', equipamentoBody);
      const equipamentoId = responseEq.data.id;

      // PASSO 2: Se foi enviado foto, faz o upload na rota específica
      if (foto) {
        const fotoData = new FormData();
        fotoData.append('file', foto);
        
        await api.post(`/equipamentos/${equipamentoId}/fotos?tipo_foto=visao_geral`, fotoData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }

      onSuccess();
      onClose();
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || 'Ocorreu um erro ao cadastrar a máquina.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[90vh]">
        
        {/* Header Modal */}
        <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50/50">
          <h2 className="text-xl font-bold text-gray-800">Anunciar Novo Equipamento</h2>
          <button onClick={onClose} className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto">
          {error && (
            <div className="mb-6 p-4 bg-red-50 text-red-600 rounded-lg text-sm font-medium border border-red-100">
              {typeof error === 'string' ? error : JSON.stringify(error)}
            </div>
          )}

          <form id="cadastro-maquina-form" onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Nome da Máquina *</label>
              <input
                type="text"
                name="nome"
                required
                placeholder="Ex: Escavadeira Hidráulica CAT 320"
                value={formData.nome}
                onChange={handleChange}
                className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-1">Descrição</label>
              <textarea
                name="descricao"
                rows="3"
                placeholder="Detalhes técnicos, potência, peso operacional..."
                value={formData.descricao}
                onChange={handleChange}
                className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors resize-none"
              ></textarea>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Categoria *</label>
                <select
                  name="categoria"
                  required
                  value={formData.categoria}
                  onChange={handleChange}
                  className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors cursor-pointer"
                >
                  <option value="linha_pesada">Linha Pesada (Tratores/Guindastes)</option>
                  <option value="linha_leve">Linha Leve (Betoneiras/Andaimes)</option>
                  <option value="veiculos">Apoio Logístico (Caminhões)</option>
                  <option value="mensalistas">Infraestrutura Fixa</option>
                  <option value="diversos">Ferramentas Menores</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Quantidade em Estoque *</label>
                <input
                  type="number"
                  name="quantidade_total"
                  min="1"
                  required
                  value={formData.quantidade_total}
                  onChange={handleChange}
                  className="w-full bg-white border border-gray-300 rounded-lg px-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-sm font-semibold text-gray-700 mb-1">Valor da Diária (R$) *</label>
                <div className="relative">
                  <span className="absolute left-4 top-2.5 text-gray-500 font-medium">R$</span>
                  <input
                    type="number"
                    name="valor_diaria"
                    step="0.01"
                    min="1"
                    required
                    placeholder="0.00"
                    value={formData.valor_diaria}
                    onChange={handleChange}
                    className="w-full bg-white border border-gray-300 rounded-lg pl-10 pr-4 py-2.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-colors"
                  />
                </div>
              </div>
            </div>

            {/* UPload de Foto */}
            <div className="mt-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">Foto da Máquina (Opcional, porém recomendado)</label>
              <label 
                htmlFor="file-upload" 
                className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-xl bg-gray-50 hover:bg-blue-50 hover:border-blue-400 cursor-pointer transition-colors"
              >
                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                  <UploadCloud className={`w-8 h-8 mb-2 ${foto ? 'text-blue-500' : 'text-gray-400'}`} />
                  {foto ? (
                    <p className="text-sm text-blue-600 font-medium">{foto.name}</p>
                  ) : (
                    <p className="text-sm text-gray-500"><span className="font-semibold text-blue-600">Clique para anexar</span> ou arraste e solte</p>
                  )}
                </div>
                <input 
                  id="file-upload" 
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
        <div className="px-6 py-4 border-t border-gray-100 flex justify-end gap-3 bg-gray-50/50">
          <button 
            type="button" 
            onClick={onClose}
            className="px-5 py-2.5 text-sm font-medium text-gray-600 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            form="cadastro-maquina-form"
            disabled={loading}
            className="px-6 py-2.5 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm flex items-center transition-colors disabled:opacity-50"
          >
            {loading ? 'Salvando no MinIO...' : 'Publicar Anúncio'}
            {!loading && <CheckCircle2 className="w-4 h-4 ml-2" />}
          </button>
        </div>

      </div>
    </div>
  );
}
