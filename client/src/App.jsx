import { useState, useEffect } from 'react'
import LandingPage from './components/LandingPage'
import Particles from './components/Particles'
import AnimatedList from './components/AnimatedList'
import TargetCursor from './components/TargetCursor'
import StarBorder from './components/StarBorder'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const EXAMPLE_CIRCUITS = [
  "Design a low-pass RC filter with 1kHz cutoff frequency",
  "Design a high-pass RC filter with 100Hz cutoff frequency",
  "Create a voltage divider that converts 9V input to 5V output",
  "Design a low-pass RC filter with 500 Hz cutoff",
  "Design a voltage divider from 12V to 3.3V"
]

function App() {
  const [showLanding, setShowLanding] = useState(true)
  const [prompt, setPrompt] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [backendStatus, setBackendStatus] = useState('checking')

  // Check backend health on mount
  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then(res => res.json())
      .then(() => setBackendStatus('online'))
      .catch(() => setBackendStatus('offline'))
  }, [])

  if (showLanding) {
    return (
      <>
        <TargetCursor />
        <LandingPage onGetStarted={() => setShowLanding(false)} />
      </>
    )
  }

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a circuit description')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description: prompt.trim() }),
      })

      const data = await response.json()

      if (data.success) {
        setResult(data)
        setError(null)
      } else {
        setError(data.error || 'Failed to generate circuit')
      }
    } catch (err) {
      console.error('API Error:', err)
      if (err.name === 'TypeError' && err.message.includes('fetch')) {
        setError('Cannot connect to backend API. Make sure it is running on port 5000.')
      } else {
        setError(`Error: ${err.message}`)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!result) return

    try {
      const response = await fetch(`${API_URL}${result.download_url}`)
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = result.filename
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError('Failed to download file')
    }
  }

  const formatExplanation = (explanation) => {
    if (!explanation) return null

    const parts = explanation.split('Calculations:')
    if (parts.length === 1) {
      return <p className="explanation-text">{explanation}</p>
    }

    const [description, calculationsPart] = parts
    const calcParts = calculationsPart.split('\n\n')
    const calculations = calcParts[0]
    const remaining = calcParts.slice(1).join('\n\n')

    return (
      <>
        <p className="explanation-text">{description.trim()}</p>
        <div className="calculations-section">
          <h3>Calculations:</h3>
          <pre className="calculations-code">{calculations.trim()}</pre>
        </div>
        {remaining && <p className="explanation-text">{remaining.trim()}</p>}
      </>
    )
  }

  return (
    <div className="app">
      <TargetCursor />
      <Particles
        particleColors={['#667eea', '#764ba2', '#ffffff']}
        particleCount={300}
        particleSpread={15}
        speed={0.15}
        particleBaseSize={150}
        moveParticlesOnHover={true}
        alphaParticles={false}
        disableRotation={false}
      />
      <header className="header">
        <h1>⚡ AutoCDA</h1>
        <p className="subtitle">AI-Powered Circuit Design Assistant</p>
        {backendStatus === 'online' && (
          <div style={{ marginTop: '0.5rem', color: '#4caf50', fontSize: '0.9rem' }}>
            ● Backend Connected
          </div>
        )}
        {backendStatus === 'offline' && (
          <div style={{ marginTop: '0.5rem', color: '#f44336', fontSize: '0.9rem' }}>
            ● Backend Offline - Start with: python backend/api.py
          </div>
        )}
      </header>

      <main className="main-content">
        <div className="input-section">
          <h2>Describe Your Circuit</h2>
          
          <div className="examples">
            <label>Quick Examples:</label>
            <AnimatedList
              items={EXAMPLE_CIRCUITS}
              onItemSelect={(item) => setPrompt(item)}
              showGradients={true}
              enableArrowNavigation={true}
              displayScrollbar={true}
            />
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem', color: 'rgba(255, 255, 255, 0.8)', fontWeight: 500 }}>
              Or describe your own circuit:
            </label>
            <textarea
              className="prompt-input"
              placeholder="e.g., Design a low-pass RC filter with 1kHz cutoff frequency"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
            />
          </div>

          <StarBorder
            as="button"
            className="generate-btn"
            color="#667eea"
            speed="5s"
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
          >
            {loading ? '⏳ Generating...' : '🚀 Generate Circuit'}
          </StarBorder>
        </div>

        {error && (
          <div className="error-box">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className="result-section">
            <div className="success-box">
              <h3>✅ Circuit Generated Successfully!</h3>
            </div>

            <div className="explanation-box">
              <h2>📋 Design Explanation</h2>
              {formatExplanation(result.explanation)}
            </div>

            <div className="download-box">
              <h2>📥 Download KiCad Project</h2>
              <button className="download-btn" onClick={handleDownload}>
                📦 Download KiCad Project (ZIP)
              </button>
              <div className="instructions">
                <h3>📖 How to open in KiCad:</h3>
                <ol>
                  <li>Extract the ZIP file</li>
                  <li>Open KiCad</li>
                  <li>File → Open Project</li>
                  <li>Select the .kicad_pro file</li>
                  <li>Open the schematic (.kicad_sch file)</li>
                </ol>
              </div>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by Claude 3.5 Sonnet • SKiDL • KiCad</p>
      </footer>
    </div>
  )
}

export default App
