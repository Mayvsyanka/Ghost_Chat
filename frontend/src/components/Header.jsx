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
            <img src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg" style={{ maxWidth: '200px', width: '100%', position: 'fixed',top: '10px',left: '10px' }}/>
        </figure> 
        <h1 className="title" style={{top: '-300px'}}>Ghost Application</h1>
            {token && (<button className="button is-danger is-large" style={{position: 'fixed',top: '10px',right: '10px',}}onClick={handleLogout}>
                Logout
            </button>)}
    </>
    );
};

export default Header;