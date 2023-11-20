import React, {useContext} from "react"

import { UserContext } from "../context/UserContext"

const Header = ({ title }) => {
    const [token, setToken] = useContext(UserContext);

    const handleLogout = () => {
        setToken(null);
    };

    return (
    <>
        <figure class="image is-flex is-justify-content-center">
            <img src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg" style={{ maxWidth: '300px', width: '100%', position: 'fixed',top: '10px',left: '10px' }}/>
        </figure> 
        <div className="has-text-centred m-6" style={{ position: 'fixed',top: '-10px', left: '500px' }}>
            <h1 className="title">{title}</h1>
            {token && (<button className="button is-danger is-large" style={{position: 'fixed',top: '10px',right: '10px',}}onClick={handleLogout}>
                Logout
            </button>)}
        </div>
    </>
    );
};

export default Header;