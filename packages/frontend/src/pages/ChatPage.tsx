import React, { useState, useRef, useEffect } from "react";
import { Send, Bot, User, Zap, FileText, AlertTriangle, CheckCircle, Clock, TrendingUp } from "lucide-react";

interface Message {
  id: string;
  content: string;
  sender: 'user' | 'ai';
  timestamp: Date;
  type?: 'text' | 'claim-preview' | 'suggestion' | 'analysis';
  data?: any;
}

export function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hey there! I'm Alex, and I've been working in RCM for over 15 years. I've seen every kind of claim issue you can imagine! 😊\n\nNow I'm AI-powered and here to make your life easier. I can help you:\n\n• Process claims faster than ever\n• Spot issues before they become denials\n• Optimize your daily workflow\n• Answer questions about specific claims\n\nJust talk to me like you would any RCM expert. Try:\n• \"Show me today's high-risk claims\"\n• \"Why was CLM-1001 flagged?\"\n• \"Help me fix this modifier issue\"",
      sender: 'ai',
      timestamp: new Date(),
      type: 'text'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const mockAIResponse = (userMessage: string): Message[] => {
    const lowercaseMessage = userMessage.toLowerCase();
    
    if (lowercaseMessage.includes('high-risk') || lowercaseMessage.includes('high risk')) {
      return [
        {
          id: Date.now().toString(),
          content: "I found 3 high-risk claims that need your attention. Based on your expertise with modifier issues, I've prioritized them:",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        },
        {
          id: (Date.now() + 1).toString(),
          content: "",
          sender: 'ai',
          timestamp: new Date(),
          type: 'claim-preview',
          data: {
            claims: [
              { id: 'CLM-1087', risk: 85, reason: 'Modifier 59 missing', payer: 'UHC', eta: '3m' },
              { id: 'CLM-1092', risk: 78, reason: 'Dx/CPT mismatch', payer: 'Aetna', eta: '5m' },
              { id: 'CLM-1095', risk: 72, reason: 'Coverage expired', payer: 'BCBS', eta: '4m' }
            ]
          }
        }
      ];
    }
    
    if (lowercaseMessage.includes('clm-1001') || lowercaseMessage.includes('why')) {
      return [
        {
          id: Date.now().toString(),
          content: "CLM-1001 was flagged because it's missing modifier 59, which UHC requires for this procedure combination. Here's the detailed analysis:",
          sender: 'ai',
          timestamp: new Date(),
          type: 'analysis',
          data: {
            claimId: 'CLM-1001',
            risk: 72,
            issues: [
              { type: 'missing_modifier', description: 'Modifier 59 required for procedure 99213', severity: 'high' },
              { type: 'policy_reference', description: 'UHC-LCD-123 §3b mandates modifier for this combination', severity: 'medium' }
            ],
            recommendation: 'Add modifier 59 to procedure 99213',
            confidence: 95
          }
        }
      ];
    }

    if (lowercaseMessage.includes('fix') || lowercaseMessage.includes('correct')) {
      return [
        {
          id: Date.now().toString(),
          content: "I'll fix CLM-1001 by adding the missing modifier 59. Here's what I changed:",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        },
        {
          id: (Date.now() + 1).toString(),
          content: "",
          sender: 'ai',
          timestamp: new Date(),
          type: 'suggestion',
          data: {
            action: 'fix_applied',
            changes: [
              { field: 'procedures[0].modifiers', before: '[]', after: '["59"]' },
              { field: 'risk_score', before: '72%', after: '12%' }
            ],
            confidence: 95,
            reasoning: 'Added modifier 59 as required by UHC-LCD-123 §3b for procedure combination'
          }
        }
      ];
    }

    // UHC specific queries
    if (lowercaseMessage.includes('uhc') && lowercaseMessage.includes('modifier')) {
      return [
        {
          id: Date.now().toString(),
          content: "Found 4 UHC claims with missing modifiers. These are costing us about $23K in potential denials:",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        },
        {
          id: (Date.now() + 1).toString(),
          content: "",
          sender: 'ai',
          timestamp: new Date(),
          type: 'claim-preview',
          data: {
            claims: [
              { id: 'CLM-1087', risk: 85, reason: 'Modifier 59 missing', payer: 'UHC', eta: '3m' },
              { id: 'CLM-1101', risk: 67, reason: 'Modifier 25 missing', payer: 'UHC', eta: '4m' },
              { id: 'CLM-1105', risk: 71, reason: 'Modifier GT required', payer: 'UHC', eta: '5m' },
              { id: 'CLM-1108', risk: 62, reason: 'Modifier 59 + 25 needed', payer: 'UHC', eta: '6m' }
            ]
          }
        }
      ];
    }

    // Appeal generation
    if (lowercaseMessage.includes('appeal') || lowercaseMessage.includes('deny') || lowercaseMessage.includes('denial')) {
      return [
        {
          id: Date.now().toString(),
          content: "I can help you generate a strong appeal letter. For denied diabetes claims, I typically see a 78% success rate when we focus on medical necessity and proper documentation. What's the denial reason?",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    // Productivity questions
    if (lowercaseMessage.includes('productivity') || lowercaseMessage.includes('forecast') || lowercaseMessage.includes('performance')) {
      return [
        {
          id: Date.now().toString(),
          content: "Based on your work patterns, you're on track for a great day! Your morning sessions typically yield 40% better accuracy, so I'd recommend tackling the complex UHC claims first. You've already processed 23 claims today with a 2.1% denial rate - well below the team average of 4.3%.",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    // Batch processing
    if (lowercaseMessage.includes('batch') && lowercaseMessage.includes('modifier')) {
      return [
        {
          id: Date.now().toString(),
          content: "Great idea! I can batch process all modifier 59 fixes. I found 12 claims that need this fix across UHC, Aetna, and BCBS. This should save you about 45 minutes compared to doing them individually.",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    // Educational/help responses
    if (lowercaseMessage.includes('help') || lowercaseMessage.includes('what can you') || lowercaseMessage.includes('how do')) {
      return [
        {
          id: Date.now().toString(),
          content: "I'm here to make your RCM work easier! Here are some things I excel at:\n\n• **Smart Analysis**: I can spot missing modifiers, coding issues, and policy violations before they cause denials\n\n• **Claims Prioritization**: I'll show you which claims need attention first based on risk and value\n\n• **Quick Fixes**: I can batch process common issues like modifier corrections\n\n• **Appeal Support**: I help write compelling appeal letters with high success rates\n\n• **Learning Your Style**: I adapt to your peak hours and specialties for better workflow\n\nTry asking me: \"Show me today's high-risk UHC claims\" or \"Help me fix this modifier issue\"",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    // Payer-specific questions
    if (lowercaseMessage.includes('aetna')) {
      return [
        {
          id: Date.now().toString(),
          content: "Aetna's been tricky lately! They updated their LCD guidelines last month. I'm seeing a lot of prior auth requirements for procedures that used to auto-approve. The key is getting the documentation right upfront. What specific Aetna issue are you dealing with?",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    if (lowercaseMessage.includes('bcbs') || lowercaseMessage.includes('blue cross')) {
      return [
        {
          id: Date.now().toString(),
          content: "BCBS varies so much by state! Are you dealing with a specific BCBS plan? I've noticed their Texas plans are really strict on modifier 25 lately, while their California plans focus more on medical necessity documentation.",
          sender: 'ai',
          timestamp: new Date(),
          type: 'text'
        }
      ];
    }

    // General RCM conversation responses
    const contextualResponses = [
      "That's a great question! In my 15 years of RCM experience, I've seen this pattern before. Can you give me more details about the specific claim or payer you're working with?",
      
      "I can definitely help with that! From what I've observed, this type of issue usually stems from either coding discrepancies or payer-specific policy changes. Which claims are you looking at?",
      
      "Absolutely! This reminds me of a similar situation I handled last quarter where we saved $47K by catching a modifier pattern early. What specific aspect would you like me to analyze?",
      
      "Good catch on bringing this up! I've been tracking similar trends across other RCM teams. Let me know the claim IDs or payer details and I can give you a targeted analysis.",
      
      "I love these kinds of challenges! Based on current payer trends and policy updates, I can probably help you get ahead of any potential issues. What's the specific scenario you're dealing with?",
      
      "That's exactly the kind of thing I'm here for! I can cross-reference this against recent LCD updates and policy changes. Can you share more details about what you're seeing?"
    ];

    return [
      {
        id: Date.now().toString(),
        content: contextualResponses[Math.floor(Math.random() * contextualResponses.length)],
        sender: 'ai',
        timestamp: new Date(),
        type: 'text'
      }
    ];
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: input,
      sender: 'user',
      timestamp: new Date(),
      type: 'text'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    // Simulate AI thinking time
    setTimeout(() => {
      const aiResponses = mockAIResponse(input);
      setMessages(prev => [...prev, ...aiResponses]);
      setIsTyping(false);
    }, 1000 + Math.random() * 1000);
  };

  const quickActions = [
    "Show me high-risk claims from today",
    "Find UHC claims with missing modifiers", 
    "Why was CLM-1001 flagged?",
    "Generate appeal for denied diabetes claim",
    "What's my productivity forecast?",
    "Batch process modifier 59 fixes",
    "Help me with Aetna claims",
    "What can you help me with?",
    "Fix this modifier issue"
  ];

  const ClaimPreview = ({ claims }: { claims: any[] }) => (
    <div className="space-y-3">
      {claims.map((claim, i) => (
        <div key={i} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
          <div className="flex items-center justify-between">
            <div>
              <div className="font-semibold text-gray-900 flex items-center gap-2">
                {claim.id}
                <span className="text-sm text-gray-500">• {claim.payer}</span>
              </div>
              <div className="text-sm text-gray-600">{claim.reason} • ETA {claim.eta}</div>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              claim.risk > 75 ? 'bg-red-100 text-red-700' : 
              claim.risk > 50 ? 'bg-yellow-100 text-yellow-700' : 
              'bg-green-100 text-green-700'
            }`}>
              {claim.risk}% Risk
            </span>
          </div>
        </div>
      ))}
    </div>
  );

  const AnalysisView = ({ data }: { data: any }) => (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center justify-between mb-4">
        <h4 className="font-semibold text-gray-900">Claim Analysis: {data.claimId}</h4>
        <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-medium">
          {data.risk}% Risk
        </span>
      </div>
      
      <div className="space-y-3">
        {data.issues.map((issue: any, i: number) => (
          <div key={i} className="flex items-start gap-3 p-3 bg-red-50 rounded-lg">
            <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5" />
            <div>
              <div className="font-medium text-gray-900">{issue.description}</div>
              <div className="text-sm text-gray-600 capitalize">{issue.severity} severity</div>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-green-50 rounded-lg">
        <div className="flex items-center gap-2 mb-1">
          <CheckCircle className="w-4 h-4 text-green-600" />
          <span className="font-medium text-gray-900">Recommended Action</span>
        </div>
        <div className="text-sm text-gray-700">{data.recommendation}</div>
        <div className="text-xs text-green-600 mt-1">{data.confidence}% confidence</div>
      </div>
    </div>
  );

  const SuggestionView = ({ data }: { data: any }) => (
    <div className="bg-white border border-gray-200 rounded-lg p-4">
      <div className="flex items-center gap-2 mb-4">
        <Zap className="w-5 h-5 text-blue-600" />
        <h4 className="font-semibold text-gray-900">Changes Applied</h4>
      </div>
      
      <div className="space-y-3">
        {data.changes.map((change: any, i: number) => (
          <div key={i} className="p-3 bg-blue-50 rounded-lg">
            <div className="font-medium text-gray-900 text-sm mb-1">{change.field}</div>
            <div className="flex items-center gap-2 text-sm">
              <span className="px-2 py-1 bg-red-100 text-red-700 rounded font-mono">
                {change.before}
              </span>
              <span className="text-gray-400">→</span>
              <span className="px-2 py-1 bg-green-100 text-green-700 rounded font-mono">
                {change.after}
              </span>
            </div>
          </div>
        ))}
      </div>
      
      <div className="mt-4 p-3 bg-gray-50 rounded-lg">
        <div className="text-sm text-gray-700">{data.reasoning}</div>
        <div className="text-xs text-blue-600 mt-1">{data.confidence}% confidence</div>
      </div>
    </div>
  );

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">Alex - Your RCM Expert</h1>
            <p className="text-sm text-gray-600">15+ years of claims expertise, now AI-powered to help you 24/7</p>
          </div>
          <div className="ml-auto">
            <div className="flex items-center gap-2 text-sm text-green-600">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              Online
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-3xl flex gap-3 ${message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-200'
              }`}>
                {message.sender === 'user' ? (
                  <User className="w-4 h-4 text-white" />
                ) : (
                  <Bot className="w-4 h-4 text-gray-600" />
                )}
              </div>
              
              <div className={`rounded-lg p-4 ${
                message.sender === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white border border-gray-200'
              }`}>
                {message.type === 'text' && (
                  <div className="whitespace-pre-wrap">{message.content}</div>
                )}
                
                {message.type === 'claim-preview' && (
                  <div>
                    <div className="text-gray-900 mb-3">{message.content}</div>
                    <ClaimPreview claims={message.data.claims} />
                  </div>
                )}
                
                {message.type === 'analysis' && (
                  <div>
                    <div className="text-gray-900 mb-3">{message.content}</div>
                    <AnalysisView data={message.data} />
                  </div>
                )}
                
                {message.type === 'suggestion' && (
                  <div>
                    <div className="text-gray-900 mb-3">{message.content}</div>
                    <SuggestionView data={message.data} />
                  </div>
                )}
                
                <div className="text-xs opacity-70 mt-2">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="max-w-3xl flex gap-3">
              <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                <Bot className="w-4 h-4 text-gray-600" />
              </div>
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex items-center gap-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      {messages.length === 1 && (
        <div className="px-6 py-4 bg-white border-t border-gray-200">
          <div className="mb-3">
            <h3 className="text-sm font-medium text-gray-700 mb-2">Try these commands:</h3>
            <div className="flex flex-wrap gap-2">
              {quickActions.map((action, i) => (
                <button
                  key={i}
                  onClick={() => setInput(action)}
                  className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-full transition-colors"
                >
                  {action}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Input */}
      <div className="bg-white border-t border-gray-200 p-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask Alex anything about your claims... (e.g., 'Show me high-risk claims')"
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Send className="w-4 h-4" />
            Send
          </button>
        </div>
      </div>
    </div>
  );
}