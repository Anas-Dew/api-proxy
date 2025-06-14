from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

app = FastAPI()

class APICallRequest(BaseModel):
    url: str = Field(..., example="https://api.example.com/v1/resource")
    method: str = Field(..., example="GET")
    body: dict | None = Field(default=None, example={"key": "value"})
    headers: dict | None = Field(default=None, example={"Authorization": "Bearer token"})

@app.post("/call-api")
async def call_api(payload: APICallRequest):
    method = payload.method.upper()

    try:
        async with httpx.AsyncClient() as client:
            if method == "GET":
                response = await client.get(
                    url=payload.url,
                    headers=payload.headers,
                    timeout=30
                )
            elif method == "POST":
                response = await client.post(
                    url=payload.url,
                    json=payload.body,
                    headers=payload.headers,
                    timeout=30
                )
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response.text
    }
