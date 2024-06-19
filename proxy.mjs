import { initializeAuthProxy } from '@propelauth/auth-proxy';
import dotenv from 'dotenv';

dotenv.config();

await initializeAuthProxy({
    authUrl: process.env.PROPEL_TRY_AUTH_URL,
    integrationApiKey: process.env.PROPEL_TRY_API_KEY,
    proxyPort: 8000,
    urlWhereYourProxyIsRunning: process.env.RENDER_PROXY_URL,
    target: {
        host: process.env.TARGET_HOST,
        port: process.env.TARGET_PORT,
        protocol: process.env.TARGET_PROTOCOL
    },
});