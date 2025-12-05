'use client';

import { useState, useRef, useEffect } from 'react';
import { sendChatMessage, ChatResponse } from '@/lib/apiClient';

// Simple icon components (no external library needed)
const SendIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13"></line>
    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
  </svg>
);

const MessageIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
  </svg>
);

const CloseIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="18" y1="6" x2="6" y2="18"></line>
    <line x1="6" y1="6" x2="18" y2="18"></line>
  </svg>
);

const MinimizeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="4 14 10 14 10 20"></polyline>
    <polyline points="20 10 14 10 14 4"></polyline>
    <line x1="14" y1="10" x2="21" y2="3"></line>
    <line x1="3" y1="21" x2="10" y2="14"></line>
  </svg>
);

const MaximizeIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="15 3 21 3 21 9"></polyline>
    <polyline points="9 21 3 21 3 15"></polyline>
    <line x1="21" y1="3" x2="14" y2="10"></line>
    <line x1="3" y1="21" x2="10" y2="14"></line>
  </svg>
);

const MicrophoneIcon = ({ isActive }: { isActive?: boolean }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill={isActive ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
    <line x1="12" y1="19" x2="12" y2="23"></line>
    <line x1="8" y1="23" x2="16" y2="23"></line>
  </svg>
);

const SpeakerIcon = ({ isActive }: { isActive?: boolean }) => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill={isActive ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
    {isActive && (
      <>
        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"></path>
        <path d="M19.07 4.93a10 10 0 0 1 0 14.14"></path>
      </>
    )}
    {!isActive && (
      <line x1="23" y1="9" x2="17" y2="15"></line>
    )}
  </svg>
);

interface Message {
  id: string;
  role: 'user' | 'bot';
  content: string;
  data?: ChatResponse['data'];
  suggestions?: string[];
  timestamp: Date;
}

interface WeatherInfo {
  temperature: number;
  condition: string;
  weatherType: string;
  isRealData: boolean;
}

interface ChatBotProps {
  currentCity?: string;
  currentWeather?: WeatherInfo | null;
  isOpen?: boolean;
  onToggle?: () => void;
}

export default function ChatBot({ currentCity, currentWeather, isOpen = false, onToggle }: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isVisible, setIsVisible] = useState(isOpen);
  const [inputHistory, setInputHistory] = useState<string[]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [tempInput, setTempInput] = useState(''); // Store current input when navigating history
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  // Use ref to always have latest weather value (avoids stale closure)
  const weatherRef = useRef(currentWeather);
  weatherRef.current = currentWeather;
  
  // Voice features
  const [isListening, setIsListening] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(false);
  const [speechSupported, setSpeechSupported] = useState(false);
  const recognitionRef = useRef<any>(null);

  // Check speech support and initialize
  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Check speech synthesis support
      const synthSupported = 'speechSynthesis' in window;
      
      // Check speech recognition support
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognitionSupported = !!SpeechRecognition;
      
      setSpeechSupported(synthSupported && recognitionSupported);
      
      // Initialize speech recognition
      if (recognitionSupported) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput(transcript);
          setIsListening(false);
          // Auto-send after speech recognition
          setTimeout(() => sendMessage(transcript), 100);
        };
        
        recognition.onerror = (event: any) => {
          console.error('Speech recognition error:', event.error);
          setIsListening(false);
          setVoiceEnabled(false); // Reset on error
        };
        
        recognition.onend = () => {
          setIsListening(false);
        };
        
        recognitionRef.current = recognition;
      }
    }
  }, []);

  // Scroll to bottom on new message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  // Speak bot responses when voice is enabled
  useEffect(() => {
    if (voiceEnabled && messages.length > 0) {
      const lastMessage = messages[messages.length - 1];
      if (lastMessage.role === 'bot') {
        speakText(lastMessage.content);
      }
    }
  }, [messages, voiceEnabled]);

  // Focus input when opened
  useEffect(() => {
    if (isVisible && !isMinimized) {
      inputRef.current?.focus();
    }
  }, [isVisible, isMinimized]);

  // Sync with parent isOpen prop
  useEffect(() => {
    setIsVisible(isOpen);
  }, [isOpen]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Add to input history (avoid duplicates of last entry)
    if (inputHistory[inputHistory.length - 1] !== text.trim()) {
      setInputHistory(prev => [...prev, text.trim()]);
    }
    setHistoryIndex(-1);
    setTempInput('');

    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: text,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Use ref to get latest weather (avoids stale closure in async callbacks)
      const latestWeather = weatherRef.current;
      
      const weatherContext = latestWeather ? {
        temperature: latestWeather.temperature,
        conditions: latestWeather.condition,
        weather_type: latestWeather.weatherType,
        is_real_data: latestWeather.isRealData
      } : undefined;
      
      const response = await sendChatMessage({
        message: text,
        context: {
          current_city: currentCity,
          current_weather: weatherContext
        }
      });

      const botMessage: Message = {
        id: `bot-${Date.now()}`,
        role: 'bot',
        content: response.response,
        data: response.data,
        suggestions: response.suggestions,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      
      // Fallback response when backend is unavailable
      const fallbackMessage: Message = {
        id: `bot-${Date.now()}`,
        role: 'bot',
        content: getMockResponse(text),
        suggestions: [
          "Find all Urban rides at Night",
          "How many Gold customers?",
          "What's the average price?"
        ],
        timestamp: new Date()
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Mock responses when backend is unavailable
  const getMockResponse = (query: string): string => {
    const q = query.toLowerCase();
    
    if (q.includes('urban') && q.includes('night')) {
      return "I found 127 Urban night rides. The average price is $32.50 with a 1.25x surge multiplier typical for nighttime. (Using cached data - backend offline)";
    }
    if (q.includes('gold') && q.includes('customer')) {
      return "You have 45 Gold tier customers who receive 15% loyalty discounts. Average spend: $48/ride. (Using cached data)";
    }
    if (q.includes('average') && q.includes('price')) {
      return "The average ride price is $28.50 with a typical surge multiplier of 1.15x during peak hours. (Using cached data)";
    }
    if (q.includes('driver')) {
      return "There are 50 active drivers with an average rating of 4.7⭐. Top drivers earn $180-250/day. (Using cached data)";
    }
    if (q.includes('surge') || q.includes('demand')) {
      return "Current surge multipliers range from 1.0x (normal) to 2.0x (high demand). NYC averages 1.3x during rush hour. (Using cached data)";
    }
    
    return "I can help you with HoneyGo data! Try asking about rides, customers, pricing, or drivers. (Note: Backend is currently offline, using cached responses)";
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
    // Navigate history with Up/Down arrows
    else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (inputHistory.length === 0) return;
      
      if (historyIndex === -1) {
        // Save current input before navigating
        setTempInput(input);
        setHistoryIndex(inputHistory.length - 1);
        setInput(inputHistory[inputHistory.length - 1]);
      } else if (historyIndex > 0) {
        setHistoryIndex(historyIndex - 1);
        setInput(inputHistory[historyIndex - 1]);
      }
    }
    else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIndex === -1) return;
      
      if (historyIndex < inputHistory.length - 1) {
        setHistoryIndex(historyIndex + 1);
        setInput(inputHistory[historyIndex + 1]);
      } else {
        // Back to current input
        setHistoryIndex(-1);
        setInput(tempInput);
      }
    }
  };

  const toggleChat = () => {
    setIsVisible(!isVisible);
    onToggle?.();
  };

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized);
  };

  const toggleMicrophone = () => {
    if (!speechSupported) {
      alert('Voice input is not supported in your browser. Please use Chrome, Edge, or Safari.');
      return;
    }

    if (isListening) {
      // Stop listening
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      // Start listening (does NOT auto-enable speaker)
      try {
        recognitionRef.current?.start();
        setIsListening(true);
      } catch (error) {
        console.error('Error starting speech recognition:', error);
      }
    }
  };

  const toggleSpeaker = () => {
    if (!speechSupported) {
      alert('Text-to-speech is not supported in your browser.');
      return;
    }
    
    if (voiceEnabled) {
      // Disable and stop any current speech
      window.speechSynthesis.cancel();
      setVoiceEnabled(false);
    } else {
      setVoiceEnabled(true);
    }
  };

  const speakText = (text: string) => {
    if (!speechSupported || typeof window === 'undefined') return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    // Speak
    window.speechSynthesis.speak(utterance);
  };

  // Floating button when chat is closed
  if (!isVisible) {
    return (
      <button
        onClick={toggleChat}
        className="fixed bottom-6 right-6 w-14 h-14 bg-[#FF6A13] rounded-full shadow-lg 
                   flex items-center justify-center hover:bg-[#e55a0a] transition-all
                   hover:scale-110 z-50"
        title="Open HoneyGo Assistant"
      >
        <span className="text-white"><MessageIcon /></span>
      </button>
    );
  }

  return (
    <div 
      className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${
        isMinimized ? 'w-72 h-14' : 'w-96 h-[500px]'
      }`}
    >
      <div className="flex flex-col h-full bg-gray-900 rounded-xl border border-gray-700 shadow-2xl overflow-hidden">
        {/* Header */}
        <div 
          className="flex items-center justify-between p-3 bg-gradient-to-r from-[#FF6A13] to-[#ff8533] cursor-pointer"
          onClick={toggleMinimize}
        >
          <div className="flex items-center gap-2">
            <span className="text-white"><MessageIcon /></span>
            <h3 className="font-semibold text-white text-sm">HoneyGo Assistant</h3>
            {isLoading && (
              <div className="flex space-x-1 ml-2">
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce" />
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce delay-100" />
                <div className="w-1.5 h-1.5 bg-white rounded-full animate-bounce delay-200" />
              </div>
            )}
          </div>
          <div className="flex items-center gap-1">
            <button
              onClick={(e) => { e.stopPropagation(); toggleMinimize(); }}
              className="p-1 hover:bg-white/20 rounded transition-colors"
              title={isMinimized ? "Expand" : "Minimize"}
            >
              <span className="text-white">{isMinimized ? <MaximizeIcon /> : <MinimizeIcon />}</span>
            </button>
            <button
              onClick={(e) => { e.stopPropagation(); toggleChat(); }}
              className="p-1 hover:bg-white/20 rounded transition-colors"
              title="Close"
            >
              <span className="text-white"><CloseIcon /></span>
            </button>
          </div>
        </div>

        {/* Chat content - hidden when minimized */}
        {!isMinimized && (
          <>
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-3 space-y-3">
              {messages.length === 0 && (
                <div className="text-center text-gray-400 mt-4">
                  <p className="text-sm">👋 Hi! I'm your HoneyGo Assistant.</p>
                  <p className="text-xs mt-1 text-gray-500">Try asking:</p>
                  <div className="mt-3 space-y-1.5">
                    {[
                      "Find all Urban rides at Night",
                      "How many Gold customers?",
                      "What's the average price?",
                      "Show driver statistics"
                    ].map((suggestion, i) => (
                      <button
                        key={i}
                        onClick={() => sendMessage(suggestion)}
                        className="block w-full text-left px-3 py-1.5 bg-gray-800 rounded-lg 
                                   hover:bg-gray-700 text-xs text-gray-300 transition-colors"
                      >
                        "{suggestion}"
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-xl px-3 py-2 ${
                      msg.role === 'user'
                        ? 'bg-[#FF6A13] text-white'
                        : 'bg-gray-800 text-gray-100'
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{msg.content}</p>

                    {/* Data summary if available */}
                    {msg.data && msg.data.count !== undefined && (
                      <div className="mt-2 pt-2 border-t border-gray-600/50 text-xs text-gray-400">
                        📊 {msg.data.count} results
                        {msg.data.avg_price && ` • Avg: $${msg.data.avg_price}`}
                      </div>
                    )}

                    {/* Suggestions */}
                    {msg.suggestions && msg.suggestions.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-600/50 space-y-1">
                        <p className="text-xs text-gray-500">Follow-up:</p>
                        {msg.suggestions.slice(0, 3).map((s, i) => (
                          <button
                            key={i}
                            onClick={() => sendMessage(s)}
                            className="block text-xs text-[#FF6A13] hover:underline text-left"
                          >
                            → {s}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-800 rounded-xl px-3 py-2">
                    <div className="flex space-x-1.5">
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                      <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="p-3 border-t border-gray-700">
              <div className="flex gap-2">
                <input
                  ref={inputRef}
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder={isListening ? "Listening..." : "Ask me anything... (↑↓ for history)"}
                  disabled={isLoading || isListening}
                  className="flex-1 bg-gray-800 border border-gray-600 rounded-lg px-3 py-2 
                             text-sm text-white placeholder-gray-500
                             focus:outline-none focus:border-[#FF6A13] focus:ring-1 focus:ring-[#FF6A13]
                             disabled:opacity-50"
                />
                {/* Microphone Button */}
                {/* Speaker Toggle Button */}
                {speechSupported && (
                  <button
                    onClick={toggleSpeaker}
                    disabled={isLoading}
                    className={`p-2 rounded-lg transition-all duration-200 ${
                      voiceEnabled 
                        ? 'bg-green-500 hover:bg-green-600' 
                        : 'bg-gray-700 hover:bg-gray-600'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                    title={voiceEnabled ? 'Disable voice responses' : 'Enable voice responses'}
                  >
                    <span className="text-white">
                      <SpeakerIcon isActive={voiceEnabled} />
                    </span>
                  </button>
                )}
                {/* Microphone Button */}
                {speechSupported && (
                  <button
                    onClick={toggleMicrophone}
                    disabled={isLoading}
                    className={`p-2 rounded-lg transition-all duration-200 ${
                      isListening 
                        ? 'bg-red-500 hover:bg-red-600 animate-pulse' 
                        : 'bg-gray-700 hover:bg-gray-600'
                    } disabled:opacity-50 disabled:cursor-not-allowed`}
                    title={isListening ? 'Stop listening' : 'Click to speak a command'}
                  >
                    <span className="text-white">
                      <MicrophoneIcon isActive={isListening} />
                    </span>
                  </button>
                )}
                <button
                  onClick={() => sendMessage(input)}
                  disabled={!input.trim() || isLoading}
                  className="p-2 bg-[#FF6A13] rounded-lg hover:bg-[#e55a0a] 
                             disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  title="Send message"
                >
                  <span className="text-white"><SendIcon /></span>
                </button>
              </div>
              <div className="flex items-center justify-between mt-1">
                <p className="text-[10px] text-gray-600">
                  Enter to send • ↑↓ history • Powered by LangChain
                </p>
                <div className="flex items-center gap-2">
                  {voiceEnabled && (
                    <span className="text-[10px] text-green-400 flex items-center gap-1">
                      <span className="w-1.5 h-1.5 bg-green-400 rounded-full"></span>
                      🔊 ON
                    </span>
                  )}
                  {isListening && (
                    <span className="text-[10px] text-red-400 flex items-center gap-1">
                      <span className="w-1.5 h-1.5 bg-red-400 rounded-full animate-pulse"></span>
                      🎤 Listening
                    </span>
                  )}
                </div>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

