import ollama
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import json

router = APIRouter(tags=["chat"], prefix="/api/chat")
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

Response types you can provide:
1. **Text responses**: Normal conversational responses for questions, explanations, advice
2. **Claim previews**: When showing multiple claims, return type "claim-preview" with data containing claims array
3. **Analysis**: When analyzing specific claims, return type "analysis" with detailed breakdown
4. **Suggestions**: When providing actionable fixes, return type "suggestion" with before/after changes

Always provide practical, actionable advice. When discussing specific claims, reference claim IDs, payers, and specific issues. Be specific about modifier requirements, coding guidelines, and payer policies.

Remember: You're not replacing human expertise - you're amplifying it. Help RCM professionals work faster and catch issues they might miss."""

def format_conversation_for_llm(conversation_history: List[ChatMessage]) -> str:
    """Convert conversation history to a format suitable for LLM"""
    formatted = []
    for msg in conversation_history:
        role = "user" if msg.sender == "user" else "assistant"
        formatted.append(f"{role}: {msg.content}")
    return "\n".join(formatted)

def determine_response_type(response_text: str, user_message: str) -> tuple[str, Optional[Dict[str, Any]]]:
    """Determine if response should be special type with structured data"""
    user_lower = user_message.lower()
    response_lower = response_text.lower()
    
    # Check for claim preview type (multiple claims mentioned)
    if ('high-risk' in user_lower or 'show' in user_lower) and 'claims' in user_lower:
        return "claim-preview", {
            "claims": [
                {"id": "CLM-1087", "risk": 85, "reason": "Modifier 59 missing", "payer": "UHC", "eta": "3m"},
                {"id": "CLM-1092", "risk": 78, "reason": "Dx/CPT mismatch", "payer": "Aetna", "eta": "5m"},
                {"id": "CLM-1095", "risk": 72, "reason": "Coverage expired", "payer": "BCBS", "eta": "4m"}
            ]
        }
    
    # Check for analysis type (specific claim mentioned)
    if 'clm-' in user_lower or 'analyze' in user_lower or 'why' in user_lower:
        return "analysis", {
            "claimId": "CLM-1001",
            "risk": 72,
            "issues": [
                {"type": "missing_modifier", "description": "Modifier 59 required for procedure 99213", "severity": "high"},
                {"type": "policy_reference", "description": "UHC-LCD-123 §3b mandates modifier for this combination", "severity": "medium"}
            ],
            "recommendation": "Add modifier 59 to procedure 99213",
            "confidence": 95
        }
    
    # Check for suggestion type (fix/correct mentioned)
    if 'fix' in user_lower or 'correct' in user_lower or 'add modifier' in user_lower:
        return "suggestion", {
            "action": "fix_applied",
            "changes": [
                {"field": "procedures[0].modifiers", "before": "[]", "after": "[\"59\"]"},
                {"field": "risk_score", "before": "72%", "after": "12%"}
            ],
            "confidence": 95,
            "reasoning": "Added modifier 59 as required by UHC-LCD-123 §3b for procedure combination"
        }
    
    return "text", None

@router.post("/message", response_model=ChatResponse)
async def chat_message(request: ChatRequest):
    """Process a chat message with Alex, the RCM expert"""
    try:
        # Format conversation history for context
        conversation_context = format_conversation_for_llm(request.conversation_history)
        
        # Prepare the full prompt with system context, conversation history, and new message
        full_prompt = f"{RCM_SYSTEM_PROMPT}\n\nConversation history:\n{conversation_context}\n\nUser: {request.message}\n\nAssistant:"
        
        # Call Ollama
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
            # Fallback to basic mock response if Ollama fails
            ai_response = "I understand you're asking about claims processing. Could you be more specific? For example, you could ask about specific claim IDs, risk levels, or payer types."
        
        # Determine response type and structure data if needed
        response_type, data = determine_response_type(ai_response, request.message)
        
        # Create response message(s)
        import time
        messages = []
        
        if response_type == "text":
            messages.append(ChatMessage(
                id=str(int(time.time() * 1000)),
                content=ai_response,
                sender="ai",
                timestamp=str(int(time.time() * 1000)),
                type="text"
            ))
        elif response_type in ["claim-preview", "analysis", "suggestion"]:
            # For special types, create two messages: text explanation + structured data
            messages.append(ChatMessage(
                id=str(int(time.time() * 1000)),
                content=ai_response,
                sender="ai", 
                timestamp=str(int(time.time() * 1000)),
                type="text"
            ))
            messages.append(ChatMessage(
                id=str(int(time.time() * 1000) + 1),
                content="",
                sender="ai",
                timestamp=str(int(time.time() * 1000)),
                type=response_type,
                data=data
            ))
        
        return ChatResponse(messages=messages)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@router.get("/health")
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