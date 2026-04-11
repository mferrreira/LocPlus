import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Login from './pages/Login'
import Cadastro from './pages/Cadastro'
import Catalogo from './pages/Catalogo'
import Dashboard from './pages/Dashboard'
import MinhasLocacoes from './pages/MinhasLocacoes'
import { PrivateRoute } from './components/PrivateRoute'

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1 container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />
          <Route path="/catalogo" element={<Catalogo />} />
          <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
          <Route path="/minhas-locacoes" element={<PrivateRoute><MinhasLocacoes /></PrivateRoute>} />
        </Routes>
      </main>
    </div>
  )
}

export default App
