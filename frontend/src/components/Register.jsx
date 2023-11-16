import React, {useContext, useState} from "react";

import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

const Register = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);

    const submitRegistration = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: password, username: username })
        };

        const response = await fetch("http://127.0.0.1:8000/api/auth/signup", requestOptions);
        const data = await response.json();

            if (!response.ok) {
                console.log("something went wrong")
                setErrorMessage(data.detail);
            } else {
                setToken(data.access_token);
                console.log("ok")
            }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (password.length > 5) {
            submitRegistration();
        } else {
            setErrorMessage(" Password must contain at least 6 symbols")
        }
    }

    return (
        <div className="column">
            <form className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centred">Register</h1>
                <div className="field">
                    <label className="label">Email</label>
                    <div className="control">
                        <input
                            type="email"
                            placeholder="Enter email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>

                <div className="field">
                    <label className="label">Password</label>
                    <div className="control">
                        <input
                            type="password"
                            placeholder="Enter password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>

                <div className="field">
                    <label className="label">Username</label>
                    <div className="control">
                        <input
                            type="username"
                            placeholder="Enter username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="input"
                            required
                        />
                    </div>
                </div>
                <br />
                <button className="button is-info is-light" type="submit">
                    Register
                </button>
            </form>
        </div>
    )
};

export default Register;