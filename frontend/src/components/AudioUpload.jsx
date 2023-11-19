import React, { useState } from 'react';

const AudioUpload = () => {
    const [selectedAudio, setSelectedAudio] = useState(null);

    const handleAudioChange = (e) => {
        setSelectedAudio(e.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedAudio) {
            alert('Please select a file.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedAudio);

        try {
            const response = await fetch('http://localhost:8000/api/document/audio/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                console.log('File uploaded successfully:', data);
            } else {
                console.error('File upload failed.');
            }
        } catch (error) {
            console.error('An error occurred during file upload:', error);
        }
    };

    return (
        <div className="has-text-centered mt-4">
            <div>
                <h2>Audio Upload</h2>
                <input type="file" onChange={handleAudioChange} />
                <button onClick={handleUpload}>Upload</button>
            </div>
        </div>
    );
}

export default AudioUpload;