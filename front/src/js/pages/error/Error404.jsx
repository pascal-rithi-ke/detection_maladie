import { useState, useEffect } from "react";
import '../../../css/error404.css';

function Error404() {
    
    const [count, setCount] = useState(5);

    useEffect(() => {
        const interval = setInterval(() => {
            setCount(count - 1);
        }, 1000);
        return () => clearInterval(interval);
    }, [count]);

    // Si le compte à rebours est terminé, rediriger l'utilisateur vers la page d'accueil
    if (count === 0) {
        window.location.href = "/";
    }

    return (
        <div className="error404">
            <h1>Erreur 404: <br/> Page non trouvée</h1>
            <p>Redirection vers la page d'accueil dans <span>{count}</span> secondes...</p>
            <img className="error404-img" src="../src/img/error404.webp" />
        </div>
    )
}

export default Error404;