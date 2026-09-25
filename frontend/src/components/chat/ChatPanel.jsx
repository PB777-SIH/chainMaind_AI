import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Sparkles } from 'lucide-react'
import { postChat } from '../../lib/api'
import './ChatPanel.css'

const SUGGESTIONS = [
  'Why is TSMC critical right now?',
  'What if the Taiwan Strait closes for 48 hours?',
  'What is driving the neon scarcity index?',
  "What's the total fused risk score?",
]

function TypedText({ text }) {
  const [shown, setShown] = useState('')
  useEffect(() => {
    setShown('')
    let i = 0
    const step = Math.max(1, Math.round(text.length / 90))
    const id = setInterval(() => {
      i += step
      setShown(text.slice(0, i))
      if (i >= text.length) clearInterval(id)
    }, 14)
    return () => clearInterval(id)
  }, [text])
  return <p className="chat-bubble-text">{shown}</p>
}

export default function ChatPanel({ getContext, onAssistantReply }) {
  const [messages, setMessages] = useState([
    { role: 'assistant', text: "I'm watching the fused risk graph live. Ask me about a facility, a material, or run a reroute scenario — I'll point to the evidence on the globe as I answer.", cited_sources: [] },
  ])
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)
  const listRef = useRef(null)

  useEffect(() => {
    if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight
  }, [messages, thinking])

  async function send(text) {
    const q = (text ?? input).trim()
    if (!q || thinking) return
    setMessages((m) => [...m, { role: 'user', text: q }])
    setInput('')
    setThinking(true)
    try {
      const context = getContext ? getContext() : {}
      const result = await postChat(q, context)
      setMessages((m) => [...m, { role: 'assistant', text: result.response, cited_sources: result.cited_sources || [] }])
      onAssistantReply && onAssistantReply(result)
    } catch (err) {
      setMessages((m) => [...m, { role: 'assistant', text: `Couldn't reach the analyst backend (${err.message}).`, cited_sources: [] }])
    } finally {
      setThinking(false)
    }
  }

  return (
    <div className="chat-panel">
      <div className="chat-header">
        <Sparkles size={15} /><span>Analyst Assistant</span>
        <span className="chat-header-tag mono">processor.py + Groq</span>
      </div>
      <div className="chat-list" ref={listRef}>
        {messages.map((m, i) => (
          <div key={i} className={`chat-row ${m.role}`}>
            <div className="chat-bubble">
              {m.role === 'assistant' ? <TypedText text={m.text} /> : <p className="chat-bubble-text">{m.text}</p>}
              {m.cited_sources?.length > 0 && (
                <div className="chat-sources">
                  {m.cited_sources.map((s, j) => <span key={j} className="mono chat-source-chip">{s}</span>)}
                </div>
              )}
            </div>
          </div>
        ))}
        <AnimatePresence>
          {thinking && (
            <motion.div className="chat-row assistant" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="chat-bubble thinking"><span className="dot" /><span className="dot" /><span className="dot" /></div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
      {messages.length < 2 && (
        <div className="chat-suggestions">
          {SUGGESTIONS.map((s) => <button key={s} onClick={() => send(s)}>{s}</button>)}
        </div>
      )}
      <form className="chat-input-row" onSubmit={(e) => { e.preventDefault(); send() }}>
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask about a node, a material, or a scenario..." />
        <button type="submit" aria-label="Send"><Send size={16} /></button>
      </form>
    </div>
  )
}