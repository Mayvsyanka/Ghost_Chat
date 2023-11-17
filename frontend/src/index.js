import React from 'react';
import { createRoot } from 'react-dom/client';
import "bulma/css/bulma.min.css";
import App from './App';

import {UserProvider} from "./context/UserContext"

const root = document.getElementById("root");
const rootInstance = createRoot(root);

rootInstance.render(
    <UserProvider>
        <App />
    </UserProvider>
);

