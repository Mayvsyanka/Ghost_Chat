import React, { useContext, useEffect, useState } from "react"

import Register from "./components/Register";
import { UserContext } from "./context/UserContext";
import Header from "./components/Header";
import Login from "./components/Login";
import ForgotPassword from "./components/ForgotPassword";
import FileUpload from "./components/FileUploader";
import AudioUpload from "./components/AudioUpload";
import Home from "./components/Home"; 
import ImageUpload from "./components/ImageUpload";

const App = () => {
  const [message, setMessage] = useState("");
  const [token,] = useContext(UserContext);
  const [showLogin, setShowLogin] = useState(false);
  const [showSignUp, setShowSignUp] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [showAudioUpload, setShowAudioUpload] = useState(false);
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [showHomeUpload, setShowUpload] = useState(false)

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

  const handleFileUploaderClick = () => {
  setShowSignUp(false);
  setShowLogin(false);
  setShowFileUpload(true);
  setShowAudioUpload(false);
  };

  const handleAudioUploaderClick = () => {
  setShowSignUp(false);
  setShowLogin(false);
  setShowAudioUpload(true);
  setShowFileUpload(false);
  };

  

  return (
    <>
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">
          {!token ? (
            <>
              {!showForgotPassword && (
                <>
                  <div className="has-text-centered is-large m-6">
                  <h1 className="title">Ghost-zen App</h1></div>
                  <figure class="image is-flex is-justify-content-center">
                    <img src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg" style={{ maxWidth: '300px', width: '100%' }}/>
                  </figure>  
                  <div className="buttons is-flex is-justify-content-center mt-1">
                  <div className="button is-info is-large mr-6" onClick={() => { setShowSignUp(false); setShowLogin(true) }}>
                    Login
                  </div>
                  <div className="button is-info is-large" onClick={() => { setShowSignUp(true); setShowLogin(false) }}>
                    SignUp
                  </div>
                  </div>
                 </> 
              )}
              {showLogin && <Login />}
              {showSignUp && <Register />}
              {showForgotPassword && <ForgotPassword />}
            </>
          ) : (
            <>
              <div className="has-text-centered is-large m-6">
              <Header title={message} /></div>
              <h1 className="title has-text-centered">Choose file type</h1>
              <div className="buttons is-flex is-justify-content-center mt-1">
                <button className="button is-info is-large mr-6" onClick={() => (window.location.href = 'http://127.0.0.1:8000/api/chat')}>
                  Document
                </button>
                  <div className="button is-info is-large" onClick={() => { setShowAudioUpload(true); setShowImageUpload(false) }}>
                  Audio
                </div>
                  <div className="button is-info is-large ml-6" onClick={() => { setShowImageUpload(true); setShowAudioUpload(false); }}>
                  Image
                </div>
              </div>
                {showAudioUpload && <AudioUpload />}
                {showImageUpload && <ImageUpload />}
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
