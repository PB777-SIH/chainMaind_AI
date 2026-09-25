import { Link, useLocation } from 'react-router-dom'
import { CircuitBoard } from 'lucide-react'
import './NavBar.css'

export default function NavBar() {
  const { pathname } = useLocation()
  return (
    <header className="navbar">
      <Link to="/" className="navbar-brand">
        <CircuitBoard size={18} />
        <span>CHAINMIND</span>
        <span className="navbar-brand-sub mono">AI</span>
      </Link>
      <nav className="navbar-links">
        <Link to="/" className={pathname === '/' ? 'active' : ''}>
          Overview
        </Link>
        <Link to="/analyst" className={pathname === '/analyst' ? 'active' : ''}>
          Analyst Mode
        </Link>
      </nav>
    </header>
  )
}
