import React, { useState } from "react";
import { Target, Trophy, Zap, Clock, Star, ChevronRight, Play, CheckCircle } from "lucide-react";

export function TrainingGymPage() {
  const [selectedScenario, setSelectedScenario] = useState<number | null>(null);
  const [userLevel, setUserLevel] = useState(1);
  const [userXP, setUserXP] = useState(350);
  const [streak, setStreak] = useState(7);

  const scenarios = [
    {
      id: 1,
      title: "Missing Modifier 59",
      difficulty: "Beginner",
      xp: 50,
      time: "2 min",
      description: "UHC claim CLM-2001 needs modifier 59 for procedure combination",
      successRate: 95,
      color: "green"
    },
    {
      id: 2,
      title: "Dx/CPT Mismatch Challenge",
      difficulty: "Intermediate", 
      xp: 100,
      time: "5 min",
      description: "Aetna claim with diagnosis code that doesn't support the procedure",
      successRate: 72,
      color: "yellow"
    },
    {
      id: 3,
      title: "Complex Appeal Scenario",
      difficulty: "Expert",
      xp: 200,
      time: "10 min", 
      description: "Multi-layer BCBS denial requiring policy research and appeal strategy",
      successRate: 43,
      color: "red"
    },
    {
      id: 4,
      title: "High-Pressure Crisis Mode",
      difficulty: "Master",
      xp: 300,
      time: "3 min",
      description: "Time-critical $50K claim with multiple issues - can you save it?",
      successRate: 28,
      color: "purple"
    }
  ];

  const achievements = [
    { name: "Modifier Master", icon: "🏆", unlocked: true },
    { name: "Speed Demon", icon: "⚡", unlocked: true },
    { name: "Policy Expert", icon: "📚", unlocked: false },
    { name: "Appeal Champion", icon: "🥇", unlocked: false },
  ];

  const getDifficultyColor = (difficulty: string) => {
    switch(difficulty) {
      case "Beginner": return "bg-green-100 text-green-700";
      case "Intermediate": return "bg-yellow-100 text-yellow-700"; 
      case "Expert": return "bg-red-100 text-red-700";
      case "Master": return "bg-purple-100 text-purple-700";
      default: return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">🎯 Training Gym</h1>
            <p className="text-gray-600">Master RCM skills in a safe practice environment</p>
          </div>
          
          {/* User Stats */}
          <div className="flex items-center gap-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">Level {userLevel}</div>
              <div className="text-sm text-gray-500">{userXP}/500 XP</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-orange-600">{streak}</div>
              <div className="text-sm text-gray-500">Day Streak</div>
            </div>
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <Target className="w-8 h-8 text-white" />
            </div>
          </div>
        </div>
        
        {/* XP Progress Bar */}
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div className="bg-blue-600 h-2 rounded-full transition-all duration-300" style={{width: `${(userXP/500)*100}%`}}></div>
          </div>
        </div>
      </div>

      <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Training Scenarios */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <Play className="w-5 h-5 text-blue-600" />
              Training Scenarios
            </h2>
            
            <div className="space-y-4">
              {scenarios.map((scenario) => (
                <div key={scenario.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                     onClick={() => setSelectedScenario(scenario.id)}>
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-semibold text-gray-900">{scenario.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(scenario.difficulty)}`}>
                          {scenario.difficulty}
                        </span>
                      </div>
                      <p className="text-gray-600 text-sm mb-3">{scenario.description}</p>
                      
                      <div className="flex items-center gap-4 text-sm text-gray-500">
                        <div className="flex items-center gap-1">
                          <Star className="w-4 h-4" />
                          {scenario.xp} XP
                        </div>
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {scenario.time}
                        </div>
                        <div className="flex items-center gap-1">
                          <Trophy className="w-4 h-4" />
                          {scenario.successRate}% success rate
                        </div>
                      </div>
                    </div>
                    
                    <ChevronRight className="w-5 h-5 text-gray-400" />
                  </div>
                </div>
              ))}
            </div>
            
            {/* Coming Soon */}
            <div className="mt-6 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
              <div className="flex items-center gap-3">
                <Zap className="w-5 h-5 text-blue-600" />
                <div>
                  <h4 className="font-medium text-blue-900">🚀 Enhanced Training Coming Soon!</h4>
                  <p className="text-blue-700 text-sm">Real-time feedback, adaptive difficulty, and AI-powered scenario generation</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Achievements */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Trophy className="w-5 h-5 text-yellow-600" />
              Achievements
            </h3>
            
            <div className="grid grid-cols-2 gap-3">
              {achievements.map((achievement, idx) => (
                <div key={idx} className={`p-3 rounded-lg border text-center ${achievement.unlocked ? 'bg-yellow-50 border-yellow-200' : 'bg-gray-50 border-gray-200'}`}>
                  <div className="text-2xl mb-1">{achievement.icon}</div>
                  <div className={`text-xs font-medium ${achievement.unlocked ? 'text-yellow-700' : 'text-gray-500'}`}>
                    {achievement.name}
                  </div>
                  {achievement.unlocked && <CheckCircle className="w-3 h-3 text-yellow-600 mx-auto mt-1" />}
                </div>
              ))}
            </div>
          </div>

          {/* Today's Challenge */}
          <div className="bg-gradient-to-br from-purple-500 to-indigo-600 rounded-lg p-6 text-white">
            <h3 className="text-lg font-semibold mb-2">🎯 Daily Challenge</h3>
            <p className="text-purple-100 text-sm mb-4">Complete 3 intermediate scenarios to earn bonus XP</p>
            
            <div className="bg-white bg-opacity-20 rounded-lg p-3">
              <div className="flex items-center justify-between text-sm">
                <span>Progress</span>
                <span>1/3 completed</span>
              </div>
              <div className="w-full bg-white bg-opacity-30 rounded-full h-2 mt-2">
                <div className="bg-white h-2 rounded-full" style={{width: '33%'}}></div>
              </div>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <h3 className="text-lg font-semibold mb-4">📊 Your Stats</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Scenarios Completed</span>
                <span className="font-medium">47</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Average Score</span>
                <span className="font-medium">87%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Time Saved</span>
                <span className="font-medium">2.3 hrs</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Favorite Skill</span>
                <span className="font-medium">Modifiers</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Selected Scenario Modal */}
      {selectedScenario && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold">Ready to Start Training?</h2>
              <button onClick={() => setSelectedScenario(null)} className="text-gray-400 hover:text-gray-600">✕</button>
            </div>
            
            <div className="mb-6">
              <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                <h3 className="font-medium text-blue-900 mb-2">🚧 Feature in Development</h3>
                <p className="text-blue-700 text-sm">
                  The Training Gym is currently being built! This mockup shows the planned interface. 
                  Soon you'll be able to practice real RCM scenarios with:
                </p>
                <ul className="list-disc list-inside text-blue-700 text-sm mt-2 space-y-1">
                  <li>Interactive claim scenarios</li>
                  <li>Real-time feedback from Alex AI</li>
                  <li>Adaptive difficulty based on performance</li>
                  <li>Progress tracking and achievements</li>
                </ul>
              </div>
            </div>
            
            <div className="flex gap-3">
              <button 
                onClick={() => setSelectedScenario(null)}
                className="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                Close Preview
              </button>
              <button 
                disabled
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg opacity-50 cursor-not-allowed"
              >
                Start Training (Coming Soon)
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}