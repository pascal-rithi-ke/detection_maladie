import { useState, useEffect } from "react";

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
        <div>
            <h1>Erreur 404: Page non trouvée</h1>
            <p>Redirection vers la page d'accueil dans {count} secondes...</p>
        </div>
    )
}

export default Error404;