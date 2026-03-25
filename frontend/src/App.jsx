import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Cadastro from './pages/Cadastro'
import CadastroMaquina from './pages/CadastroMaquina'
import Vistoria from './pages/Vistoria'
import EquipamentoDetalhes from './pages/EquipamentoDetalhes'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/add-maquina" element={<CadastroMaquina />} />
          <Route path="/terminal-vistoria" element={<Vistoria />} />
          <Route path="/equipamentos/:id" element={<EquipamentoDetalhes />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
