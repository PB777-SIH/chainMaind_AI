import { Routes, Route } from 'react-router-dom'
import NavBar from './components/layout/NavBar'
import Landing from './pages/Landing'
import AnalystMode from './pages/AnalystMode'

export default function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/analyst" element={<AnalystMode />} />
      </Routes>
    </>
  )
}
