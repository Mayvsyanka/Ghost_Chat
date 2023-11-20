import React, { useContext, useEffect, useState } from "react"

import AudioUpload from "./AudioUpload";

const Home = () => {
  
  const [showFileUpload, setShowFileUpload] = useState(false);
  const [showAudioUpload, setShowAudioUpload] = useState(false);
  return (
            <>
              <h1 className="title has-text-centered">Choose file type</h1>
              <div className="buttons is-flex is-justify-content-center mt-1">
                <div className="button is-info is-large mr-6" onClick={() => (window.location.href = 'http://127.0.0.1:8000/api/chat')}>
                  Documents
                </div>
                <div className="button is-info is-large" onClick={() => setShowAudioUpload(true)}>
                  Audio
                </div>
                </div>
                {showAudioUpload && <AudioUpload />}
            </>
  );
};

export default Home;
