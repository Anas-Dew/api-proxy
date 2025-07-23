from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
import websockets
import json

app = FastAPI(
    title="Proxy API",
    description="An API that calls APIs",
    version="1.0.0",
)

class APICallRequest(BaseModel):
    url: str = Field(..., example="https://api.example.com/v1/resource")
    method: str = Field(..., example="GET")
    body: dict | None = Field(default=None, example={"key": "value"})
    headers: dict | None = Field(default=None, example={"Authorization": "Bearer token"})

@app.get("/health")
async def health_check():
    return {"status": "OK"}

@app.post("/call-api")
async def call_api(payload: APICallRequest):
    method = payload.method.upper()

    try:
        if method == "SOCKET":
            # Handle WebSocket connection
            import asyncio
            additional_headers = payload.headers or {}
            messages = []
            async with websockets.connect(
                payload.url,
                additional_headers=additional_headers
            ) as websocket:
                # Send body if provided
                if payload.body:
                    await websocket.send(json.dumps(payload.body))

                async def receive_messages():
                    while True:
                        try:
                            msg = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                            messages.append(msg)
                        except asyncio.TimeoutError:
                            # No message received in this interval, continue
                            continue
                        except websockets.exceptions.ConnectionClosed:
                            break

                # Listen for 3 seconds
                try:
                    await asyncio.wait_for(receive_messages(), timeout=3)
                except asyncio.TimeoutError:
                    pass

                return {
                    "status_code": 200,
                    "headers": {},
                    "body": messages
                }
        else:
            # Handle HTTP requests
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
                
                return {
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "body": response.text
                }
    except websockets.exceptions.WebSocketException as e:
        raise HTTPException(status_code=500, detail=f"WebSocket error: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
