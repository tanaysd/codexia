# 🎯 Training Gym - LLM-Powered RCM Learning Platform

> **Revolutionary AI-powered training system that transforms RCM skill development**

![Training Status](https://img.shields.io/badge/status-beta-orange)
![AI Powered](https://img.shields.io/badge/AI-Llama%203.2%203B-blue)
![Local](https://img.shields.io/badge/privacy-local%20AI-green)

## 🚀 **What Makes Training Gym Revolutionary**

The Training Gym is the world's first **LLM-powered RCM learning platform** that provides:

- **🧠 Unlimited Personalized Scenarios** - AI generates custom training based on your skill level
- **💬 Real-Time AI Coaching** - Get contextual hints and explanations when you struggle  
- **📈 Adaptive Difficulty** - System learns your performance and adjusts automatically
- **🎮 Gamification** - Levels, XP, achievements, and competitive leaderboards
- **🔒 Privacy-Safe** - Runs entirely on local Llama 3.2 3B (no external API calls)

## 🎮 **Current Implementation Status**

### ✅ **Fully Functional (Beta Ready)**
- **LLM Backend** - Complete training engine powered by Llama 3.2 3B
- **Training API** - Full REST API for all training interactions
- **Scenario Generation** - AI creates unlimited personalized RCM scenarios
- **Adaptive Coaching** - Real-time hints and performance analysis
- **User Progress** - XP tracking, level progression, achievement system
- **Professional UI** - Gamified interface integrated with Codexia design

### 🚧 **In Development**
- **Frontend-Backend Integration** - Connecting UI to real API endpoints
- **Persistent Storage** - Database layer for user progress and scenarios
- **Advanced Analytics** - Detailed performance insights and trends
- **Team Features** - Collaborative training and team leaderboards

## 🏗️ **Architecture Overview**

```
┌─ Training Gym Frontend ─┐    ┌─ Training API (Port 8002) ─┐
│  • Gamified Interface   │    │  • Session Management      │
│  • Progress Tracking    │◄──►│  • Action Processing       │ 
│  • Achievement System   │    │  • Hint Generation         │
│  • Leaderboards        │    │  • Analytics Engine        │
└─────────────────────────┘    └───────────────────────────┘
                                             │
                               ┌─ LLM Training Engine ─┐
                               │  • Scenario Generator  │
                               │  • Adaptive Coach      │
                               │  • Performance Analyzer│
                               │  • Difficulty Adjuster │
                               └─ Llama 3.2 3B (Local)─┘
```

## 🚀 **Quick Start Guide**

### **Prerequisites**
```bash
# 1. Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Download Llama 3.2 3B model
ollama pull llama3.2:3b

# 3. Start Ollama server
ollama serve
```

### **Start Training Gym**
```bash
# 1. Start the training API
cd packages/backend
. .venv/bin/activate
python training_test_api.py

# 2. Access the Training Gym
# Frontend: http://localhost:5173/training
# API: http://localhost:8002
```

## 🎯 **How to Use Training Gym**

### **1. Frontend Interface**
Navigate to http://localhost:5173/training to access the gamified interface:

- **📊 Dashboard**: View your level, XP, streak, and progress
- **🎮 Scenarios**: Browse training challenges by difficulty
- **🏆 Achievements**: Track unlocked badges and milestones  
- **📈 Analytics**: Review performance trends and insights

### **2. API Interaction**
Test the backend directly via API calls:

#### **Start Training Session**
```bash
curl -X POST http://localhost:8002/api/training/start-session \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "your_username",
    "session_goals": ["practice_modifiers", "improve_speed"],
    "preferred_difficulty": "intermediate"
  }'
```

#### **Get Personalized Scenario**
The API automatically generates scenarios based on your profile:
```json
{
  "scenario_id": "uuid-generated",
  "title": "Missing Modifier 25 - UHC Claim", 
  "difficulty": "intermediate",
  "claim_data": {
    "claim_id": "CLM-2024-001",
    "procedures": [...],
    "payer": "UnitedHealthcare"
  },
  "learning_objectives": [
    "Recognize when modifier 25 is required",
    "Understand UHC-specific policies"
  ]
}
```

#### **Submit Actions & Get Feedback**
```bash
curl -X POST http://localhost:8002/api/training/submit-action \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your_session_id",
    "action_type": "correct_claim",
    "action_details": {"modifier_added": "25"},
    "time_taken_seconds": 45,
    "confidence_level": 0.8
  }'
```

#### **Get AI Hints When Struggling**
```bash
curl -X POST http://localhost:8002/api/training/get-hint \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "your_session_id", 
    "struggle_time": 120
  }'
```

## 🧠 **LLM Features Deep Dive**

### **Personalized Scenario Generation**
The AI analyzes your profile and creates custom scenarios:

```python
# User Profile Analysis
- Skill Level: Intermediate
- Weak Areas: ["modifier_requirements", "prior_auth"]
- Strong Areas: ["basic_coding", "claim_entry"]
- Recent Performance: 78% accuracy, improving

# AI-Generated Scenario
- Focus: Modifier requirements (your weak area)
- Complexity: Intermediate level
- Payer: UHC (based on your training history)
- Issues: 2-3 deliberately introduced problems
- Time Limit: Adjusted to your skill level
```

### **Real-Time Adaptive Coaching**
The AI coach provides contextual help:

```python
# Coaching Triggers
- Time struggling > 60 seconds
- Multiple incorrect attempts
- User requests hint
- Performance pattern analysis

# AI-Generated Hints
"Look at the procedures being performed. When an E/M service 
is provided with another procedure on the same day, UHC 
requires a specific modifier. What modifier separates these services?"
```

### **Performance Analysis & Difficulty Adjustment**
```python
# AI Analysis
Recent Performance:
- 5 scenarios completed
- Average accuracy: 85% 
- Average time: 3.2 minutes
- Hints used: 1.2 per scenario

# AI Recommendation  
"User shows strong improvement in modifier recognition. 
Recommend increasing difficulty to 'expert' level and 
introducing complex multi-payer scenarios."
```

## 🎮 **Gamification System**

### **XP & Leveling**
- **Base XP**: 50 points per completed scenario
- **Accuracy Bonus**: Up to 50% bonus for high accuracy
- **Speed Bonus**: Up to 25% bonus for quick completion
- **Difficulty Multiplier**: 
  - Beginner: 1.0x
  - Intermediate: 1.5x
  - Expert: 2.0x
  - Master: 3.0x

### **Achievement System**
- **🏆 Modifier Master**: Complete 10 modifier scenarios with 90%+ accuracy
- **⚡ Speed Demon**: Complete 5 scenarios under 2 minutes each
- **📚 Policy Expert**: Perfect score on 3 complex policy scenarios
- **🔥 Streak Master**: Maintain 7-day training streak

### **Leaderboards**
- **Daily/Weekly/Monthly** rankings
- **Team competitions** (coming soon)
- **Skill-specific** leaderboards (modifiers, appeals, etc.)

## 🔧 **API Reference**

### **Core Endpoints**

| Endpoint | Method | Description |
|----------|---------|-------------|
| `/api/training/start-session` | POST | Start new training session |
| `/api/training/submit-action` | POST | Submit user action, get feedback |
| `/api/training/get-hint` | POST | Request contextual AI hint |
| `/api/training/session/{id}/analytics` | GET | Get session performance analytics |
| `/api/training/user/{id}/profile` | GET | Get user progress and stats |
| `/api/training/user/{id}/achievements` | GET | Get unlocked achievements |
| `/api/training/leaderboard` | GET | Get competitive rankings |
| `/api/training/health` | GET | Check system health |

### **Data Models**

#### **UserProfile**
```python
{
  "user_id": "string",
  "level": 1,
  "total_xp": 350,
  "current_streak": 7,
  "skill_ratings": {"modifiers": 0.85, "appeals": 0.72},
  "weak_areas": ["prior_auth", "policy_interpretation"],
  "strong_areas": ["basic_coding", "claim_entry"],
  "average_accuracy": 0.78,
  "total_scenarios_completed": 23
}
```

#### **TrainingScenario**
```python
{
  "scenario_id": "uuid",
  "title": "Missing Modifier 25 Challenge",
  "difficulty": "intermediate",
  "claim_data": {...},
  "intended_issues": [...],
  "optimal_actions": ["correct_claim"],
  "learning_objectives": [...],
  "time_limit_seconds": 240
}
```

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Ollama Connection Failed**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# Restart Ollama if needed
ollama serve
```

#### **Training API Not Responding**
```bash
# Check if training API is running
curl http://localhost:8002/health

# Restart training API
cd packages/backend
python training_test_api.py
```

#### **Frontend Shows "Coming Soon" Modal**
This is expected - the frontend UI is not yet connected to the backend API. The scenarios are currently interactive via API calls only.

### **Development Mode**
```bash
# View API logs for debugging
cd packages/backend
. .venv/bin/activate
python training_test_api.py --log-level DEBUG
```

## 🚀 **Roadmap**

### **Phase 1: Core Integration** ✅ 
- [x] LLM-powered scenario generation
- [x] Adaptive coaching system
- [x] Training API endpoints
- [x] Gamification backend

### **Phase 2: Frontend Integration** 🚧
- [ ] Connect UI to training API
- [ ] Real-time progress updates
- [ ] Interactive scenario completion
- [ ] Achievement notifications

### **Phase 3: Advanced Features** 📋
- [ ] Persistent database storage
- [ ] Advanced analytics dashboard  
- [ ] Team challenges and collaboration
- [ ] Certification pathways
- [ ] Integration with main Codexia workflow

### **Phase 4: Enterprise Features** 🔮
- [ ] Multi-tenant support
- [ ] Custom scenario libraries
- [ ] Advanced reporting
- [ ] Integration with HR systems

## 💡 **Training Scenarios Examples**

### **Beginner Level**
```
Title: "Missing Modifier 59"
Difficulty: Beginner
Learning Time: 2-3 minutes
Success Rate: 95%

Scenario: UHC claim with two procedures performed on same day
Issue: Missing modifier 59 for procedure separation
Learning: When and how to apply modifier 59
```

### **Expert Level**  
```
Title: "Complex Multi-Payer Appeal"
Difficulty: Expert  
Learning Time: 8-10 minutes
Success Rate: 43%

Scenario: Denied claim requiring policy research and appeal strategy
Issues: Medical necessity, prior auth, coding complexity
Learning: Advanced appeal writing and policy interpretation
```

## 🤝 **Contributing**

Want to improve the Training Gym? Here's how:

### **Add New Scenarios**
1. Edit `training_gym/agents/scenario_generator.py`
2. Add scenario templates for new difficulty levels
3. Test with the Training API

### **Enhance AI Coaching**
1. Modify `training_gym/agents/adaptive_coach.py`
2. Improve hint generation logic
3. Add new performance analysis patterns

### **Extend Gamification**
1. Update achievement definitions
2. Add new XP calculation rules
3. Create new leaderboard categories

---

**Ready to revolutionize RCM training?** 🚀

*The Training Gym transforms Codexia from an RCM tool into an intelligent learning platform - your competitive advantage in healthcare revenue cycle management.*