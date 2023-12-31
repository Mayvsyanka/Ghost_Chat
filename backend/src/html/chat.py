html = """
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket File Upload</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #white;
            margin: 20px;
        }

        h1 {
            color: black;
            text-align: center;
            margin-top: -20px
        }

        #fileInput {
            display: none;
            border-radius: 10px;
            background-color: #3498db;
        }

        #uploadButton {
            padding: 10px 20px;
            border-radius:10px;
            border: none;
            background-color: #209CEE;
            color: white;
            cursor: pointer;
            borderRadius: 60px;
            display: inline-block;
        }

        #questionInput {
            border: 1px solid #ccc;
            padding: 8px;
            width: calc(80% - 120px); 
            height: 100px; 
            resize: vertical;
            margin-top: 20px;
            display: inline-block; 
        }

        #sendQuestionButton {
            padding: 10px 20px;
            border: none;
            border-radius:10px;
            background-color: #209CEE;
            color: white;
            cursor: pointer;
            display: inline-block; 
            vertical-align: top; 
            margin-top: 20px;
            margin-left: 20px; 
            borderRadius: 5px
        }

        #disconnectButton {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 10px;
            border: none;
            background-color: #e74c3c;
            color: white;
            cursor: pointer;
            border-radius: 10px;
        }

        #output {
            background-color: #7DF9FF;
            padding: 10px;
            max-height: 300px; 
            margin-top: 10px;
            overflow-y: auto; 
        }

        p {
            color: black;
        }
    </style>
</head>
<body>
    <img src="https://i.ibb.co/tp1Q4Y2/Ghostgam.jpg" width="150">
    <h1>Welcome to ZEN-GHOST chat!</h1>
    <br>
    <br>
    <label for="fileInput" id="uploadButton">Upload File</label>
    <input type="file" id="fileInput">
    <button onclick="sendFile()">Send File</button>
    <br>
    <textarea id="questionInput" placeholder="Type your question..."></textarea>
    <button onclick="sendQuestion()" id="sendQuestionButton">Send Question to Ghost</button>
    <br>
    <button id="disconnectButton">Home page</button>
    <div id="output"></div>

    <script>
        const socket = new WebSocket('ws://127.0.0.1:8000/api/chat');

        document.getElementById('disconnectButton').addEventListener('click', function() {
        window.location.href = 'http://127.0.0.1:3000/';
        socket.send('disconnect');
        });


        socket.addEventListener('open', (event) => {
            console.log('Connected to WebSocket');
        });

        socket.addEventListener('message', (event) => {
            const outputDiv = document.getElementById('output');
            outputDiv.innerHTML += `<p>${event.data}</p>`;
        });

        function sendFile() {
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];

            if (file) {
                const reader = new FileReader();
                reader.onload = function(event) {
                    socket.send(event.target.result);
                };
                reader.readAsArrayBuffer(file);
            }
        }

        function sendQuestion() {
            const questionInput = document.getElementById('questionInput');
            const question = questionInput.value;

            if (question.trim() !== '') {
                socket.send(question);
                questionInput.value = '';
            }
        }
    </script>
</body>
</html>
"""
