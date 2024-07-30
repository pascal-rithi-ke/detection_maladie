
// Components
import VerticalMenu from '../components/VerticalMenu.jsx'
import Footer from '../components/footer.jsx'
import Chatbot from '../components/Chatbot.jsx' // Importez le composant Chatbot

function Assistant() {
    return (
        <>
            <VerticalMenu />
            <div className="App">
                <Chatbot /> {/* Ajoutez le composant Chatbot */}
            </div>
            <Footer />
        </>
    )
}

export default Assistant