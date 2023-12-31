import React, { useState } from 'react';

const AudioUpload = () => {
  const [fileRoute, setFileRoute] = useState('');
  const [transcription, setTranscription] = useState('');

  const handleFileRouteChange = (event) => {
    setFileRoute(event.target.value);
  };

  const handleTranscription = async () => {
    if (!fileRoute.trim()) {
      console.log('Part to your file');
      return;
    }

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/audio/audio?route=${encodeURIComponent(fileRoute)}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const result = await response.json();
        setTranscription(result);
      } else {
        console.error('Ошибка при транскрипции аудио');
      }
    } catch (error) {
      console.error('Ошибка при транскрипции аудио', error);
    }
  };

  return (
    <div>
      <h1>Download your file</h1>
      <input type="text" value={fileRoute} onChange={handleFileRouteChange} placeholder="Route to file" />
      <button onClick={handleTranscription}>Convert audio</button>
      {transcription && (
        <div>
          <h2>Result</h2>
          <p>{transcription}</p>
        </div>
      )}
    </div>
  );
};

export default AudioUpload;