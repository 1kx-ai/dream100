import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { setApiToken, setApiUrl } from './services/apiConfig.js';

window.setApiToken = setApiToken;
window.setApiUrl = setApiUrl;

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
