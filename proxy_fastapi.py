from fastapi import FastAPI, Request, HTTPException
import httpx
from dotenv import load_dotenv
import os
import uvicorn


load_dotenv()

app = FastAPI()

PROPEL_TRY_AUTH_URL = os.getenv("PROPEL_TRY_AUTH_URL")
PROPEL_TRY_API_KEY = os.getenv("PROPEL_TRY_API_KEY")
TARGET_URL = "http://localhost:8501"  # The target URL you're proxying to

async def verify_token_with_propelauth(token: str) -> bool:
    # This function should implement the logic to verify the token with PropelAuth
    # using PROPEL_TRY_AUTH_URL and PROPEL_TRY_API_KEY. This is a placeholder.
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {PROPEL_TRY_API_KEY}"}
        # Assuming PropelAuth provides an endpoint for token verification
        response = await client.post(f"{PROPEL_TRY_AUTH_URL}/api/backend/v1/end_user_api_keys/validate", headers=headers, json={"token": token})
        return response.status_code == 200

async def proxy_request(http_method: str, path: str, request: Request):
   # Prepare the headers you want to add/modify in the request
    header_auth = {"Authorization": f"Bearer {PROPEL_TRY_API_KEY}"}
    
    # Extract existing headers from the incoming request
    headers = dict(request.headers)
    
    # Remove headers that might cause issues or are not needed
    headers.pop("host", None)
    headers.pop("content-length", None)    
    headers.update(header_auth)
    token = request.headers.get("Authorization")
    print(f"Token: {token}")
    if not token or not await verify_token_with_propelauth(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    async with httpx.AsyncClient() as client:
        url = f"{TARGET_URL}/{path}"
        headers = dict(request.headers)
        # Forward the request to the target URL
        response = await client.request(http_method, url, content=await request.body(), headers=headers, params=request.query_params)
        return response

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    header_auth = {"Authorization": f"Bearer {PROPEL_TRY_API_KEY}"}
    print(request.headers)
    # Extract the token
    token = request.headers.get("Authorization")
    print(f"Extracted Token: {token}")  # This will help you verify if the token is being received correctly

    return await proxy_request(request.method, path, request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)