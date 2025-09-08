from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"
    MASTER = "master"

class ScenarioType(str, Enum):
    MODIFIER_ISSUE = "modifier_issue"
    DX_CPT_MISMATCH = "dx_cpt_mismatch"
    PRIOR_AUTH = "prior_auth"
    APPEAL_WRITING = "appeal_writing"
    POLICY_INTERPRETATION = "policy_interpretation"
    TIME_PRESSURE = "time_pressure"

class ActionType(str, Enum):
    APPROVE = "approve"
    DENY = "deny"
    REQUEST_INFO = "request_info"
    CORRECT_CLAIM = "correct_claim"
    APPEAL = "appeal"

class UserProfile(BaseModel):
    user_id: str
    level: int = 1
    total_xp: int = 0
    current_streak: int = 0
    skill_ratings: Dict[str, float] = Field(default_factory=dict)
    weak_areas: List[str] = Field(default_factory=list)
    strong_areas: List[str] = Field(default_factory=list)
    preferred_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    total_scenarios_completed: int = 0
    average_accuracy: float = 0.0
    average_time_per_scenario: float = 0.0
    last_training_date: Optional[datetime] = None

class ClaimData(BaseModel):
    claim_id: str
    patient_info: Dict[str, Any]
    procedures: List[Dict[str, Any]]
    diagnoses: List[Dict[str, Any]]
    payer: str
    modifiers: List[str] = Field(default_factory=list)
    service_date: str
    provider_info: Dict[str, Any]
    additional_context: Dict[str, Any] = Field(default_factory=dict)

class TrainingScenario(BaseModel):
    scenario_id: str
    title: str
    description: str
    difficulty: DifficultyLevel
    scenario_type: ScenarioType
    claim_data: ClaimData
    intended_issues: List[Dict[str, Any]]  # Issues deliberately introduced for training
    optimal_actions: List[ActionType]
    learning_objectives: List[str]
    time_limit_seconds: Optional[int] = None
    max_attempts: int = 3
    hint_system_enabled: bool = True

class UserAction(BaseModel):
    action_type: ActionType
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence_level: Optional[float] = None  # User's self-reported confidence
    time_taken_seconds: float

class ScenarioResult(BaseModel):
    scenario_id: str
    user_id: str
    user_actions: List[UserAction]
    optimal_actions: List[ActionType]
    accuracy_score: float  # 0.0 to 1.0
    speed_score: float     # Based on time vs optimal time
    learning_score: float  # Based on improvement and understanding
    total_xp_earned: int
    hints_used: int = 0
    attempts_taken: int = 1
    completion_time_seconds: float
    feedback_provided: Optional[str] = None
    areas_for_improvement: List[str] = Field(default_factory=list)
    completed_at: datetime = Field(default_factory=datetime.now)

class TrainingSession(BaseModel):
    session_id: str
    user_id: str
    started_at: datetime = Field(default_factory=datetime.now)
    scenarios_completed: List[ScenarioResult] = Field(default_factory=list)
    current_scenario: Optional[TrainingScenario] = None
    session_goals: List[str] = Field(default_factory=list)
    current_difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    total_xp_earned: int = 0
    session_duration_seconds: float = 0
    completed_at: Optional[datetime] = None
    adaptive_adjustments_made: List[Dict[str, Any]] = Field(default_factory=list)

class Achievement(BaseModel):
    achievement_id: str
    name: str
    description: str
    icon: str
    category: str
    requirements: Dict[str, Any]
    xp_reward: int
    unlocked_at: Optional[datetime] = None

class UserAchievement(BaseModel):
    user_id: str
    achievement_id: str
    unlocked_at: datetime = Field(default_factory=datetime.now)
    progress_when_unlocked: Dict[str, Any] = Field(default_factory=dict)

class LearningPath(BaseModel):
    path_id: str
    user_id: str
    title: str
    description: str
    estimated_duration_weeks: int
    milestones: List[Dict[str, Any]]
    current_milestone: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    personalization_factors: Dict[str, Any] = Field(default_factory=dict)

class TrainingAnalytics(BaseModel):
    user_id: str
    timeframe_days: int
    scenarios_attempted: int
    scenarios_completed: int
    average_accuracy: float
    improvement_rate: float
    skill_progression: Dict[str, float]
    time_efficiency_trend: List[float]
    knowledge_gaps: List[str]
    recommended_focus_areas: List[str]
    generated_at: datetime = Field(default_factory=datetime.now)