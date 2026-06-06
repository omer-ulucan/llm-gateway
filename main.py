from fastapi import FastAPI, HTTPException
from schemas import ChatRequest, ChatResponse
from model import get_model
import mlflow
import time


mlflow.set_tracking_uri("https://localhost:5000")
mlflow.set_experiment("llm-gateway")


app = FastAPI()

@app.post("/v1/chat/completions")
@mlflow.trace
async def llm_communication(request: ChatRequest):
    llm = get_model()
    start = time.time()

    result = llm.create_chat_completion(
        messages=[
            {"role": m.role, "content": m.content} for m in request.messages
            ]
        )
    
    content = result["choices"][0]["message"]["content"]  

    latency = time.time() - start
    token_count = result["usage"]["total_tokens"]
    response_length = len(result["choices"][0]["message"]["content"])

    mlflow.log_metric("latency", latency)
    mlflow.log_metric("token_count", token_count)
    mlflow.log_metric("response_length", response_length)
    
    return ChatResponse(
        model=request.model,
        content=content
    )