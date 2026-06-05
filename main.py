from fastapi import FastAPI, HTTPException
from schemas import ChatRequest, ChatResponse
from model import get_model

app = FastAPI()

@app.post("/v1/chat/completions")
async def llm_communication(request: ChatRequest):
    llm = get_model()
    result = llm.create_chat_completion(
        messages=[
            {"role": m.role, "content": m.content} for m in request.messages
            ]
        )
    
    return ChatResponse(
        model=request.model,
        content=result["choices"][0]["message"]["content"]   
    )