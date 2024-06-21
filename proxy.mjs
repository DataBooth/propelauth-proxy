import { initializeAuthProxy } from '@propelauth/auth-proxy';
import dotenv from 'dotenv';

dotenv.config();

await initializeAuthProxy({
    authUrl: process.env.PROPEL_AUTH_URL,
    integrationApiKey: process.env.PROPEL_API_KEY,
    proxyPort: 8000,
    urlWhereYourProxyIsRunning: process.env.PROXY_SERVER_URL,
    target: {
        host: process.env.TARGET_HOST,
        port: process.env.TARGET_PORT,
        protocol: process.env.TARGET_PROTOCOL
    },
});


// import { initializeAuthProxy } from '@propelauth/auth-proxy'

// // Replace with your configuration
// await initializeAuthProxy({
//     authUrl: "YOUR_AUTH_URL",
//     integrationApiKey: "YOUR_API_KEY",
//     proxyPort: 8000,
//     urlWhereYourProxyIsRunning: 'http://localhost:8000',
//     target: {
//         host: 'localhost',
//         port: 8501,
//         protocol: 'http:'
//     },
// })