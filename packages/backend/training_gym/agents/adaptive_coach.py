import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..models.core import (
    TrainingScenario, UserProfile, ScenarioResult, UserAction, 
    DifficultyLevel, TrainingSession
)
from .llm_client import LlamaTrainingClient

logger = logging.getLogger(__name__)

class AdaptiveCoach:
    """
    Provides real-time coaching, hints, and performance analysis using LLM
    """
    
    def __init__(self):
        self.llm_client = LlamaTrainingClient()
        self.hint_thresholds = {
            DifficultyLevel.BEGINNER: 45,      # Offer hint after 45 seconds
            DifficultyLevel.INTERMEDIATE: 60,  # Offer hint after 60 seconds  
            DifficultyLevel.EXPERT: 90,       # Offer hint after 90 seconds
            DifficultyLevel.MASTER: 120       # Offer hint after 2 minutes
        }
    
    async def should_offer_hint(self, scenario: TrainingScenario, time_elapsed: float, 
                              user_actions: List[UserAction]) -> bool:
        """Determine if user would benefit from a hint"""
        
        threshold = self.hint_thresholds.get(scenario.difficulty, 60)
        
        # Offer hint if user is struggling (time-based)
        if time_elapsed >= threshold:
            return True
        
        # Offer hint if user made multiple incorrect attempts
        if len(user_actions) >= 2:
            return True
        
        # Offer hint if user seems stuck (no actions for a while)
        if user_actions and time_elapsed - user_actions[-1].time_taken_seconds > 30:
            return True
        
        return False
    
    async def provide_contextual_hint(self, scenario: TrainingScenario, 
                                    user_profile: UserProfile, 
                                    current_session: TrainingSession,
                                    struggle_time: float) -> str:
        """Provide intelligent, contextual hint based on user's situation"""
        
        # Determine what the user might be struggling with
        last_action = current_session.scenarios_completed[-1].user_actions[-1] if current_session.scenarios_completed else None
        last_action_str = f"{last_action.action_type} - {last_action.details}" if last_action else "No action taken"
        
        hint = await self.llm_client.provide_hint(
            scenario, last_action_str, int(struggle_time), user_profile
        )
        
        logger.info(f"Provided hint to user {user_profile.user_id} for scenario {scenario.scenario_id}")
        return hint
    
    async def analyze_performance_pattern(self, user_profile: UserProfile, 
                                        recent_results: List[ScenarioResult]) -> Dict[str, Any]:
        """Analyze user's performance patterns and provide insights"""
        
        if not recent_results:
            return {"status": "insufficient_data", "message": "Need more scenarios for analysis"}
        
        # Calculate performance metrics
        accuracy_trend = [r.accuracy_score for r in recent_results]
        speed_trend = [r.completion_time_seconds for r in recent_results]
        hints_used = sum(r.hints_used for r in recent_results)
        
        # Identify patterns
        patterns = {
            "improving_accuracy": self._is_improving_trend(accuracy_trend),
            "consistent_speed": self._is_consistent_speed(speed_trend),
            "hint_dependency": hints_used / len(recent_results) > 1.5,
            "difficulty_appropriate": self._is_difficulty_appropriate(recent_results, user_profile)
        }
        
        # Generate insights using LLM
        adjustment_recommendation = await self.llm_client.adjust_difficulty(
            user_profile, recent_results
        )
        
        return {
            "status": "analysis_complete",
            "patterns": patterns,
            "recommendations": adjustment_recommendation,
            "next_actions": self._generate_next_actions(patterns, adjustment_recommendation)
        }
    
    async def provide_post_scenario_feedback(self, scenario: TrainingScenario, 
                                           scenario_result: ScenarioResult,
                                           user_profile: UserProfile) -> str:
        """Provide detailed feedback after scenario completion"""
        
        user_actions = [f"{action.action_type}: {action.details}" for action in scenario_result.user_actions]
        optimal_actions = [action.value for action in scenario.optimal_actions]
        
        feedback = await self.llm_client.explain_result(
            scenario, user_actions, optimal_actions, scenario_result
        )
        
        logger.info(f"Provided feedback to user {user_profile.user_id} for scenario {scenario.scenario_id}")
        return feedback
    
    def calculate_learning_velocity(self, user_profile: UserProfile, 
                                  recent_sessions: List[TrainingSession]) -> Dict[str, float]:
        """Calculate how quickly user is learning and improving"""
        
        if len(recent_sessions) < 2:
            return {"velocity": 0.0, "confidence": 0.0}
        
        # Calculate improvement over time
        session_accuracies = []
        session_speeds = []
        
        for session in recent_sessions:
            if session.scenarios_completed:
                avg_accuracy = sum(r.accuracy_score for r in session.scenarios_completed) / len(session.scenarios_completed)
                avg_speed = sum(r.completion_time_seconds for r in session.scenarios_completed) / len(session.scenarios_completed)
                session_accuracies.append(avg_accuracy)
                session_speeds.append(avg_speed)
        
        # Calculate learning velocity (improvement rate)
        if len(session_accuracies) >= 2:
            accuracy_velocity = (session_accuracies[-1] - session_accuracies[0]) / len(session_accuracies)
            speed_velocity = (session_speeds[0] - session_speeds[-1]) / len(session_speeds)  # Negative is good (faster)
            
            # Combined learning velocity
            learning_velocity = (accuracy_velocity * 0.7) + (speed_velocity * 0.3)
            
            return {
                "velocity": learning_velocity,
                "accuracy_trend": accuracy_velocity,
                "speed_trend": speed_velocity,
                "confidence": min(len(session_accuracies) / 5.0, 1.0)  # Higher confidence with more data
            }
        
        return {"velocity": 0.0, "confidence": 0.0}
    
    def identify_knowledge_gaps(self, user_profile: UserProfile, 
                               recent_results: List[ScenarioResult]) -> List[str]:
        """Identify specific areas where user needs improvement"""
        
        gaps = []
        
        # Analyze by scenario type
        scenario_performance = {}
        for result in recent_results:
            scenario_type = result.scenario_id  # In real implementation, would map to scenario type
            if scenario_type not in scenario_performance:
                scenario_performance[scenario_type] = []
            scenario_performance[scenario_type].append(result.accuracy_score)
        
        # Identify areas with consistently low performance
        for scenario_type, scores in scenario_performance.items():
            avg_score = sum(scores) / len(scores)
            if avg_score < 0.7:  # Below 70% accuracy
                gaps.append(f"low_performance_{scenario_type}")
        
        # Check for excessive hint usage
        total_hints = sum(r.hints_used for r in recent_results)
        if total_hints / len(recent_results) > 2:
            gaps.append("hint_dependency")
        
        # Check for slow completion times
        avg_time = sum(r.completion_time_seconds for r in recent_results) / len(recent_results)
        if avg_time > 240:  # More than 4 minutes average
            gaps.append("decision_speed")
        
        return gaps
    
    def recommend_learning_path(self, user_profile: UserProfile, 
                               performance_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Recommend personalized learning path based on analysis"""
        
        recommendations = {
            "immediate_focus": [],
            "skill_building": [],
            "challenge_areas": [],
            "estimated_timeline": {}
        }
        
        # Analyze patterns and recommend focus areas
        patterns = performance_analysis.get("patterns", {})
        
        if patterns.get("hint_dependency"):
            recommendations["immediate_focus"].append("independent_problem_solving")
            recommendations["estimated_timeline"]["independence"] = "2-3 weeks"
        
        if not patterns.get("improving_accuracy"):
            recommendations["immediate_focus"].append("accuracy_fundamentals")
            recommendations["estimated_timeline"]["accuracy_improvement"] = "1-2 weeks"
        
        if not patterns.get("consistent_speed"):
            recommendations["skill_building"].append("decision_making_speed")
            recommendations["estimated_timeline"]["speed_improvement"] = "3-4 weeks"
        
        # Add challenge areas based on user level
        if user_profile.level >= 2 and user_profile.average_accuracy > 0.8:
            recommendations["challenge_areas"].extend([
                "complex_multi_issue_scenarios",
                "time_pressure_training",
                "advanced_policy_interpretation"
            ])
        
        return recommendations
    
    def _is_improving_trend(self, values: List[float]) -> bool:
        """Check if values show an improving trend"""
        if len(values) < 3:
            return False
        
        # Simple trend analysis - check if recent values are higher than early values
        early_avg = sum(values[:len(values)//2]) / (len(values)//2)
        recent_avg = sum(values[len(values)//2:]) / (len(values) - len(values)//2)
        
        return recent_avg > early_avg
    
    def _is_consistent_speed(self, times: List[float]) -> bool:
        """Check if completion times are becoming more consistent"""
        if len(times) < 3:
            return False
        
        # Calculate coefficient of variation for recent times
        recent_times = times[-3:]
        avg_time = sum(recent_times) / len(recent_times)
        variance = sum((t - avg_time) ** 2 for t in recent_times) / len(recent_times)
        std_dev = variance ** 0.5
        
        # Consistent if CV < 0.3
        return (std_dev / avg_time) < 0.3 if avg_time > 0 else False
    
    def _is_difficulty_appropriate(self, results: List[ScenarioResult], 
                                 user_profile: UserProfile) -> bool:
        """Check if current difficulty level is appropriate"""
        if not results:
            return True
        
        avg_accuracy = sum(r.accuracy_score for r in results) / len(results)
        avg_hints = sum(r.hints_used for r in results) / len(results)
        
        # Difficulty is appropriate if:
        # - Accuracy is between 60-85% (challenging but achievable)
        # - Not relying too heavily on hints
        return 0.6 <= avg_accuracy <= 0.85 and avg_hints < 2
    
    def _generate_next_actions(self, patterns: Dict[str, bool], 
                             recommendations: Dict[str, Any]) -> List[str]:
        """Generate specific next actions based on analysis"""
        actions = []
        
        recommended_difficulty = recommendations.get("recommended_difficulty")
        if recommended_difficulty:
            actions.append(f"adjust_difficulty_to_{recommended_difficulty}")
        
        focus_areas = recommendations.get("focus_areas", [])
        for area in focus_areas:
            actions.append(f"practice_{area}")
        
        if patterns.get("hint_dependency"):
            actions.append("reduce_hint_usage_gradually")
        
        if not patterns.get("improving_accuracy"):
            actions.append("focus_on_fundamentals")
        
        return actions