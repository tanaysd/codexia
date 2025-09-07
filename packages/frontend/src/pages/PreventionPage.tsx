import React, { useState } from "react";
import { Shield, DollarSign, TrendingUp, AlertTriangle, CheckCircle, Clock, Target, Zap, Award, BarChart3 } from "lucide-react";

export function PreventionPage() {
  const [timeRange, setTimeRange] = useState('Q1 2024');
  
  // Mock data that would come from real analytics
  const preventionStats = {
    totalPrevented: 1247,
    totalSaved: 2840000,
    avgClaimValue: 2278,
    preventionRate: 94.2,
    topIssues: [
      { issue: "Modifier 59 Missing", prevented: 342, saved: 778000, trend: "+15%" },
      { issue: "Dx/CPT Mismatch", prevented: 298, saved: 679000, trend: "+22%" },
      { issue: "Coverage Verification", prevented: 234, saved: 533000, trend: "+8%" },
      { issue: "Prior Authorization", prevented: 189, saved: 431000, trend: "+31%" },
      { issue: "Bundling Errors", prevented: 184, saved: 419000, trend: "+12%" }
    ]
  };

  const dailyTrend = [
    { date: "Jan 1", prevented: 12, saved: 27360 },
    { date: "Jan 2", prevented: 15, saved: 34170 },
    { date: "Jan 3", prevented: 18, saved: 41004 },
    { date: "Jan 4", prevented: 21, saved: 47838 },
    { date: "Jan 5", prevented: 19, saved: 43282 },
    { date: "Jan 6", prevented: 16, saved: 36448 },
    { date: "Jan 7", prevented: 23, saved: 52394 }
  ];

  const recentPrevented = [
    { id: "CLM-2341", issue: "Modifier 59 missing", value: 3420, timestamp: "2 mins ago", confidence: 97 },
    { id: "CLM-2342", issue: "Invalid Dx code", value: 2890, timestamp: "5 mins ago", confidence: 94 },
    { id: "CLM-2343", issue: "Coverage expired", value: 4120, timestamp: "8 mins ago", confidence: 98 },
    { id: "CLM-2344", issue: "Bundling error", value: 1560, timestamp: "12 mins ago", confidence: 91 },
    { id: "CLM-2345", issue: "PA required", value: 5670, timestamp: "15 mins ago", confidence: 96 }
  ];

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <Shield className="w-8 h-8 text-green-600" />
              <h1 className="text-3xl font-bold text-gray-900">Denial Prevention</h1>
            </div>
            <p className="text-gray-600">AI-powered prevention saving your organization millions</p>
          </div>
          <div className="flex items-center gap-4">
            <select 
              value={timeRange} 
              onChange={(e) => setTimeRange(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg bg-white"
            >
              <option>Q1 2024</option>
              <option>Q4 2023</option>
              <option>Q3 2023</option>
            </select>
            <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2">
              <Shield className="w-4 h-4" />
              Export Report
            </button>
          </div>
        </div>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl border border-gray-200 p-6 text-center">
            <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="w-6 h-6 text-green-600" />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{preventionStats.totalPrevented.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Denials Prevented</div>
            <div className="text-xs text-green-600 mt-1">+18% vs last quarter</div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6 text-center">
            <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <DollarSign className="w-6 h-6 text-blue-600" />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">${(preventionStats.totalSaved / 1000000).toFixed(1)}M</div>
            <div className="text-sm text-gray-600">Revenue Saved</div>
            <div className="text-xs text-blue-600 mt-1">+22% vs last quarter</div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6 text-center">
            <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Target className="w-6 h-6 text-purple-600" />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{preventionStats.preventionRate}%</div>
            <div className="text-sm text-gray-600">Prevention Rate</div>
            <div className="text-xs text-purple-600 mt-1">+3.2% vs last quarter</div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6 text-center">
            <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Clock className="w-6 h-6 text-orange-600" />
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">${preventionStats.avgClaimValue.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Avg Saved/Claim</div>
            <div className="text-xs text-orange-600 mt-1">+$150 vs last quarter</div>
          </div>
        </div>

        {/* ROI Impact Banner */}
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl p-8 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <Award className="w-8 h-8" />
                <h2 className="text-2xl font-bold">Incredible ROI Impact</h2>
              </div>
              <p className="text-green-100 mb-4">
                AI prevention has saved your organization more money this quarter than the annual cost of 15 full-time staff members
              </p>
              <div className="grid grid-cols-3 gap-8">
                <div>
                  <div className="text-3xl font-bold">${(preventionStats.totalSaved / 1000000).toFixed(1)}M</div>
                  <div className="text-sm text-green-100">Total Saved</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">2,847%</div>
                  <div className="text-sm text-green-100">ROI on AI Investment</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">15.2x</div>
                  <div className="text-sm text-green-100">Revenue Multiple</div>
                </div>
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg font-medium text-green-100 mb-2">Cost of Codexia AI</div>
              <div className="text-4xl font-bold">$99K</div>
              <div className="text-sm text-green-100">Annual Subscription</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Top Prevention Categories */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="w-5 h-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900">Top Prevention Categories</h3>
            </div>
            <div className="space-y-4">
              {preventionStats.topIssues.map((item, i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium text-gray-900">{item.issue}</div>
                    <div className="text-sm text-gray-600">{item.prevented} claims prevented</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-gray-900">${(item.saved / 1000).toFixed(0)}K</div>
                    <div className={`text-sm ${item.trend.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                      {item.trend} vs last quarter
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Real-time Prevention Feed */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-yellow-600" />
                <h3 className="text-lg font-semibold text-gray-900">Real-time Prevention</h3>
              </div>
              <div className="flex items-center gap-2 text-sm text-green-600">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                Live
              </div>
            </div>
            <div className="space-y-3">
              {recentPrevented.map((item, i) => (
                <div key={i} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                  <div className="flex items-center gap-3">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <div>
                      <div className="font-medium text-gray-900">{item.id}</div>
                      <div className="text-sm text-gray-600">{item.issue}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-green-600">${item.value.toLocaleString()}</div>
                    <div className="text-xs text-gray-500">{item.timestamp}</div>
                    <div className="text-xs text-blue-600">{item.confidence}% confidence</div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-blue-50 rounded-lg text-center">
              <div className="text-sm text-blue-700">
                <span className="font-medium">23 more denials</span> prevented in the last hour
              </div>
            </div>
          </div>

          {/* Weekly Trend Chart */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="w-5 h-5 text-green-600" />
              <h3 className="text-lg font-semibold text-gray-900">Daily Prevention Trend</h3>
            </div>
            <div className="space-y-3">
              {dailyTrend.map((day, i) => (
                <div key={i} className="flex items-center justify-between">
                  <div className="text-sm text-gray-600 w-16">{day.date}</div>
                  <div className="flex-1 mx-4">
                    <div className="bg-gray-200 rounded-full h-2 relative">
                      <div 
                        className="bg-green-500 h-2 rounded-full" 
                        style={{ width: `${(day.prevented / 25) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-medium text-gray-900">{day.prevented} claims</div>
                    <div className="text-xs text-green-600">${(day.saved / 1000).toFixed(0)}K saved</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Predictive Alerts */}
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <div className="flex items-center gap-2 mb-6">
              <AlertTriangle className="w-5 h-5 text-orange-600" />
              <h3 className="text-lg font-semibold text-gray-900">Predictive Alerts</h3>
            </div>
            <div className="space-y-4">
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="w-4 h-4 text-red-600" />
                  <span className="font-medium text-red-800">High Risk Pattern Detected</span>
                </div>
                <div className="text-sm text-red-700 mb-2">
                  UHC claims with procedure 99213 are 85% likely to be denied without modifier 59
                </div>
                <div className="text-xs text-red-600">Estimated impact: $127K in potential denials</div>
              </div>
              
              <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <Clock className="w-4 h-4 text-yellow-600" />
                  <span className="font-medium text-yellow-800">Policy Change Alert</span>
                </div>
                <div className="text-sm text-yellow-700 mb-2">
                  New Medicare guidelines effective Monday will affect 23% of your claim volume
                </div>
                <div className="text-xs text-yellow-600">Recommended: Update workflow rules</div>
              </div>
              
              <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center gap-2 mb-2">
                  <TrendingUp className="w-4 h-4 text-blue-600" />
                  <span className="font-medium text-blue-800">Optimization Opportunity</span>
                </div>
                <div className="text-sm text-blue-700 mb-2">
                  Batching orthopedic claims together could prevent 15% more denials
                </div>
                <div className="text-xs text-blue-600">Potential additional savings: $45K/month</div>
              </div>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <div className="mt-8 bg-white rounded-xl border border-gray-200 p-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Executive Summary</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Financial Impact</h4>
              <p className="text-sm text-gray-600">
                Codexia's AI prevention system has saved <strong>${(preventionStats.totalSaved / 1000000).toFixed(1)}M</strong> in 
                denied claims this quarter, delivering a <strong>2,847% ROI</strong> on your AI investment.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Operational Excellence</h4>
              <p className="text-sm text-gray-600">
                Prevention rate of <strong>{preventionStats.preventionRate}%</strong> puts you in the top 1% of 
                healthcare organizations nationally for denial management efficiency.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 mb-2">Strategic Advantage</h4>
              <p className="text-sm text-gray-600">
                Predictive capabilities enable proactive policy adaptation, keeping you ahead of 
                industry changes and maintaining competitive advantage.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}