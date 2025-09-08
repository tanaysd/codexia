import ollama
import json
import logging
from typing import Dict, Any, Optional, List
from ..models.core import TrainingScenario, UserProfile, ScenarioResult, DifficultyLevel

logger = logging.getLogger(__name__)

class LlamaTrainingClient:
    """
    LLM client specifically designed for training gym interactions
    """
    
    def __init__(self, model: str = "llama3.2:3b"):
        self.model = model
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        return """You are Alex, an AI-powered Revenue Cycle Management (RCM) expert with over 15 years of experience in medical claims processing, denial management, and healthcare revenue optimization. 

In the Training Gym context, you serve as:
1. An intelligent scenario generator creating realistic RCM training scenarios
2. A coaching assistant providing real-time hints and explanations
3. A performance analyst offering personalized feedback and insights
4. An adaptive learning guide adjusting difficulty and focus areas

Key principles:
- Always maintain RCM expertise and professional tone
- Provide educational explanations that build understanding
- Be encouraging while maintaining accuracy
- Reference specific policies, modifiers, and payer requirements
- Focus on practical, real-world application
- Generate realistic claim data and scenarios
- Adapt responses to user's experience level and needs

Remember: RCM = Revenue Cycle Management (healthcare billing), not refrigeration."""

    async def generate_scenario(self, user_profile: UserProfile, difficulty: DifficultyLevel, 
                              focus_area: str) -> Dict[str, Any]:
        """Generate a personalized training scenario"""
        
        prompt = f"""
        Generate a realistic RCM training scenario with the following requirements:

        User Profile:
        - Experience Level: {user_profile.level}
        - Weak Areas: {user_profile.weak_areas}
        - Strong Areas: {user_profile.strong_areas}
        - Average Accuracy: {user_profile.average_accuracy:.2f}
        - Total Scenarios Completed: {user_profile.total_scenarios_completed}

        Scenario Requirements:
        - Difficulty: {difficulty.value}
        - Focus Area: {focus_area}
        - Should challenge their weak areas while building confidence
        - Include 2-3 deliberate issues for them to identify and resolve

        Generate a JSON response with this exact structure:
        {{
            "title": "Descriptive scenario title",
            "description": "Brief scenario description for the user",
            "claim_data": {{
                "claim_id": "CLM-XXXX",
                "patient_info": {{"name": "Patient Name", "dob": "YYYY-MM-DD", "member_id": "12345"}},
                "procedures": [{{"cpt_code": "99213", "description": "Office visit", "modifiers": [], "units": 1}}],
                "diagnoses": [{{"icd10_code": "Z00.00", "description": "Encounter for examination"}}],
                "payer": "Insurance Company Name",
                "service_date": "2024-01-15",
                "provider_info": {{"npi": "1234567890", "name": "Dr. Smith"}}
            }},
            "intended_issues": [
                {{"type": "missing_modifier", "description": "Modifier 25 required for E/M with procedure", "severity": "high"}},
                {{"type": "dx_support", "description": "Diagnosis doesn't support medical necessity", "severity": "medium"}}
            ],
            "optimal_actions": ["correct_claim"],
            "learning_objectives": [
                "Recognize when modifier 25 is required",
                "Identify medical necessity issues"
            ],
            "time_limit_seconds": 300
        }}

        Ensure all medical codes and scenarios are realistic and educational.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=False
            )
            
            content = response['message']['content']
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_content = content[start_idx:end_idx]
                return json.loads(json_content)
            else:
                logger.error("Could not extract JSON from LLM response")
                return self._fallback_scenario(difficulty, focus_area)
                
        except Exception as e:
            logger.error(f"Error generating scenario: {e}")
            return self._fallback_scenario(difficulty, focus_area)
    
    async def provide_hint(self, scenario: TrainingScenario, user_action: str, 
                          struggle_time: int, user_profile: UserProfile) -> str:
        """Provide contextual hint during training"""
        
        prompt = f"""
        The user is working on this RCM training scenario and needs a helpful hint:

        Scenario: {scenario.title}
        Description: {scenario.description}
        Claim Data: {scenario.claim_data.dict()}
        Focus Area: {scenario.scenario_type}
        
        User Status:
        - Experience Level: {user_profile.level}
        - Time struggling: {struggle_time} seconds
        - Last action attempted: {user_action}
        
        Provide a helpful hint that:
        1. Guides them toward the solution without giving it away
        2. Is educational and builds understanding
        3. References specific RCM knowledge
        4. Is encouraging and supportive
        5. Matches their experience level
        
        Keep the hint concise (2-3 sentences) and actionable.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=False
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error providing hint: {e}")
            return "Take a closer look at the claim details. What requirements might this payer have for this type of service?"
    
    async def explain_result(self, scenario: TrainingScenario, user_actions: List[str], 
                           optimal_actions: List[str], scenario_result: ScenarioResult) -> str:
        """Provide detailed explanation after scenario completion"""
        
        prompt = f"""
        Provide educational feedback on this completed RCM training scenario:

        Scenario: {scenario.title}
        Difficulty: {scenario.difficulty}
        Learning Objectives: {scenario.learning_objectives}
        
        User Performance:
        - Actions Taken: {user_actions}
        - Optimal Actions: {optimal_actions}
        - Accuracy Score: {scenario_result.accuracy_score:.2f}
        - Time Taken: {scenario_result.completion_time_seconds:.1f}s
        - Hints Used: {scenario_result.hints_used}
        
        Provide feedback that:
        1. Explains why the optimal actions were correct
        2. Identifies what the user did well
        3. Points out areas for improvement
        4. Provides specific RCM knowledge for future scenarios
        5. Is encouraging and builds confidence
        
        Format as friendly, expert guidance from an experienced RCM professional.
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=False
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error explaining result: {e}")
            return "Great work on completing this scenario! Each challenge helps build your RCM expertise."
    
    async def adjust_difficulty(self, user_profile: UserProfile, 
                              recent_results: List[ScenarioResult]) -> Dict[str, Any]:
        """Analyze performance and recommend difficulty adjustments"""
        
        # Calculate recent performance metrics
        if not recent_results:
            return {"recommended_difficulty": user_profile.preferred_difficulty, "reasoning": "No recent data"}
        
        avg_accuracy = sum(r.accuracy_score for r in recent_results) / len(recent_results)
        avg_time = sum(r.completion_time_seconds for r in recent_results) / len(recent_results)
        total_hints = sum(r.hints_used for r in recent_results)
        
        prompt = f"""
        Analyze this user's recent RCM training performance and recommend difficulty adjustments:

        User Profile:
        - Current Level: {user_profile.level}
        - Total XP: {user_profile.total_xp}
        - Current Difficulty: {user_profile.preferred_difficulty}
        - Historical Accuracy: {user_profile.average_accuracy:.2f}
        
        Recent Performance ({len(recent_results)} scenarios):
        - Average Accuracy: {avg_accuracy:.2f}
        - Average Time: {avg_time:.1f} seconds
        - Total Hints Used: {total_hints}
        - Improvement Trend: {"improving" if avg_accuracy > user_profile.average_accuracy else "declining"}
        
        Recommend:
        1. Should difficulty increase, decrease, or stay the same?
        2. What specific areas need focus?
        3. What type of scenarios would be most beneficial?
        
        Provide JSON response:
        {{
            "recommended_difficulty": "beginner|intermediate|expert|master",
            "reasoning": "Brief explanation of recommendation",
            "focus_areas": ["area1", "area2"],
            "confidence_level": 0.8
        }}
        """
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': prompt}
                ],
                stream=False
            )
            
            content = response['message']['content']
            
            # Extract JSON from response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            
            if start_idx >= 0 and end_idx > start_idx:
                json_content = content[start_idx:end_idx]
                return json.loads(json_content)
            else:
                return {
                    "recommended_difficulty": user_profile.preferred_difficulty,
                    "reasoning": "Maintaining current difficulty level",
                    "focus_areas": user_profile.weak_areas[:2] if user_profile.weak_areas else ["modifiers"],
                    "confidence_level": 0.5
                }
                
        except Exception as e:
            logger.error(f"Error adjusting difficulty: {e}")
            return {
                "recommended_difficulty": user_profile.preferred_difficulty,
                "reasoning": "Error in analysis, maintaining current level",
                "focus_areas": user_profile.weak_areas[:2] if user_profile.weak_areas else ["modifiers"],
                "confidence_level": 0.3
            }
    
    def _fallback_scenario(self, difficulty: DifficultyLevel, focus_area: str) -> Dict[str, Any]:
        """Fallback scenario when LLM generation fails"""
        return {
            "title": f"{difficulty.value.title()} {focus_area.replace('_', ' ').title()} Challenge",
            "description": f"Practice your {focus_area.replace('_', ' ')} skills with this scenario",
            "claim_data": {
                "claim_id": "CLM-9999",
                "patient_info": {"name": "Test Patient", "dob": "1980-01-01", "member_id": "TEST123"},
                "procedures": [{"cpt_code": "99213", "description": "Office visit", "modifiers": [], "units": 1}],
                "diagnoses": [{"icd10_code": "Z00.00", "description": "General examination"}],
                "payer": "Test Insurance",
                "service_date": "2024-01-15",
                "provider_info": {"npi": "1234567890", "name": "Dr. Test"}
            },
            "intended_issues": [
                {"type": focus_area, "description": f"Practice {focus_area} identification", "severity": "medium"}
            ],
            "optimal_actions": ["correct_claim"],
            "learning_objectives": [f"Practice {focus_area.replace('_', ' ')} skills"],
            "time_limit_seconds": 300
        }