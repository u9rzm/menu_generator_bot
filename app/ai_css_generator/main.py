from fastapi import FastAPI, HTTPException
from guard import PromptRequest
from openai_client import call_openai, check_openai_health

app = FastAPI()

@app.post("/generate")
async def generate(data: PromptRequest):
    response = await call_openai(data.prompt)
    return {"status": "ok", "result": response}

@app.get("/health")
async def health():
    try:
        await check_openai_health()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
