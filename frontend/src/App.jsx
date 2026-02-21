import { useEffect, useRef, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [isUploading, setIsUploading] = useState(false)
  const [documentInfo, setDocumentInfo] = useState(null)
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [citations, setCitations] = useState([])
  const [tableRows, setTableRows] = useState([])
  const [error, setError] = useState('')

  const pdfViewerRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files?.[0]
    setSelectedFile(file ?? null)
    setDocumentInfo(null)
    setAnswer('')
    setCitations([])
    setTableRows([])
    setError('')
  }

  const handleUpload = async () => {
    if (!selectedFile) return
    setIsUploading(true)
    setError('')
    try {
      const formData = new FormData()
      formData.append('file', selectedFile)
      const res = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || 'Upload failed')
      }
      const data = await res.json()
      setDocumentInfo(data.document)
    } catch (e) {
      setError(e.message || 'Unexpected error during upload')
    } finally {
      setIsUploading(false)
    }
  }

  const handleAsk = async () => {
    if (!question.trim()) return
    setError('')
    setAnswer('')
    setCitations([])
    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || 'Query failed')
      }
      const data = await res.json()
      setAnswer(data.answer)
      setCitations(data.citations || [])
    } catch (e) {
      setError(e.message || 'Unexpected error during query')
    }
  }

  const handleAskTable = async () => {
    if (!question.trim()) return
    setError('')
    setTableRows([])
    try {
      const res = await fetch(`${API_BASE}/query/table`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || 'Table query failed')
      }
      const data = await res.json()
      setTableRows(data.rows || [])
    } catch (e) {
      setError(e.message || 'Unexpected error during table query')
    }
  }

  const handleCitationClick = (citation) => {
    if (!documentInfo || !pdfViewerRef.current) return
    const iframe = pdfViewerRef.current
    // Simple behavior: open the page via URL fragment when supported
    // Fallback: just focus the iframe
    iframe.focus()
  }

  useEffect(() => {
    setAnswer('')
    setCitations([])
  }, [documentInfo?.id])

  const pdfUrl = documentInfo
    ? `${API_BASE.replace('8000', '8000')}/static/${documentInfo.name}`
    : null

  return (
    <div className="app-root">
      <div className="glass-shell">
        <header className="app-header">
          <div className="branding">
            <div className="orb" />
            <div>
              <h1>SmartDoc AI</h1>
              <p className="subtitle">Next‑gen document intelligence for SFCR reports</p>
            </div>
          </div>
          <div className="tag">alpha</div>
        </header>

        <main className="layout">
          <section className="left-pane">
            <div className="panel upload-panel">
              <h2>Upload PDF</h2>
              <p className="hint">Drop a SFCR PDF and let SmartDoc index it.</p>
              <div className="upload-zone">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={handleFileChange}
                />
                <button
                  className="primary"
                  disabled={!selectedFile || isUploading}
                  onClick={handleUpload}
                >
                  {isUploading ? 'Uploading…' : 'Process document'}
                </button>
              </div>
              {documentInfo && (
                <div className="doc-meta">
                  <div className="pill">Loaded</div>
                  <span>{documentInfo.name}</span>
                  <span>• {documentInfo.pages} pages</span>
                </div>
              )}
            </div>

            <div className="panel chat-panel">
              <h2>Ask your document</h2>
              <div className="chat-input">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask about solvency ratios, own funds, risk profile, etc."
                />
                <div className="chat-actions">
                  <button className="primary" onClick={handleAsk} disabled={!question.trim()}>
                    Ask
                  </button>
                  <button className="secondary" onClick={handleAskTable} disabled={!question.trim()}>
                    Ask as table
                  </button>
                </div>
              </div>

              {error && <div className="error-banner">{error}</div>}

              {answer && (
                <div className="answer-block">
                  <h3>AI answer</h3>
                  <p>{answer}</p>
                </div>
              )}

              {citations.length > 0 && (
                <div className="citations">
                  <h3>Citations</h3>
                  <div className="citation-chips">
                    {citations.map((c, idx) => (
                      <button
                        key={c.chunk_id || idx}
                        className="chip"
                        onClick={() => handleCitationClick(c)}
                      >
                        p.{c.page}: {c.text.slice(0, 60)}…
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {tableRows.length > 0 && (
                <div className="citations">
                  <h3>Table</h3>
                  <div className="table-preview">
                    <pre>{JSON.stringify(tableRows.slice(0, 5), null, 2)}</pre>
                  </div>
                </div>
              )}
            </div>
          </section>

          <section className="right-pane">
            <div className="panel viewer-panel">
              <h2>PDF viewer</h2>
              {documentInfo ? (
                <iframe
                  ref={pdfViewerRef}
                  title="PDF"
                  src={pdfUrl}
                  className="pdf-frame"
                />
              ) : (
                <div className="viewer-placeholder">
                  <p>Upload a document to preview and navigate citations.</p>
                </div>
              )}
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
