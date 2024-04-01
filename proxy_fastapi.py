import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
import uvicorn

load_dotenv()

app = FastAPI()

PROPEL_TRY_AUTH_URL = os.getenv("PROPEL_TRY_AUTH_URL")
PROPEL_TRY_API_KEY = os.getenv("PROPEL_TRY_API_KEY")
TARGET_URL = "http://localhost:8501"  # The target URL you're proxying to


async def proxy_request(http_method: str, path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{TARGET_URL}/{path}"
        headers = dict(request.headers)
        # Remove headers that shouldn't be forwarded
        headers.pop("host", None)
        headers.pop("content-length", None)
        if http_method == "GET":
            response = await client.get(url, params=request.query_params, headers=headers)
        elif http_method == "POST":
            body = await request.body()
            response = await client.post(url, content=body, headers=headers)
        elif http_method == "PUT":
            body = await request.body()
            response = await client.put(url, content=body, headers=headers)
        elif http_method == "DELETE":
            response = await client.delete(url, headers=headers)
        elif http_method == "PATCH":
            body = await request.body()
            response = await client.patch(url, content=body, headers=headers)
        else:
            return {"error": "Unsupported HTTP method"}
        return Response(
            content=response.content, status_code=response.status_code, headers=dict(response.headers)
        )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(path: str, request: Request):
    return await proxy_request(request.method, path, request)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
