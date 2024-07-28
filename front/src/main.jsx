import React from 'react'
import ReactDOM from 'react-dom/client'

// Pages
import Home from './js/pages/Home.jsx'
import DetecImg from './js/pages/DetecImg.jsx'
import Assistant from './js/pages/Assistant.jsx'
import Ordonnance from './js/pages/Ordonnance.jsx'

// Error Pages
import Error404 from './js/pages/error/Error404.jsx'

// CSS
import '../src/css/index.css'

import { BrowserRouter, Routes, Route } from "react-router-dom";

ReactDOM.createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/Assistant" element={<Assistant />} />
      {/*}
      <Route path="/img-detection" element={<DetecImg />} />
      <Route path="/ordonnance" element={<Ordonnance />} />
      */}
      {/* Si la route n'existe pas */}
      <Route path="*" element={<Error404 />} />
    </Routes>
</BrowserRouter>
)
