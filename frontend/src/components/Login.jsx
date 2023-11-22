import React, { useState, useContext } from "react"

import ForgotPassword from "./ForgotPassword";
import ErrorMessage from "./ErrorMessage"
import { UserContext } from "../context/UserContext"

const Login = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMessage, setErrorMessage] = useState("");
    const [, setToken] = useContext(UserContext);
    const [showForgotPassword, setShowForgotPassword] = useState(false);
    const [showSignUp, setShowSignUp] = useState(false);
    const [showLogin, setShowLogin] = useState(false);

    const handleForgetPasswordClick = () => {
        setShowForgotPassword(true);
        setShowLogin(false);
        setShowSignUp(false);
    };
    /*
    const submitLogin = async () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: JSON.stringify('grant_type=&username=${email}&password=${password}&scope=&client_id=&client_secret='),
        };
        const response = await fetch("http://127.0.0.1:8000/api/auth/login", requestOptions);
        const data = await response.json();
        
        if (!response.ok) {
            console.log("something went wrong")
            setErrorMessage(data.detail);
        } else {
            setToken(data.access_token);
            console.log("ok")
        }
    };
    */
    const submitLogin = async () => {

        console.log("Sending login request...");

        const requestBody = new URLSearchParams();
        requestBody.append("grant_type", "");
        requestBody.append("username", email);
        requestBody.append("password", password);
        requestBody.append("scope", "");
        requestBody.append("client_id", "");
        requestBody.append("client_secret", "");

        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: requestBody.toString(),
        };

        console.log("Request sent!");

        const response = await fetch("http://localhost:8000/api/auth/login", requestOptions);
        const data = await response.json();

        if (!response.ok) {
            console.log("something went wrong");
            setErrorMessage(data.detail);
        } else {
            setToken(data.access_token);
            console.log("ok");
        }
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        submitLogin();
    }

    return (
    <div className="column">
        {showForgotPassword ? (
            <ForgotPassword />
        ) : (
            <form className="box" onSubmit={handleSubmit}>
                <h1 className="title has-text-centred">Login</h1>
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

                <br />
                <button className="button is-info is-ghost is-light" type="submit">
                    Login
                </button>
            </form>
        )}
        {!showForgotPassword && (
            <>
                <button
                    className="button is-info is-text is-light"
                    type="button"
                    onClick={handleForgetPasswordClick}
                >
                    Forget password?
                </button>
                
            </>
        )}
    </div>
);
};

export default Login;