
// Components
import VerticalMenu from '../components/VerticalMenu.jsx'
import Footer from '../components/footer.jsx'
import Chatbot from '../components/Chatbot.jsx' // Importez le composant Chatbot

function Assistant() {
    return (
        <>
            <div style={{ display: 'flex' }}>
                <VerticalMenu />
                <div className="App">
                    <h1>Assistant</h1>
                    <Chatbot /> {/* Ajoutez le composant Chatbot */}
                </div>
            </div>
            <Footer />
        </>
    )
}

export default Assistant