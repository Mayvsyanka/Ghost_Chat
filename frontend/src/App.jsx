import React, { useContext, useEffect, useState } from "react"

import Register from "./components/Register";
import { UserContext } from "./context/UserContext";
import Header from "./components/Header";
import Login from "./components/Login";
import ForgotPassword from "./components/ForgotPassword";
import FileUpload from "./components/FileUploader";

const App = () => {
  const [message, setMessage] = useState("");
  const [token,] = useContext(UserContext);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("http://localhost:8000/api", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("something went wrong")
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage()
  }, []);

  const handleForgotPasswordClick = () => {
  setShowSignUp(false);
  setShowLogin(false);
  setShowForgotPassword(true);
};

  return (
    <><div className="has-text-centered is-large m-6">
      <Header title={message} /></div>
      <figure class="image is-flex is-justify-content-center">
        <img src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg" style={{ maxWidth: '300px', width: '100%' }}/>
      </figure>
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">
          {!token ? (
            <>
              {!showForgotPassword && (  // Показываем кнопки только если showForgotPassword равен false
                <div className="buttons is-flex is-justify-content-center mt-1">
                  <div className="button is-info is-large mr-6" onClick={() => { setShowSignUp(false); setShowLogin(true)}}>
                    Login
                  </div>
                  <div className="button is-info is-large" onClick={() => { setShowSignUp(true); setShowLogin(false)}}>
                    SignUp
                  </div>
                </div>
              )}
              {showLogin && <Login />}
              {showSignUp && <Register />}
              {showForgotPassword && <ForgotPassword />}
            </>
          ) : (
              <>
                <h1 class="title has-text-centered">Choose file type</h1>
                  <div className="buttons is-flex is-justify-content-center mt-1">
                    <div className="button is-info is-large mr-6" onClick={() => { setShowSignUp(false); setShowLogin(true)}}>
                      Documents
                    </div>
                    <div className="button is-info is-large mr-6" onClick={() => { setShowSignUp(false); setShowLogin(true)}}>
                      Audio
                    </div>
                  </div>
              </>
          )}
        </div>
        <div className="column"></div>
      </div>
    </>
  );
}

export default App;

  /*return (
    <>
      <Header title={message} />
      <div className="buttons">
        {!token ? (
            <><div className="button" onClick={handleLoginClick}>
            Login
          </div><div className="button" onClick={handleSignUpClick}>
              SignUp
            </div></>
          ) : (
            <p>Table</p>
          )}
      </div>
      {showLogin && <Login />}
      {showSignUp && <Register />}
      {}
    </>
  );
};


export default App;*/
