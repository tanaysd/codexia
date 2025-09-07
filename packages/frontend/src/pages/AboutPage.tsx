import React from "react";
import { Heart, Clock, Target, TrendingUp, Users, Zap, CheckCircle, ArrowRight } from "lucide-react";

export function AboutPage() {
  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-5xl mx-auto">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Heart className="w-8 h-8 text-red-500" />
            <h1 className="text-4xl font-bold text-gray-900">Why We Built Codexia</h1>
          </div>
          <p className="text-xl text-gray-600 leading-relaxed max-w-3xl mx-auto">
            Because we believe RCM professionals deserve tools that amplify their expertise,
            not replace their judgment.
          </p>
        </div>

        {/* Journey Layout with Connecting Line */}
        <div className="relative">
          {/* Central Connecting Line */}
          <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-orange-200 via-blue-200 via-purple-200 via-green-200 via-red-200 to-indigo-200 transform -translate-x-0.5 hidden md:block"></div>

          <div className="space-y-12 md:space-y-16">
            
            {/* Step 1 - The Problem (Left) */}
            <div className="flex justify-start">
              <div className="relative w-full md:w-5/12">
                <div className="bg-white rounded-xl border border-orange-200 shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-orange-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">1</div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                        <Clock className="w-6 h-6 text-orange-600" />
                        The Problem We Witnessed
                      </h2>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">RCM Teams Were Struggling</h3>
                      <ul className="space-y-2 text-gray-700">
                        <li className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                          Spending 4+ hours daily on routine claim reviews
                        </li>
                        <li className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                          Missing critical modifier issues that led to denials
                        </li>
                        <li className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-red-500 rounded-full mt-2"></div>
                          Training new staff took 6+ months to be productive
                        </li>
                      </ul>
                    </div>
                    <div className="p-4 bg-red-50 rounded-lg border border-red-200">
                      <div className="font-medium text-red-800">$2.4M annual revenue loss</div>
                      <div className="text-sm text-red-600">Due to preventable denials and 40% staff burnout</div>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -right-8 w-8 h-0.5 bg-orange-300"></div>
              </div>
            </div>

            {/* Step 2 - Our Vision (Right) */}
            <div className="flex justify-end">
              <div className="relative w-full md:w-5/12">
                <div className="bg-white rounded-xl border border-blue-200 shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-blue-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">2</div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2 flex items-center gap-2">
                        <Target className="w-6 h-6 text-blue-600" />
                        Our Vision
                      </h2>
                      <p className="text-gray-600">AI That Amplifies Human Expertise</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                        <Users className="w-4 h-4 text-blue-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Expert Partnership</h4>
                        <p className="text-sm text-gray-600">AI that works <em>with</em> you, not instead of you.</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                        <Zap className="w-4 h-4 text-green-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Superhuman Speed</h4>
                        <p className="text-sm text-gray-600">Process claims 10x faster while maintaining accuracy.</p>
                      </div>
                    </div>
                    <div className="flex items-start gap-3">
                      <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                        <TrendingUp className="w-4 h-4 text-purple-600" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-gray-900">Continuous Learning</h4>
                        <p className="text-sm text-gray-600">AI that learns from your expertise every day.</p>
                      </div>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -left-8 w-8 h-0.5 bg-blue-300"></div>
              </div>
            </div>

            {/* Step 3 - The Story Behind Our Design (Left) */}
            <div className="flex justify-start">
              <div className="relative w-full md:w-5/12">
                <div className="bg-white rounded-xl border border-purple-200 shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-purple-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">3</div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">The Story Behind Our Design</h2>
                      <p className="text-gray-600">Intentional Flow That Mirrors Expertise</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <p className="text-gray-700">
                      Every section follows an intentional order that mirrors how RCM experts actually work.
                    </p>
                    <div className="space-y-3 text-sm">
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-xs font-bold">1</div>
                        <div>
                          <span className="font-medium text-gray-900">Morning Brief</span>
                          <span className="text-gray-600"> → Assess your day</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 bg-green-600 text-white rounded-full flex items-center justify-center text-xs font-bold">2</div>
                        <div>
                          <span className="font-medium text-gray-900">Chat with Alex</span>
                          <span className="text-gray-600"> → Consult when needed</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 bg-purple-600 text-white rounded-full flex items-center justify-center text-xs font-bold">3</div>
                        <div>
                          <span className="font-medium text-gray-900">Workbench</span>
                          <span className="text-gray-600"> → Work with AI routing</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 bg-red-600 text-white rounded-full flex items-center justify-center text-xs font-bold">4</div>
                        <div>
                          <span className="font-medium text-gray-900">Denial Prevention</span>
                          <span className="text-gray-600"> → Prove your impact</span>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 bg-indigo-600 text-white rounded-full flex items-center justify-center text-xs font-bold">5</div>
                        <div>
                          <span className="font-medium text-gray-900">AI Insights</span>
                          <span className="text-gray-600"> → Improve continuously</span>
                        </div>
                      </div>
                    </div>
                    <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                      <div className="flex items-center gap-2 mb-2">
                        <Heart className="w-4 h-4 text-red-500" />
                        <span className="font-medium text-gray-900 text-sm">This is How Experts Think</span>
                      </div>
                      <p className="text-xs text-gray-700">
                        Not trendy tech - this is professional expertise enhanced by AI.
                      </p>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -right-8 w-8 h-0.5 bg-purple-300"></div>
              </div>
            </div>

            {/* Step 4 - What Makes Us Different (Right) */}
            <div className="flex justify-end">
              <div className="relative w-full md:w-5/12">
                <div className="bg-white rounded-xl border border-green-200 shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-green-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">4</div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">What Makes Us Different</h2>
                      <p className="text-gray-600">Built by RCM Experts, for RCM Experts</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-gray-900 text-sm">100+ Hours with Professionals</h4>
                        <p className="text-xs text-gray-600">Understanding real workflows, not building another "AI tool."</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-gray-900 text-sm">Personalized to Your Style</h4>
                        <p className="text-xs text-gray-600">Alex learns your peak hours, specialties, and preferences.</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-gray-900 text-sm">Conversational, Not Complicated</h4>
                        <p className="text-xs text-gray-600">Talk to Alex like a senior colleague. No training required.</p>
                      </div>
                    </div>
                    <div className="flex gap-3">
                      <CheckCircle className="w-5 h-5 text-green-600 mt-0.5" />
                      <div>
                        <h4 className="font-semibold text-gray-900 text-sm">Transparent Decision Making</h4>
                        <p className="text-xs text-gray-600">Every recommendation comes with clear explanations.</p>
                      </div>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -left-8 w-8 h-0.5 bg-green-300"></div>
              </div>
            </div>

            {/* Step 5 - Early Impact Stories (Left) */}
            <div className="flex justify-start">
              <div className="relative w-full md:w-5/12">
                <div className="bg-white rounded-xl border border-red-200 shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-red-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">5</div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-2">Early Impact Stories</h2>
                      <p className="text-gray-600">Real Results from Real Professionals</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span className="font-medium text-green-800 text-sm">Sarah, Senior RCM Specialist</span>
                      </div>
                      <p className="text-sm text-green-700 italic mb-1">
                        "Alex caught a modifier pattern I'd been missing for weeks. Saved us $47K."
                      </p>
                      <div className="text-xs text-green-600 font-medium">25% faster processing</div>
                    </div>
                    <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                        <span className="font-medium text-blue-800 text-sm">Marcus, RCM Manager</span>
                      </div>
                      <p className="text-sm text-blue-700 italic mb-1">
                        "New hires productive in 2 weeks, not 6 months. Like having a mentor on demand."
                      </p>
                      <div className="text-xs text-blue-600 font-medium">75% faster onboarding</div>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -right-8 w-8 h-0.5 bg-red-300"></div>
              </div>
            </div>

            {/* Step 6 - Call to Action (Right) */}
            <div className="flex justify-end">
              <div className="relative w-full md:w-5/12">
                <div className="bg-gradient-to-r from-gray-900 to-blue-900 text-white rounded-xl shadow-lg p-8">
                  <div className="flex items-start gap-4 mb-6">
                    <div className="w-14 h-14 bg-indigo-600 text-white rounded-full flex items-center justify-center text-xl font-bold shadow-lg">6</div>
                    <div>
                      <h2 className="text-2xl font-bold mb-2">Ready to Transform?</h2>
                      <p className="text-gray-300">Join the RCM Revolution</p>
                    </div>
                  </div>
                  <div className="space-y-4">
                    <p className="text-gray-300 text-sm">
                      Join RCM professionals who are already using AI to amplify their expertise
                      and reclaim their time for what matters most.
                    </p>
                    <div className="space-y-3">
                      <button className="w-full px-6 py-3 bg-white text-gray-900 rounded-lg font-medium hover:bg-gray-100 transition-colors flex items-center justify-center gap-2">
                        Start Chatting with Alex
                        <ArrowRight className="w-4 h-4" />
                      </button>
                      <button className="w-full px-6 py-3 border border-white text-white rounded-lg font-medium hover:bg-white hover:text-gray-900 transition-colors">
                        View Morning Brief
                      </button>
                    </div>
                  </div>
                </div>
                {/* Arrow to center line */}
                <div className="hidden md:block absolute top-8 -left-8 w-8 h-0.5 bg-indigo-300"></div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}