import { useState } from 'react'
import './App.css'

function App() {
  const [image, setImage] = useState(null)
  const [text_result, setTextResult] = useState(null)

  function handleCancelImage() {
    setImage(null)
    setTextResult(null)
  }

  function handleSubmitImage() {
    console.log('image', image)
  }

  function handleImageChange(e) {
    const selectedImage = e.target.files[0];
    setImage(selectedImage);
  
    // Vérifier le format de l'image
    if (selectedImage.type !== "image/png" && selectedImage.type !== "image/jpeg") {
      setTextResult("Le format de l'image n'est pas valide (.png ou .jpeg)");
      // Cacher l'image si le format n'est pas pris en charge
      setImage(null);
      return;
    }
  
    // Vérifier la taille de l'image
    if (selectedImage.size > 10000000) {
      setTextResult("L'image est trop lourde");
      // Cacher l'image si elle est trop lourde
      setImage(null);
      return;
    }
  
    // Effacer le message d'erreur si tout est correct
    setTextResult(null);
  }

  return (
    <>
      <h1>Prédiction de maladie</h1>
      <div className="App">
        
        <div className='App-part'>
          <div className='App-part-header'>
            <h2>Déposer une image pour l'analyse</h2>
          </div>
          <div className='App-part-content'>
            <button className="custom-file-input">
              Déposer une image
              <input type="file" onChange={handleImageChange} />
            </button>
            {text_result !== null && <p className='errorText'>{text_result}</p>}
            {text_result === null && image && 
            <>
              <button onClick={handleSubmitImage}>Lancer l'analyse</button>
              <button onClick={handleCancelImage}>Annuler</button>
              <div className='App-part-container-preview-img'>
                <img className='preview-img' src={URL.createObjectURL(image)} alt="image" />
              </div>
            </>
            }
          </div>
        </div>

        <div className='App-part'>
          <div className='App-part-header'>
            <h2>Résultat de l'analyse</h2>
          </div>
        </div>

      </div>
    </>
  )
}

export default App