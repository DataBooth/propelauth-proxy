default:
    @just --list

propelauth:
    npm i @propelauth/auth-proxy && npm install dotenv

proxy:
    node proxy.mjs