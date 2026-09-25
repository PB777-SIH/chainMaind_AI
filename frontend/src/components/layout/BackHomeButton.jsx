// src/components/layout/BackHomeButton.jsx
import { Link } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import './BackHomeButton.css'

export default function BackHomeButton() {
  return (
    <Link to="/" className="back-home-fab" aria-label="Back to overview">
      <ArrowLeft size={18} />
    </Link>
  )
}