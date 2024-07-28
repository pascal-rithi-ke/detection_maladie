import { useState } from 'react'
import axios from 'axios'

import '../../css/App.css'

// Components
import NavBar from '../components/Chatbot.jsx'
import Footer from '../components/footer.jsx'

function DetecImg() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [text_result, setTextResult] = useState(null);
  const [textUpload, setTextUpload] = useState("Déposer une image");
  const [formatImage, setFormatImage] = useState(null);

  function handleCancelImage() {
    setImage(null);
    setTextResult(null);
    setImagePreview(null);
    setFormatImage(null);
    setResult(null);
    setTextUpload("Déposer une image");
  }

  function handleImageChange(e) {
    const selectedImage = e.target.files[0];
    setImage(selectedImage);
    setFormatImage(selectedImage.type);

    setImagePreview(null);
    setResult(null);
    
    // Vérifier le format de l'image
    if (selectedImage.type !== "image/png" && selectedImage.type !== "image/jpeg") {
      setTextResult("Le format de l'image n'est pas valide (.png ou .jpeg)");
      // Cacher l'image si le format n'est pas pris en charge
      setImage(null);
      setTextUpload("Déposer une image");
      return;
    }
  
    // Effacer le message d'erreur si tout est correct
    setTextResult(null);
    setTextUpload("Changer l'image");
  }

  function handleSubmitImage() {
    const formData = new FormData();
    formData.append('image', image);
  
    axios.post('http://localhost:5000/processImage', formData, {
      params: {
        format: formatImage
      },
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(res => {
      setTextResult(res.data.message);
      setImagePreview(res.data.upload_image);
      setResult("Analyse terminée: " + res.data.message_test);
      setImage(null);
      setFormatImage(null);
      setTextUpload("Lancer une nouvelle analyse")
    })
    .catch(err => {
      console.log(err);
      setTextResult("Erreur lors de l'analyse de l'image");
    })
  }

  return (
    <>
      <NavBar />
      <div className="App">
        
        <div className='App-part'>
          <div className='App-part-header'>
            <h2>Déposer une image pour l'analyse</h2>
          </div>
          <div className='App-part-text'>
            <p>Note:<br/>Votre image sera insérée dans notre base de données afin de nous aider à améliorer notre modèle de prédiction</p>
          </div>
          <div className='App-part-content'>
            <button className="custom-file-input">
              {textUpload}
              <input type="file" onChange={handleImageChange} />
            </button>
            {imagePreview && (
              <>
                <div className='App-part-container-preview-img'>
                  <div className='App-part-content-preview-img'>
                    <img className='preview-img' src={imagePreview} alt="image" />
                  </div>
                </div>
              </>
            )}
            {text_result !== null && (
              <p className='errorText'>{text_result}</p>
            )}
            {text_result === null && image && (
            <>
              <button onClick={handleCancelImage}>Annuler</button>
              <div className='App-part-container-preview-img'>
                <div className='App-part-content-preview-img'>
                  <img className='preview-img' src={URL.createObjectURL(image)} alt="image" />
                </div>
                <button onClick={handleSubmitImage}>Lancer l'analyse</button>
              </div>
            </>
            )}
          </div>
        </div>

        <div className='App-part'>
          <div className='App-part-header'>
            <h2>Résultat de l'analyse</h2>
          </div>
          {result && (
            <>
              <p className='resultText'>{result}</p>
            </>
          )}
        </div>
      </div>
      <Footer />
    </>
  )
}

export default DetecImg