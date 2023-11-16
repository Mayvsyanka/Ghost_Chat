import React, {useContext} from "react"

import { UserContext } from "../context/UserContext"

const Header = ({ title }) => {
    const [token, setToken] = useContext(UserContext);

    const handleLogout = () => {
        setToken(null);
    };

    return (
        <div className="has-text-centred m-6">
            <h1 className="title">{title}</h1>
            {token && (<button className="button is-danger is-large" onClick={handleLogout}>
                Logout
            </button>)}
        </div>
    );
};

export default Header;