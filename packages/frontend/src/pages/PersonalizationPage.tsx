import React from "react";
import { Brain, TrendingUp, Clock, Target, Award, AlertCircle, CheckCircle, Calendar } from "lucide-react";

export function PersonalizationPage() {
  const currentUser = "Sarah Chen"; // Mock user
  const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <Brain className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-900">AI Insights</h1>
          </div>
          <p className="text-gray-600">Personalized productivity insights powered by your work patterns</p>
        </div>

        {/* Productivity Forecast Alert */}
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-lg p-6 mb-8">
          <div className="flex items-start gap-4">
            <TrendingUp className="w-6 h-6 text-green-600 mt-1" />
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                🚀 Productivity Forecast: +25% Efficiency Today
              </h3>
              <p className="text-gray-700 mb-4">
                Based on your work patterns from last week, following this optimized sequence will boost your productivity:
              </p>
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4 border border-green-200">
                  <div className="font-medium text-gray-900">1. High-Risk Claims (9:00-10:30am)</div>
                  <div className="text-sm text-gray-600">Your peak accuracy window</div>
                </div>
                <div className="bg-white rounded-lg p-4 border border-green-200">
                  <div className="font-medium text-gray-900">2. Batch Modifier Fixes (10:45-11:30am)</div>
                  <div className="text-sm text-gray-600">30% faster when grouped</div>
                </div>
                <div className="bg-white rounded-lg p-4 border border-green-200">
                  <div className="font-medium text-gray-900">3. Appeals & Documentation (2:00-4:00pm)</div>
                  <div className="text-sm text-gray-600">Afternoon focus optimal</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Work Pattern Analysis */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900">Your Work Patterns</h3>
            </div>
            <div className="space-y-4">
              <div className="border-l-4 border-green-500 pl-4">
                <div className="font-medium text-gray-900">Peak Performance: 9:00-11:00 AM</div>
                <div className="text-sm text-gray-600">95% accuracy rate • 40% faster processing</div>
              </div>
              <div className="border-l-4 border-blue-500 pl-4">
                <div className="font-medium text-gray-900">Specialty: Complex Appeals</div>
                <div className="text-sm text-gray-600">60% above team average • 12min avg resolution</div>
              </div>
              <div className="border-l-4 border-orange-500 pl-4">
                <div className="font-medium text-gray-900">Focus Area: Modifier Issues</div>
                <div className="text-sm text-gray-600">Catches 85% others miss • Top performer</div>
              </div>
              <div className="border-l-4 border-purple-500 pl-4">
                <div className="font-medium text-gray-900">Optimal Break: After 45 minutes</div>
                <div className="text-sm text-gray-600">Maintains accuracy • Prevents fatigue</div>
              </div>
            </div>
          </div>

          {/* Performance Metrics */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Award className="w-5 h-5 text-yellow-600" />
              <h3 className="text-lg font-semibold text-gray-900">This Week's Performance</h3>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-700">2.1%</div>
                <div className="text-sm text-gray-600">Denial Rate</div>
                <div className="text-xs text-green-600">vs 4.3% team avg</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-700">8.4min</div>
                <div className="text-sm text-gray-600">Avg Processing</div>
                <div className="text-xs text-blue-600">vs 12.1min team avg</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-700">47</div>
                <div className="text-sm text-gray-600">Claims Today</div>
                <div className="text-xs text-purple-600">+18% from yesterday</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-2xl font-bold text-orange-700">$142K</div>
                <div className="text-sm text-gray-600">Revenue Saved</div>
                <div className="text-xs text-orange-600">This week</div>
              </div>
            </div>
          </div>

          {/* AI Recommendations */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Target className="w-5 h-5 text-red-600" />
              <h3 className="text-lg font-semibold text-gray-900">Smart Recommendations</h3>
            </div>
            <div className="space-y-3">
              <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-blue-600 mt-0.5" />
                <div>
                  <div className="font-medium text-gray-900">Batch UHC Claims Together</div>
                  <div className="text-sm text-gray-600">You're 30% faster when processing similar payer types consecutively</div>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
                <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                <div>
                  <div className="font-medium text-gray-900">Focus on Modifier 59 Cases</div>
                  <div className="text-sm text-gray-600">Your expertise area - 15 cases waiting in queue</div>
                </div>
              </div>
              <div className="flex items-start gap-3 p-3 bg-yellow-50 rounded-lg">
                <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5" />
                <div>
                  <div className="font-medium text-gray-900">ICD-10 Update Training</div>
                  <div className="text-sm text-gray-600">New Q1 guidelines affect 23% of your claim types</div>
                </div>
              </div>
            </div>
          </div>

          {/* Personalized Queue */}
          <div className="bg-white rounded-lg border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-4">
              <Calendar className="w-5 h-5 text-green-600" />
              <h3 className="text-lg font-semibold text-gray-900">Your Optimized Queue</h3>
            </div>
            <div className="text-sm text-gray-600 mb-4">
              Prioritized based on your strengths and current time ({currentTime})
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">CLM-1087 • High Priority</div>
                  <div className="text-sm text-gray-600">Modifier 59 missing • UHC • Your specialty</div>
                </div>
                <span className="px-2 py-1 bg-red-100 text-red-700 rounded text-sm">85% Risk</span>
              </div>
              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">CLM-1092 • Appeal Ready</div>
                  <div className="text-sm text-gray-600">Complex case • Matches your success pattern</div>
                </div>
                <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded text-sm">62% Risk</span>
              </div>
              <div className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <div>
                  <div className="font-medium text-gray-900">CLM-1095 • Quick Fix</div>
                  <div className="text-sm text-gray-600">Routine modifier • 3min estimated</div>
                </div>
                <span className="px-2 py-1 bg-green-100 text-green-700 rounded text-sm">31% Risk</span>
              </div>
            </div>
          </div>
        </div>

        {/* Learning Insights */}
        <div className="mt-8 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <Brain className="w-6 h-6 text-blue-600 mt-1" />
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                🧠 Codexia is Learning About You
              </h3>
              <p className="text-gray-700 mb-4">
                After analyzing your work patterns, I've identified key insights that will make you more productive:
              </p>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <div className="text-sm font-medium text-gray-900 mb-1">Strength Discovery</div>
                  <div className="text-sm text-gray-600">You excel at complex appeals that others struggle with</div>
                </div>
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <div className="text-sm font-medium text-gray-900 mb-1">Pattern Recognition</div>
                  <div className="text-sm text-gray-600">Morning sessions yield 40% better accuracy rates</div>
                </div>
                <div className="bg-white rounded-lg p-4 border border-blue-200">
                  <div className="text-sm font-medium text-gray-900 mb-1">Optimization Opportunity</div>
                  <div className="text-sm text-gray-600">Batching similar claims can save 90min daily</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}