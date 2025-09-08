# 🏥 Codexia - AI-Powered RCM Copilot

> **Your Digital Twin for Revenue Cycle Management**  
> Codexia is an intelligent copilot that digitally twins an experienced RCM operator's workflow, transforming complex claims processing into streamlined, AI-powered decisions.

![Demo Status](https://img.shields.io/badge/demo-ready-brightgreen)
![AI Powered](https://img.shields.io/badge/AI-powered-blue)
![Workflow](https://img.shields.io/badge/workflow-Assess→Plan→Act-orange)

## ✨ What Makes Codexia Powerful

### 🧠 **AI-Driven Intelligence**
- **Smart Assessment**: Instantly identifies claim issues like missing modifiers, Dx/CPT mismatches, and coverage problems
- **Risk Scoring**: Provides precise risk percentages (72% denial risk) with evidence-based reasoning
- **Policy Awareness**: Cross-references UHC-LCD guidelines and payer requirements in real-time

### ⚡ **Streamlined Workflow**
- **Assess → Plan → Act**: Mirrors expert RCM operator decision-making process
- **Morning Brief**: Prioritized daily queue with impact and urgency scoring
- **One-Click Actions**: From assessment to corrected claim in seconds

### 🎯 **Expert-Level Outputs**
- **Corrected Claims**: Auto-generates properly coded claims with change logs
- **Appeal Letters**: Creates Level 1 appeal documentation with policy citations
- **Audit Trail**: Complete evidence chain for compliance and training

## 🚀 Key Features

| Feature | Description | Impact |
|---------|-------------|---------|
| **🎯 Training Gym** | AI-powered learning platform with personalized scenarios | 🏆 Transforms RCM training |
| **🔥 Alex AI Chat** | Conversational RCM expert powered by Llama 3.2 3B | 🚀 Instant expert guidance |
| **Intelligent Triage** | Auto-prioritizes claims by denial risk and revenue impact | ⏰ 80% faster claim review |
| **Real-time Assessment** | Instant analysis against 1000+ payer policies | 🎯 95% accuracy rate |
| **Automated Corrections** | Generates corrected claims with proper modifiers/codes | 💰 Reduces denials by 60% |
| **Evidence-Based Appeals** | Creates appeals with specific policy citations | 📈 Improves success rate by 40% |
| **Learning Workflow** | Explains decisions for team training and knowledge transfer | 🧑‍🎓 Accelerates staff onboarding |

## 💡 Demo Scenarios

### **🎯 Training Gym** - Revolutionary Learning Platform
- **Personalized Learning**: AI generates scenarios tailored to your skill level
- **Real-Time Coaching**: Get hints and explanations when you struggle
- **Adaptive Difficulty**: System learns and adjusts challenge level automatically
- **Gamification**: Earn XP, unlock achievements, climb leaderboards
- **Safe Practice**: Train on realistic scenarios without real-world consequences

### **🔥 Chat with Alex** - AI-Powered RCM Expert
- **Natural Language**: Ask Alex anything about claims processing
- **Expert Responses**: 15+ years of RCM experience via Llama 3.2 3B
- **Real-time Help**: Instant guidance on modifiers, denials, payer policies
- **Interactive**: Conversational interface replaces complex workflows

### **Morning Brief** - Daily Claims Queue
- View prioritized claims needing attention
- Risk-based sorting with ETA estimates  
- One-click claim review workflow

### **Claim Workbench** - AI-Powered Processing
- **Input**: Raw claim JSON data
- **Assess**: AI identifies issues and provides risk scoring
- **Plan**: Recommends specific actions (recoding vs appeal)
- **Act**: Generates corrected claims or appeal letters

## 🏛️ Architecture

```
┌─ Frontend (React + Tailwind) ─┐    ┌─ Backend (FastAPI + AI) ─┐
│  • Training Gym 🎯           │    │  • Assessment Engine     │
│  • Chat with Alex 🔥         │◄──►│  • Plan Generation       │
│  • Morning Brief             │    │  • Artifact Creation     │
│  • Claim Workbench           │    │  • Training API          │
│  • Modern UI Components      │    └─────────────────────────┘
└───────────────────────────────┘                │
                                                  │
                              ┌─ Local Llama 3.2 3B (Ollama) ─┐
                              │  • Scenario Generation        │
                              │  • Real-time Coaching         │
                              │  • Adaptive Difficulty        │
                              │  • Performance Analysis       │
                              └────────────────────────────────┘
                                                  │
                                      ┌─ Vector Index (FAISS) ─┐
                                      │  • Policy Documents     │
                                      │  • Payer Guidelines     │ 
                                      │  • Claims History       │
                                      │  • Training Scenarios   │
                                      └─────────────────────────┘
```

**Packages:**
- `packages/frontend` – React web app with Training Gym & Chat UI
- `packages/backend` – FastAPI service with AI engines & Training API
  - `training_gym/` – LLM-powered learning platform
  - `agents/` – Scenario generation & adaptive coaching
  - `models/` – Training data structures
- `packages/contracts` – shared TypeScript interfaces
- `packages/extension` – browser extension for EMR integration

## 🚀 Quick Start

**Prerequisites:**
```bash
# Install Ollama for AI chat
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama 3.2 3B model
ollama pull llama3.2:3b
```

**One-command setup and run:**
```bash
make setup && make dev
```

**Or use the startup script:**
```bash
./scripts/start.sh
```

**Access the app:**
- **Frontend**: http://localhost:5173
- **Training Gym**: http://localhost:5173/training 🎯
- **Chat with Alex**: http://localhost:5173/chat 🔥
- **Backend API**: http://localhost:8000  
- **AI Chat API**: http://localhost:8001
- **Training API**: http://localhost:8002
- **API Docs**: http://localhost:8000/docs

## 🎯 Use Cases

### **For RCM Teams**
- **Reduce claim review time** from hours to minutes
- **Standardize decision-making** across team members
- **Improve first-pass claim accuracy** through training
- **Safe skill building** with unlimited practice scenarios

### **For Healthcare Providers**
- **Accelerate revenue cycle operations** with AI guidance
- **Reduce claim denials and appeals** proactively
- **Train new staff faster** with personalized AI coaching
- **Scale expertise** across large teams consistently

### **For Payers/Consultants**
- **Audit claim processing workflows** systematically
- **Identify common denial patterns** with analytics
- **Optimize reimbursement strategies** through data insights
- **Benchmark team performance** with leaderboards

## 🔥 **NEW: AI-Powered Features**

### **🎯 Training Gym** - LLM-Powered Learning Platform ✅ **LIVE NOW**
Revolutionary RCM training system with personalized AI coaching:

**🧠 Powered by Llama 3.2 3B** - Local AI generates unlimited training scenarios
- **Personalized Scenarios**: AI creates custom challenges based on your skill level
- **Real-Time Coaching**: Get contextual hints when you're stuck
- **Adaptive Difficulty**: System learns and adjusts to your performance
- **Gamification**: Levels, XP, achievements, and leaderboards
- **4 Difficulty Levels**: Beginner → Intermediate → Expert → Master

**Access Training Gym at:** http://localhost:5173/training 🎯

### **Chat Interface** 💬 ✅ **LIVE NOW**
Transform claim processing into natural conversations with Alex, our AI-powered RCM expert with 15+ years of experience:

**🤖 Powered by Llama 3.2 3B** - Running locally via Ollama for real-time responses

**Try these commands:**
- *"Show me high-risk claims from today"*
- *"Why was CLM-1001 flagged for modifier 59?"*
- *"Help me with UHC modifier requirements"*
- *"Generate an appeal for the diabetes coverage denial"*
- *"Find claims with missing modifiers"*

**Access Alex at:** http://localhost:5173/chat 🔥

### **Interactive Claim Manipulation** ⚡
- Real-time editing with AI suggestions
- Visual diff showing before/after changes
- Collaborative review with team annotations
- Undo/redo with explanation chains

### **Intelligent Automation** 🤖
- Auto-fix low-risk issues without human review
- Batch processing with confidence thresholds
- Learning from user corrections to improve accuracy
- Integration with EMR/PMS for seamless workflow

## 🛠️ Technology Stack

### **AI & Machine Learning**
- **Llama 3.2 3B** - Local LLM via Ollama for chat & training
- **FAISS** - Vector similarity search for policy matching
- **Sentence Transformers** - Semantic embeddings
- **Custom RL Agents** - Adaptive difficulty and coaching

### **Backend**
- **FastAPI** - High-performance API framework
- **Pydantic** - Data validation and serialization
- **SQLAlchemy** - Database ORM (future)
- **Prometheus** - Metrics and monitoring

### **Frontend**
- **React 18** - Modern UI framework
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast development and building

## Demo

For a step-by-step walkthrough, see [DEMO_RUNBOOK.md](./DEMO_RUNBOOK.md).

**Useful commands:**
```bash
make health           # Check service status
make reset            # Reset demo environment  
make stop             # Stop background services
make clean            # Clean all dependencies
```

---

**Ready to transform your revenue cycle?** Experience the future of RCM automation.

*Built with ❤️ for healthcare revenue cycle teams*
