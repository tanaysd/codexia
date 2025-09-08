from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import logging
import uuid
from datetime import datetime

from ..models.core import (
    UserProfile, TrainingScenario, TrainingSession, ScenarioResult, 
    UserAction, DifficultyLevel, ActionType
)
from ..agents.scenario_generator import ScenarioGenerator
from ..agents.adaptive_coach import AdaptiveCoach

router = APIRouter(tags=["training"], prefix="/api/training")
logger = logging.getLogger(__name__)

# In-memory storage for demo (replace with database in production)
user_profiles: Dict[str, UserProfile] = {}
training_sessions: Dict[str, TrainingSession] = {}
scenario_results: Dict[str, List[ScenarioResult]] = {}

# Initialize training components
scenario_generator = ScenarioGenerator()
adaptive_coach = AdaptiveCoach()

class StartSessionRequest(BaseModel):
    user_id: str
    session_goals: List[str] = []
    preferred_difficulty: Optional[str] = None

class StartSessionResponse(BaseModel):
    session_id: str
    user_profile: UserProfile
    first_scenario: TrainingScenario

class SubmitActionRequest(BaseModel):
    session_id: str
    action_type: str
    action_details: Dict[str, Any] = {}
    confidence_level: Optional[float] = None
    time_taken_seconds: float

class SubmitActionResponse(BaseModel):
    success: bool
    hint: Optional[str] = None
    scenario_completed: bool = False
    scenario_result: Optional[ScenarioResult] = None
    next_scenario: Optional[TrainingScenario] = None
    feedback: Optional[str] = None

class GetHintRequest(BaseModel):
    session_id: str
    struggle_time: float

class GetHintResponse(BaseModel):
    hint: str
    hint_count: int

class SessionAnalyticsResponse(BaseModel):
    session_id: str
    scenarios_completed: int
    total_xp_earned: int
    average_accuracy: float
    improvement_insights: Dict[str, Any]

@router.post("/start-session", response_model=StartSessionResponse)
async def start_training_session(request: StartSessionRequest):
    """Start a new training session for a user"""
    
    try:
        # Get or create user profile
        user_profile = user_profiles.get(request.user_id)
        if not user_profile:
            user_profile = UserProfile(
                user_id=request.user_id,
                level=1,
                total_xp=350,  # Match frontend mock
                current_streak=7,  # Match frontend mock
                skill_ratings={},
                weak_areas=["modifier_issue", "dx_cpt_mismatch"],
                strong_areas=["basic_claims"],
                preferred_difficulty=DifficultyLevel(request.preferred_difficulty) if request.preferred_difficulty else DifficultyLevel.BEGINNER
            )
            user_profiles[request.user_id] = user_profile
        
        # Create new training session
        session_id = str(uuid.uuid4())
        training_session = TrainingSession(
            session_id=session_id,
            user_id=request.user_id,
            session_goals=request.session_goals,
            current_difficulty=user_profile.preferred_difficulty
        )
        
        # Generate first scenario
        first_scenario = await scenario_generator.generate_personalized_scenario(
            user_profile, user_profile.preferred_difficulty
        )
        
        training_session.current_scenario = first_scenario
        training_sessions[session_id] = training_session
        
        logger.info(f"Started training session {session_id} for user {request.user_id}")
        
        return StartSessionResponse(
            session_id=session_id,
            user_profile=user_profile,
            first_scenario=first_scenario
        )
        
    except Exception as e:
        logger.error(f"Error starting training session: {e}")
        raise HTTPException(status_code=500, detail="Failed to start training session")

