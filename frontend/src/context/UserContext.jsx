import React, { createContext, useState, useEffect } from "react";
import ErrorMessage from "../components/ErrorMessage";

export const UserContext = createContext();

export const UserProvider = (props) => {
  const storedToken = localStorage.getItem("awesomeLeadsToken");
  const [token, setToken] = useState(storedToken);
  const [errorMessage, setErrorMessage] = useState("");

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const storedToken = localStorage.getItem("awesomeLeadsToken");

                if (!storedToken) {
                    console.log("Token is missing in localStorage");
                    return;
                }

                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${storedToken}`,
                    },
                };

                const response = await fetch("http://127.0.0.1:8000/api/auth/refresh_token", requestOptions);

                if (!response.ok) {
                    console.error("Something went wrong", response.statusText);
                    const errorMessage = await response.text();
                    setErrorMessage(errorMessage);
                } else {
                    console.log("OK");
                    const data = await response.json();
                    localStorage.setItem("awesomeLeadsToken", data.access_token);
                    setToken(data.access_token);
                }
            } catch (error) {
                console.error("Error fetching user:", error);
            }
        };

        fetchUser();
    }, []); // Пустой массив зависимостей, чтобы useEffect выполнялся только при монтировании компонента

    return (
        <UserContext.Provider value={[token, setToken]}>
            {props.children}
            {errorMessage && <ErrorMessage message={errorMessage} />}
        </UserContext.Provider>
    );
};
