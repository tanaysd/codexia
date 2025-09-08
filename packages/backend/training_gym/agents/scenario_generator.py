import uuid
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..models.core import (
    TrainingScenario, UserProfile, DifficultyLevel, ScenarioType, 
    ClaimData, ActionType
)
from .llm_client import LlamaTrainingClient

logger = logging.getLogger(__name__)

class ScenarioGenerator:
    """
    Generates personalized training scenarios using LLM and predefined templates
    """
    
    def __init__(self):
        self.llm_client = LlamaTrainingClient()
        self.scenario_templates = self._load_scenario_templates()
    
    async def generate_personalized_scenario(self, user_profile: UserProfile, 
                                           difficulty: Optional[DifficultyLevel] = None,
                                           focus_area: Optional[str] = None) -> TrainingScenario:
        """Generate a scenario tailored to the user's needs and skill level"""
        
        # Determine difficulty and focus area if not specified
        if difficulty is None:
            difficulty = self._determine_optimal_difficulty(user_profile)
        
        if focus_area is None:
            focus_area = self._determine_focus_area(user_profile)
        
        try:
            # Use LLM to generate scenario
            scenario_data = await self.llm_client.generate_scenario(
                user_profile, difficulty, focus_area
            )
            
            # Convert to TrainingScenario object
            scenario = self._build_training_scenario(scenario_data, difficulty, focus_area)
            
            logger.info(f"Generated personalized scenario {scenario.scenario_id} for user {user_profile.user_id}")
            return scenario
            
        except Exception as e:
            logger.error(f"Error generating personalized scenario: {e}")
            # Fallback to template-based generation
            return self._generate_template_scenario(user_profile, difficulty, focus_area)
    
    def _determine_optimal_difficulty(self, user_profile: UserProfile) -> DifficultyLevel:
        """Determine optimal difficulty based on user performance"""
        
        if user_profile.total_scenarios_completed < 5:
            return DifficultyLevel.BEGINNER
        
        accuracy = user_profile.average_accuracy
        level = user_profile.level
        
        if accuracy >= 0.9 and level >= 3:
            return DifficultyLevel.EXPERT
        elif accuracy >= 0.8 and level >= 2:
            return DifficultyLevel.INTERMEDIATE
        elif accuracy >= 0.85 and level >= 4:
            return DifficultyLevel.MASTER
        else:
            return DifficultyLevel.BEGINNER
    
    def _determine_focus_area(self, user_profile: UserProfile) -> str:
        """Determine what area the user should focus on"""
        
        # Prioritize weak areas
        if user_profile.weak_areas:
            return user_profile.weak_areas[0]
        
        # If no weak areas identified, rotate through common areas
        common_focus_areas = [
            "modifier_issue",
            "dx_cpt_mismatch", 
            "prior_auth",
            "policy_interpretation"
        ]
        
        # Use scenario count to rotate focus areas
        area_index = user_profile.total_scenarios_completed % len(common_focus_areas)
        return common_focus_areas[area_index]
    
    def _build_training_scenario(self, scenario_data: Dict[str, Any], 
                               difficulty: DifficultyLevel, focus_area: str) -> TrainingScenario:
        """Build TrainingScenario object from LLM-generated data"""
        
        scenario_id = str(uuid.uuid4())
        
        # Build ClaimData object
        claim_info = scenario_data.get("claim_data", {})
        claim_data = ClaimData(
            claim_id=claim_info.get("claim_id", f"CLM-{scenario_id[:8]}"),
            patient_info=claim_info.get("patient_info", {}),
            procedures=claim_info.get("procedures", []),
            diagnoses=claim_info.get("diagnoses", []),
            payer=claim_info.get("payer", "Unknown Payer"),
            modifiers=claim_info.get("modifiers", []),
            service_date=claim_info.get("service_date", "2024-01-15"),
            provider_info=claim_info.get("provider_info", {}),
            additional_context=claim_info.get("additional_context", {})
        )
        
        # Convert action strings to ActionType enums
        optimal_actions = []
        for action_str in scenario_data.get("optimal_actions", ["correct_claim"]):
            try:
                optimal_actions.append(ActionType(action_str.lower()))
            except ValueError:
                optimal_actions.append(ActionType.CORRECT_CLAIM)
        
        # Determine scenario type from focus area
        scenario_type = self._focus_area_to_scenario_type(focus_area)
        
        return TrainingScenario(
            scenario_id=scenario_id,
            title=scenario_data.get("title", f"{difficulty.value.title()} Training Challenge"),
            description=scenario_data.get("description", "Practice your RCM skills"),
            difficulty=difficulty,
            scenario_type=scenario_type,
            claim_data=claim_data,
            intended_issues=scenario_data.get("intended_issues", []),
            optimal_actions=optimal_actions,
            learning_objectives=scenario_data.get("learning_objectives", []),
            time_limit_seconds=scenario_data.get("time_limit_seconds", 300),
            max_attempts=3,
            hint_system_enabled=True
        )
    
    def _focus_area_to_scenario_type(self, focus_area: str) -> ScenarioType:
        """Convert focus area string to ScenarioType enum"""
        focus_to_type_map = {
            "modifier_issue": ScenarioType.MODIFIER_ISSUE,
            "dx_cpt_mismatch": ScenarioType.DX_CPT_MISMATCH,
            "prior_auth": ScenarioType.PRIOR_AUTH,
            "appeal_writing": ScenarioType.APPEAL_WRITING,
            "policy_interpretation": ScenarioType.POLICY_INTERPRETATION,
            "time_pressure": ScenarioType.TIME_PRESSURE
        }
        return focus_to_type_map.get(focus_area, ScenarioType.MODIFIER_ISSUE)
    
    def _generate_template_scenario(self, user_profile: UserProfile, 
                                  difficulty: DifficultyLevel, focus_area: str) -> TrainingScenario:
        """Fallback template-based scenario generation"""
        
        scenario_id = str(uuid.uuid4())
        
        # Get template based on difficulty and focus area
        template = self.scenario_templates.get(f"{difficulty.value}_{focus_area}", 
                                             self.scenario_templates.get("default"))
        
        # Customize template for user
        claim_data = ClaimData(
            claim_id=f"CLM-{scenario_id[:8]}",
            patient_info=template["patient_info"],
            procedures=template["procedures"],
            diagnoses=template["diagnoses"],
            payer=template["payer"],
            modifiers=template.get("modifiers", []),
            service_date="2024-01-15",
            provider_info=template["provider_info"]
        )
        
        return TrainingScenario(
            scenario_id=scenario_id,
            title=template["title"],
            description=template["description"],
            difficulty=difficulty,
            scenario_type=self._focus_area_to_scenario_type(focus_area),
            claim_data=claim_data,
            intended_issues=template["intended_issues"],
            optimal_actions=[ActionType(action) for action in template["optimal_actions"]],
            learning_objectives=template["learning_objectives"],
            time_limit_seconds=template.get("time_limit_seconds", 300)
        )
    
    def _load_scenario_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined scenario templates for fallback"""
        return {
            "beginner_modifier_issue": {
                "title": "Missing Modifier 25 - Office Visit",
                "description": "UHC claim needs modifier 25 for E/M service with procedure",
                "patient_info": {"name": "John Smith", "dob": "1975-03-15", "member_id": "UHC123456"},
                "procedures": [
                    {"cpt_code": "99213", "description": "Office visit - Level 3", "modifiers": [], "units": 1},
                    {"cpt_code": "12001", "description": "Simple repair 2.5cm", "modifiers": [], "units": 1}
                ],
                "diagnoses": [{"icd10_code": "S01.01XA", "description": "Laceration scalp initial"}],
                "payer": "UnitedHealthcare",
                "provider_info": {"npi": "1234567890", "name": "Dr. Sarah Johnson"},
                "intended_issues": [
                    {"type": "missing_modifier", "description": "Modifier 25 required for E/M with procedure", "severity": "high"}
                ],
                "optimal_actions": ["correct_claim"],
                "learning_objectives": [
                    "Recognize when modifier 25 is required",
                    "Understand E/M service documentation requirements"
                ],
                "time_limit_seconds": 180
            },
            "intermediate_dx_cpt_mismatch": {
                "title": "Diagnosis Support Issue - Aetna",
                "description": "Aetna claim with diagnosis that doesn't support procedure medical necessity",
                "patient_info": {"name": "Maria Garcia", "dob": "1982-07-22", "member_id": "AET789012"},
                "procedures": [{"cpt_code": "93000", "description": "Electrocardiogram", "modifiers": [], "units": 1}],
                "diagnoses": [{"icd10_code": "Z00.00", "description": "General adult medical examination"}],
                "payer": "Aetna",
                "provider_info": {"npi": "2345678901", "name": "Dr. Michael Chen"},
                "intended_issues": [
                    {"type": "medical_necessity", "description": "EKG not medically necessary for routine exam", "severity": "high"}
                ],
                "optimal_actions": ["request_info"],
                "learning_objectives": [
                    "Identify medical necessity requirements",
                    "Understand Aetna's coverage policies"
                ],
                "time_limit_seconds": 240
            },
            "default": {
                "title": "RCM Training Challenge",
                "description": "General RCM scenario for skill building",
                "patient_info": {"name": "Test Patient", "dob": "1980-01-01", "member_id": "TEST123"},
                "procedures": [{"cpt_code": "99213", "description": "Office visit", "modifiers": [], "units": 1}],
                "diagnoses": [{"icd10_code": "Z00.00", "description": "General examination"}],
                "payer": "Generic Insurance",
                "provider_info": {"npi": "1234567890", "name": "Dr. Test"},
                "intended_issues": [
                    {"type": "general", "description": "Practice RCM skills", "severity": "medium"}
                ],
                "optimal_actions": ["correct_claim"],
                "learning_objectives": ["Practice general RCM skills"],
                "time_limit_seconds": 300
            }
        }