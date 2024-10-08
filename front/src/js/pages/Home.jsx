import { useState } from 'react'
import axios from 'axios'

// Components
import NavBar from '../components/VerticalMenu.jsx'
import Footer from '../components/Foot.jsx'

// CSS
import '../../css/App.css'

function App() {
  return (
    <>
      <NavBar/>
      <div className="HomePage-info">
        <h1>Projet de détection de maladies</h1>
        <div className="App">
            <p>Le but de ce projet est de permettre à des patients de détecter des maladies à partir d'une discution avec un assistant virtuel.</p>
        </div>
        <Footer/>
      </div>
    </>
  )
}

export default App