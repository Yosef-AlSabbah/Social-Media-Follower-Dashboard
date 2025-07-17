import { createRoot } from 'react-dom/client';
import App from './App.tsx'
import './index.css'
import { initializeApp } from './lib/api-client'

// Initialize API configuration and app setup
initializeApp()

createRoot(document.getElementById("root")!).render(<App />);
