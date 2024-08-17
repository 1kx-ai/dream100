import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Welcome to Your App</h1>
      <button className="btn btn-primary">Click me</button>
      <div className="card w-96 bg-base-100 shadow-xl mt-4">
        <div className="card-body">
          <h2 className="card-title">Card title</h2>
          <p>This is a card component from daisyUI.</p>
          <div className="card-actions justify-end">
            <button className="btn btn-secondary">More info</button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
