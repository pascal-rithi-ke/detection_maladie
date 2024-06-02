import '../../css/pages/NavBar.css'

function NavBar(){
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                <li><a href="/">Home</a></li>
                <li><a href="/Assistant">Assistant</a></li>
                <li><a href="/img-detection">Detection d'image</a></li>
                <li><a href="/Ordonnance">Ordonnance</a></li>
            </ul>
        </nav>
    )
}

export default NavBar