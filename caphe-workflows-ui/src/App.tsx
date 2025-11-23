import { useState } from 'react'
import capheLogo from './assets/caphe-logo.png'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <a href="https://caphetechnologies.com" target="_blank">
          <img src={capheLogo} className="logo caphe" alt="Caphè Technologies logo" />
        </a>
      </div>
      <h1>☕ Caphè Technologies Workflows</h1>
      <p className="tagline">Healthcare Workflow Automation Platform</p>
      <div className="card">
        <div className="stats">
          <div className="stat-item">
            <span className="stat-number">2,080+</span>
            <span className="stat-label">Workflows</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">238</span>
            <span className="stat-label">Active</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">400+</span>
            <span className="stat-label">Integrations</span>
          </div>
        </div>
        <button onClick={() => setCount((count) => count + 1)}>
          Workflows Executed: {count}
        </button>
        <p className="description">
          Empowering healthcare organizations with intelligent automation
        </p>
      </div>
      <p className="read-the-docs">
        Built with excellence for healthcare professionals
      </p>
    </>
  )
}

export default App
