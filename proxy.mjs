import { initializeAuthProxy } from '@propelauth/auth-proxy';
import dotenv from 'dotenv';

dotenv.config();

await initializeAuthProxy({
    authUrl: process.env.PROPEL_TRY_AUTH_URL,
    integrationApiKey: process.env.PROPEL_TRY_API_KEY,
    proxyPort: 8000,
    urlWhereYourProxyIsRunning: 'http://localhost:8000',
    target: {
        host: 'localhost',
        port: 8501,
        protocol: 'http:'
    },
});