@router.post("/submit-action", response_model=SubmitActionResponse)
async def submit_user_action(request: SubmitActionRequest):
    """Submit a user action during training"""
    
    try:
        session = training_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Training session not found")
        
        if not session.current_scenario:
            raise HTTPException(status_code=400, detail="No active scenario in session")
        
        user_profile = user_profiles.get(session.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Create user action
        user_action = UserAction(
            action_type=ActionType(request.action_type),
            details=request.action_details,
            confidence_level=request.confidence_level,
            time_taken_seconds=request.time_taken_seconds
        )
        
        # Check if action is correct (simplified logic)
        optimal_actions = session.current_scenario.optimal_actions
        action_correct = user_action.action_type in optimal_actions
        
        response = SubmitActionResponse(success=True)
        
        # If action is incorrect, provide hint if appropriate
        if not action_correct:
            # Check if we should offer a hint
            elapsed_time = sum([
                result.completion_time_seconds 
                for result in session.scenarios_completed
            ]) + request.time_taken_seconds
            
            should_hint = await adaptive_coach.should_offer_hint(
                session.current_scenario, elapsed_time, [user_action]
            )
            
            if should_hint:
                hint = await adaptive_coach.provide_contextual_hint(
                    session.current_scenario, user_profile, session, request.time_taken_seconds
                )
                response.hint = hint
        
        # If action is correct or max attempts reached, complete scenario
        if action_correct or len([user_action]) >= session.current_scenario.max_attempts:
            # Calculate scenario result
            accuracy_score = 1.0 if action_correct else 0.3
            scenario_result = ScenarioResult(
                scenario_id=session.current_scenario.scenario_id,
                user_id=session.user_id,
                user_actions=[user_action],
                optimal_actions=optimal_actions,
                accuracy_score=accuracy_score,
                speed_score=min(1.0, 180.0 / request.time_taken_seconds),  # Optimal time 3 minutes
                learning_score=0.8,  # Simplified
                total_xp_earned=int(50 * accuracy_score),
                completion_time_seconds=request.time_taken_seconds,
                hints_used=1 if response.hint else 0
            )
            
            # Add to session and user results
            session.scenarios_completed.append(scenario_result)
            session.total_xp_earned += scenario_result.total_xp_earned
            
            if session.user_id not in scenario_results:
                scenario_results[session.user_id] = []
            scenario_results[session.user_id].append(scenario_result)
            
            # Update user profile
            user_profile.total_xp += scenario_result.total_xp_earned
            user_profile.total_scenarios_completed += 1
            
            # Provide feedback
            feedback = await adaptive_coach.provide_post_scenario_feedback(
                session.current_scenario, scenario_result, user_profile
            )
            
            # Generate next scenario
            next_scenario = await scenario_generator.generate_personalized_scenario(
                user_profile, session.current_difficulty
            )
            
            session.current_scenario = next_scenario
            
            response.scenario_completed = True
            response.scenario_result = scenario_result
            response.next_scenario = next_scenario
            response.feedback = feedback
        
        return response
        
    except Exception as e:
        logger.error(f"Error submitting action: {e}")
        raise HTTPException(status_code=500, detail="Failed to process action")

@router.post("/get-hint", response_model=GetHintResponse)
async def get_training_hint(request: GetHintRequest):
    """Get a hint for the current scenario"""
    
    try:
        session = training_sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Training session not found")
        
        if not session.current_scenario:
            raise HTTPException(status_code=400, detail="No active scenario")
        
        user_profile = user_profiles.get(session.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Provide hint
        hint = await adaptive_coach.provide_contextual_hint(
            session.current_scenario, user_profile, session, request.struggle_time
        )
        
        # Track hint usage (simplified)
        hint_count = 1  # In real implementation, track per scenario
        
        return GetHintResponse(hint=hint, hint_count=hint_count)
        
    except Exception as e:
        logger.error(f"Error providing hint: {e}")
        raise HTTPException(status_code=500, detail="Failed to provide hint")

@router.get("/session/{session_id}/analytics", response_model=SessionAnalyticsResponse)
async def get_session_analytics(session_id: str):
    """Get analytics for a training session"""
    
    try:
        session = training_sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Training session not found")
        
        user_profile = user_profiles.get(session.user_id)
        if not user_profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        # Calculate analytics
        scenarios_completed = len(session.scenarios_completed)
        total_xp = session.total_xp_earned
        
        avg_accuracy = 0.0
        if scenarios_completed > 0:
            avg_accuracy = sum(r.accuracy_score for r in session.scenarios_completed) / scenarios_completed
        
        # Get improvement insights
        user_results = scenario_results.get(session.user_id, [])
        improvement_insights = await adaptive_coach.analyze_performance_pattern(
            user_profile, user_results[-10:]  # Last 10 results
        )
        
        return SessionAnalyticsResponse(
            session_id=session_id,
            scenarios_completed=scenarios_completed,
            total_xp_earned=total_xp,
            average_accuracy=avg_accuracy,
            improvement_insights=improvement_insights
        )
        
    except Exception as e:
        logger.error(f"Error getting session analytics: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analytics")

@router.get("/user/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """Get user's training profile"""
    
    user_profile = user_profiles.get(user_id)
    if not user_profile:
        # Create default profile
        user_profile = UserProfile(
            user_id=user_id,
            level=1,
            total_xp=350,
            current_streak=7,
            weak_areas=["modifier_issue"],
            strong_areas=["basic_claims"]
        )
        user_profiles[user_id] = user_profile
    
    return user_profile

@router.get("/user/{user_id}/achievements")
async def get_user_achievements(user_id: str):
    """Get user's achievements and progress"""
    
    # Mock achievements data (replace with real implementation)
    achievements = [
        {"name": "Modifier Master", "icon": "🏆", "unlocked": True, "unlocked_at": "2024-01-10"},
        {"name": "Speed Demon", "icon": "⚡", "unlocked": True, "unlocked_at": "2024-01-15"},
        {"name": "Policy Expert", "icon": "📚", "unlocked": False},
        {"name": "Appeal Champion", "icon": "🥇", "unlocked": False}
    ]
    
    return {"achievements": achievements}

@router.get("/leaderboard")
async def get_training_leaderboard():
    """Get training leaderboard"""
    
    # Mock leaderboard data
    leaderboard = [
        {"user_id": "user1", "name": "Alex Smith", "level": 3, "total_xp": 1250, "rank": 1},
        {"user_id": "user2", "name": "Sarah Johnson", "level": 2, "total_xp": 890, "rank": 2},
        {"user_id": "user3", "name": "Mike Chen", "level": 2, "total_xp": 750, "rank": 3}
    ]
    
    return {"leaderboard": leaderboard}

@router.get("/health")
async def training_health():
    """Health check for training system"""
    
    return {
        "status": "healthy",
        "active_sessions": len(training_sessions),
        "total_users": len(user_profiles),
        "llm_available": True
    }