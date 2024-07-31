import React, { useState } from 'react';
import '../../css/VerticalMenu.css';
// Importez l'image
import menuIcon from '../../img/menu.png'; // Chemin de l'image
import closeIcon from '../../img/close.png'; // Chemin de l'image

function VerticalMenu() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [iconSrc, setIconSrc] = useState(menuIcon);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
        setIconSrc(isMenuOpen ? menuIcon : closeIcon);
    }

    return (
        <div className="vertical-menu-container">
            <img 
                src={iconSrc} 
                alt="Menu" 
                className={`menu-icon ${isMenuOpen ? 'rotate' : ''}`}
                onClick={toggleMenu}
            />
            <div className={`vertical-menu ${isMenuOpen ? 'open' : ''}`}>
                <a href="/">Home</a>
                <a href="/Assistant">ChatBot assistant</a>
            </div>
        </div>
    );
}

export default VerticalMenu;