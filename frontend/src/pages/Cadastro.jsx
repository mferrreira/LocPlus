import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Building2, User, ChevronRight, CheckCircle2 } from 'lucide-react';
import api from '../services/api';

export default function Cadastro() {
  const navigate = useNavigate();
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Passo 1: Objetivo da Conta
  const [objetivo, setObjetivo] = useState('disponibilizar_maquinas');
  
  // Passo 2: Tipo de Entidade (Por padrão B2B PJ)
  const [tipoEntidade, setTipoEntidade] = useState('pessoa_juridica');

  // Dados do Formulário Final
  const [formData, setFormData] = useState({
    nome_completo: '',
    email: '',
    senha: '',
    documento: '', // CNPJ ou CPF
    telefone_celular: '',
    // Específicos PJ
    razao_social: '',
    nome_fantasia: '',
    inscricao_estadual: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleCadastrar = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Prepara o payload nos moldes do Pydantic Backend
    const payload = {
      email: formData.email,
      objetivo: objetivo,
      tipo_entidade: tipoEntidade,
      nome_completo: formData.nome_completo,
      documento: formData.documento.replace(/\D/g, ''),
      telefone_celular: formData.telefone_celular.replace(/\D/g, ''),
      senha: formData.senha,
      viu_guia_cadastro: true,
      
      // Enviamos apenas se for PJ
      ...(tipoEntidade === 'pessoa_juridica' && {
        razao_social: formData.razao_social,
        nome_fantasia: formData.nome_fantasia,
        inscricao_estadual: formData.inscricao_estadual.replace(/\D/g, '')
      })
    };

    try {
      const response = await api.post('/usuarios/cadastro', payload);
      // Sucesso! Vamos acionar o Log-in forçado na próxima tela conforme sua designação
      if (response.status === 201) {
        navigate('/login', { state: { message: 'Conta criada com sucesso! Avaliação de plano Freemium concluída, faça login' }});
      }
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Erro desconhecido. Verifique os campos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-gray-900 border border-gray-800 rounded-xl shadow-2xl p-8">
        
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-white">Criar Nova Conta</h1>
          <div className="flex items-center gap-2 mt-4 text-sm font-medium">
             <span className={step >= 1 ? 'text-emerald-500' : 'text-gray-500'}>1. Setup de Perfil</span>
             <ChevronRight className="w-4 h-4 text-gray-700" />
             <span className={step >= 2 ? 'text-emerald-500' : 'text-gray-500'}>2. Informações B2B</span>
          </div>
        </div>

        {error && (
          <div className="bg-red-500/10 border border-red-500/20 text-red-500 p-3 rounded-lg mb-6 text-sm">
            {typeof error === 'string' ? error : JSON.stringify(error)}
          </div>
        )}

        {/* STEP 1 */}
        {step === 1 && (
          <div className="space-y-6">
            <h2 className="text-lg text-gray-300 font-medium">Qual é o seu objetivo na LocPlus?</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => setObjetivo('disponibilizar_maquinas')}
                className={`p-6 border rounded-xl text-left transition-all ${
                  objetivo === 'disponibilizar_maquinas' 
                  ? 'border-emerald-500 bg-emerald-500/10' 
                  : 'border-gray-800 hover:border-gray-700'
                }`}
              >
                <Building2 className={`w-8 h-8 mb-4 ${objetivo === 'disponibilizar_maquinas' ? 'text-emerald-500' : 'text-gray-500'}`} />
                <h3 className="text-white font-medium text-lg">Sou Locador</h3>
                <p className="text-gray-400 text-sm mt-1">Quero oferecer minha frota no catálogo, gerenciar contratos e monitorar vistorias.</p>
              </button>

              <button
                type="button"
                onClick={() => setObjetivo('alugar_maquinas')}
                className={`p-6 border rounded-xl text-left transition-all ${
                  objetivo === 'alugar_maquinas' 
                  ? 'border-blue-500 bg-blue-500/10' 
                  : 'border-gray-800 hover:border-gray-700'
                }`}
              >
                <User className={`w-8 h-8 mb-4 ${objetivo === 'alugar_maquinas' ? 'text-blue-500' : 'text-gray-500'}`} />
                <h3 className="text-white font-medium text-lg">Sou Locatário</h3>
                <p className="text-gray-400 text-sm mt-1">Quero buscar máquinas para a minha obra e assinar vistorias digitais.</p>
              </button>
            </div>

            <div className="flex justify-end pt-6 mt-6 border-t border-gray-800">
              <button 
                onClick={() => setStep(2)}
                className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 px-8 rounded-lg flex items-center gap-2"
              >
                Continuar Setup <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          </div>
        )}

        {/* STEP 2 */}
        {step === 2 && (
          <form onSubmit={handleCadastrar} className="space-y-4">
            <h2 className="text-lg text-gray-300 font-medium mb-6">Informações Essenciais</h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Nome Completo do Responsável</label>
                <input
                  type="text"
                  name="nome_completo"
                  required
                  value={formData.nome_completo}
                  onChange={handleChange}
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Email de Acesso</label>
                <input
                  type="email"
                  name="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Senha Segura</label>
                <input
                  type="password"
                  name="senha"
                  required
                  value={formData.senha}
                  onChange={handleChange}
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Celular / WhatsApp</label>
                <input
                  type="text"
                  name="telefone_celular"
                  required
                  value={formData.telefone_celular}
                  onChange={handleChange}
                  className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>

            {/* ESPECÍFICO DE LOCADORA B2B */}
            {objetivo === 'disponibilizar_maquinas' && (
              <div className="mt-6 pt-6 border-t border-gray-800 space-y-4">
                <h3 className="text-white font-medium">Dados da Empresa Locadora</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="md:col-span-2">
                    <label className="block text-sm text-gray-400 mb-1">Nome Fantasia (Como você aparecerá na vitrine)</label>
                    <input
                      type="text"
                      name="nome_fantasia"
                      required={tipoEntidade === 'pessoa_juridica'}
                      value={formData.nome_fantasia}
                      onChange={handleChange}
                      className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">Razão Social</label>
                    <input
                      type="text"
                      name="razao_social"
                      required={tipoEntidade === 'pessoa_juridica'}
                      value={formData.razao_social}
                      onChange={handleChange}
                      className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm text-gray-400 mb-1">CNPJ</label>
                    <input
                      type="text"
                      name="documento"
                      required
                      value={formData.documento}
                      onChange={handleChange}
                      className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                  <div className="md:col-span-2">
                    <label className="block text-sm text-gray-400 mb-1">Inscrição Estadual</label>
                    <input
                      type="text"
                      name="inscricao_estadual"
                      required={tipoEntidade === 'pessoa_juridica'}
                      value={formData.inscricao_estadual}
                      onChange={handleChange}
                      className="w-full bg-gray-950 border border-gray-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-500"
                    />
                  </div>
                </div>
              </div>
            )}

            <div className="flex justify-between pt-6 mt-6 border-t border-gray-800">
              <button 
                type="button"
                onClick={() => setStep(1)}
                className="text-gray-400 hover:text-white px-4 py-2 font-medium transition-colors"
              >
                Voltar
              </button>
              
              <button 
                type="submit"
                disabled={loading}
                className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-3 px-8 rounded-lg flex items-center gap-2 transition-colors disabled:opacity-50"
              >
                {loading ? 'Processando Autenticação...' : 'Finalizar Cadastro'}
                {!loading && <CheckCircle2 className="w-5 h-5" />}
              </button>
            </div>
          </form>
        )}

      </div>

      <div className="mt-8 text-center">
        <p className="text-gray-400 text-sm">
          Já possui conta?{' '}
          <Link to="/login" className="text-emerald-500 hover:text-emerald-400 font-medium">
            Entrar no Painel
          </Link>
        </p>
      </div>

    </div>
  );
}
