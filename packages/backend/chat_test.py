#!/usr/bin/env python3

import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json
import uvicorn

app = FastAPI(title="Chat Test API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger = logging.getLogger(__name__)

class ChatMessage(BaseModel):
    id: str
    content: str
    sender: str  # 'user' or 'ai'
    timestamp: str
    type: Optional[str] = 'text'  # 'text', 'claim-preview', 'analysis', 'suggestion'
    data: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    messages: List[ChatMessage]

# RCM-specific system prompt for Alex persona
RCM_SYSTEM_PROMPT = """You are Alex, an AI-powered Revenue Cycle Management (RCM) expert with over 15 years of experience in medical claims processing, denial management, and healthcare revenue optimization. You work as a supportive colleague alongside RCM professionals to help them process claims faster and more accurately.

Your personality:
- Friendly, knowledgeable, and experienced
- Speak like a seasoned RCM professional, not a generic AI
- Use industry terminology naturally
- Share insights from "years of experience" in RCM
- Be encouraging and solution-focused

Your expertise areas:
- Medical claims processing and assessment
- Modifier requirements and coding guidelines  
- Payer-specific policies (UHC, Aetna, BCBS, etc.)
- Denial prevention and appeals management
- ICD-10/CPT coding accuracy
- Prior authorization requirements
- Compliance with LCD/NCD guidelines

Always provide practical, actionable advice. When discussing specific claims, reference claim IDs, payers, and specific issues. Be specific about modifier requirements, coding guidelines, and payer policies.

Remember: You're not replacing human expertise - you're amplifying it. Help RCM professionals work faster and catch issues they might miss."""

@app.post("/api/chat/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Process a chat message with Alex, the RCM expert"""
    try:
        # Call Ollama with RCM context
        try:
            response = ollama.chat(
                model='llama3.2:3b',
                messages=[
                    {'role': 'system', 'content': RCM_SYSTEM_PROMPT},
                    {'role': 'user', 'content': request.message}
                ],
                stream=False
            )
            
            ai_response = response['message']['content']
            
        except Exception as ollama_error:
            logger.warning(f"Ollama error: {ollama_error}, falling back to mock response")
            # Fallback response
            ai_response = f"I understand you're asking about: '{request.message}'. As an RCM expert, I can help with claims processing, modifiers, denials, and payer policies. Could you be more specific about what you need help with?"
        
        # Create response message
        import time
        response_message = ChatMessage(
            id=str(int(time.time() * 1000)),
            content=ai_response,
            sender="ai",
            timestamp=str(int(time.time() * 1000)),
            type="text"
        )
        
        return ChatResponse(messages=[response_message])
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@app.get("/api/chat/health")
async def chat_health():
    """Check if chat service and Ollama are working"""
    try:
        # Test Ollama connection
        models = ollama.list()
        llama_available = any('llama3.2:3b' in str(model) for model in models.get('models', []))
        
        return {
            "status": "ok",
            "ollama_connected": True,
            "llama_model_available": llama_available,
            "models": [str(model) for model in models.get('models', [])]
        }
    except Exception as e:
        return {
            "status": "degraded", 
            "ollama_connected": False,
            "error": str(e),
            "fallback_available": True
        }

@app.get("/")
async def root():
    return {"message": "Chat Test API - Ready to test Llama integration with RCM context"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)