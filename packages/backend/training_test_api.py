#!/usr/bin/env python3

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from training_gym.api.training import router as training_router
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Training Gym Test API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include training router
app.include_router(training_router)

@app.get("/")
async def root():
    return {
        "message": "Training Gym API - LLM-powered RCM training system",
        "features": [
            "Personalized scenario generation via Llama 3.2 3B",
            "Real-time adaptive coaching and hints",
            "Performance analysis and difficulty adjustment",
            "Gamification with XP, levels, and achievements"
        ],
        "endpoints": {
            "start_session": "/api/training/start-session",
            "submit_action": "/api/training/submit-action", 
            "get_hint": "/api/training/get-hint",
            "analytics": "/api/training/session/{session_id}/analytics",
            "profile": "/api/training/user/{user_id}/profile",
            "achievements": "/api/training/user/{user_id}/achievements",
            "leaderboard": "/api/training/leaderboard"
        }
    }

@app.get("/api/training/demo-scenario")
async def get_demo_scenario():
    """Get a demo scenario for testing"""
    return {
        "scenario": {
            "scenario_id": "demo-001",
            "title": "Missing Modifier 25 - UHC Claim",
            "description": "A UHC claim needs modifier 25 for E/M service with procedure",
            "difficulty": "beginner", 
            "claim_data": {
                "claim_id": "CLM-2024-001",
                "patient_info": {
                    "name": "John Smith",
                    "dob": "1975-03-15",
                    "member_id": "UHC123456"
                },
                "procedures": [
                    {
                        "cpt_code": "99213", 
                        "description": "Office visit - Level 3",
                        "modifiers": [],
                        "units": 1
                    },
                    {
                        "cpt_code": "12001",
                        "description": "Simple repair 2.5cm", 
                        "modifiers": [],
                        "units": 1
                    }
                ],
                "diagnoses": [
                    {
                        "icd10_code": "S01.01XA",
                        "description": "Laceration scalp initial"
                    }
                ],
                "payer": "UnitedHealthcare",
                "service_date": "2024-01-15",
                "provider_info": {
                    "npi": "1234567890",
                    "name": "Dr. Sarah Johnson"
                }
            },
            "learning_objectives": [
                "Recognize when modifier 25 is required",
                "Understand E/M service documentation requirements"
            ],
            "time_limit_seconds": 180
        },
        "hint": "Look at the procedures being performed. When an E/M service is performed with another procedure, what modifier might be needed?",
        "explanation": "This scenario tests knowledge of modifier 25, which is required when an E/M service is performed with another procedure on the same day."
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)