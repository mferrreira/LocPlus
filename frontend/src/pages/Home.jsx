import { useState, useEffect } from 'react'
import api from '../services/api'
import EquipamentoCard from '../components/EquipamentoCard'
import { Search, Filter } from 'lucide-react'

export default function Home() {
  const [equipamentos, setEquipamentos] = useState([])
  const [loading, setLoading] = useState(true)
  const [busca, setBusca] = useState('')
  const [categoria, setCategoria] = useState('')

  const fetchEquipamentos = async () => {
    setLoading(true)
    try {
      const params = {}
      if (busca) params.busca = busca
      if (categoria) params.categoria = categoria
      
      const res = await api.get('/equipamentos', { params })
      setEquipamentos(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Effect estrito (Sem re-renders acidentais, dependência clara na Categoria)
  useEffect(() => {
    fetchEquipamentos()
  }, [categoria]) 

  const handleSearch = (e) => {
    e.preventDefault()
    fetchEquipamentos()
  }

  return (
    <div>
      {/* Hero Header de Busca */}
      <div className="mb-10 bg-gradient-to-r from-blue-700 to-blue-500 rounded-3xl p-10 text-white shadow-xl">
        <h1 className="text-4xl font-extrabold mb-4">Encontre a máquina certa, agora.</h1>
        <p className="text-blue-100 mb-8 text-xl max-w-2xl">Do canteiro de obras ao agronegócio. Alugue equipamentos pesados ou ferramentas diretos com seus donos.</p>
        
        <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-0 bg-white p-2 rounded-xl shadow-lg border">
          <div className="flex-1 flex items-center px-4 py-2 border-b md:border-b-0">
            <Search className="text-gray-400 w-6 h-6 mr-3" />
            <input 
              type="text" 
              placeholder="Busque por Retroescavadeira, Furadeira, Trator..." 
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              className="w-full text-gray-900 text-lg outline-none bg-transparent placeholder-gray-400"
            />
          </div>
          <div className="md:w-72 md:border-l pl-4 flex items-center py-2">
            <Filter className="text-gray-400 w-5 h-5 mr-3" />
            <select 
              value={categoria} 
              onChange={(e) => setCategoria(e.target.value)} 
              className="w-full text-gray-900 outline-none bg-transparent cursor-pointer font-medium appearance-none"
            >
              <option value="">Todas as Categorias</option>
              <option value="linha_pesada">Linha Pesada (Trat. / Linha Amarela)</option>
              <option value="linha_leve">Linha Leve (Beton. / Andaimes)</option>
              <option value="veiculos">Apoio Logístico (Veículos/Caminhões)</option>
              <option value="mensalistas">Fixas (Containers, Cabines)</option>
              <option value="diversos">Ferramentas & Diversos</option>
            </select>
          </div>
          <button type="submit" className="ml-2 bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 px-10 rounded-lg transition-colors h-full">
            Pesquisar
          </button>
        </form>
      </div>

      {/* Área de Listagem de Cards */}
      {loading ? (
        <div className="flex flex-col items-center justify-center my-32">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-600 mb-4"></div>
          <p className="text-gray-500 font-medium">Sincronizando com as garagens...</p>
        </div>
      ) : equipamentos.length === 0 ? (
        <div className="flex flex-col items-center justify-center my-20 bg-gray-50 py-16 rounded-2xl border-2 border-dashed border-gray-200">
          <p className="text-gray-500 text-lg font-medium">Nenhum equipamento logado nesta região com estes filtros.</p>
          <button onClick={() => {setBusca(''); setCategoria('');}} className="mt-4 text-blue-600 font-bold hover:underline">Limpar filtros</button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
          {equipamentos.map(eq => (
            <EquipamentoCard key={eq.id} equipamento={eq} />
          ))}
        </div>
      )}
    </div>
  )
}
