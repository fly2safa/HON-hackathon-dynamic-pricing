'use client';

import React, { useState, useEffect } from 'react';

interface AIThinkingAnimationProps {
  isThinking: boolean;
  currentStep?: string;
  steps?: string[];
}

export default function AIThinkingAnimation({ 
  isThinking, 
  currentStep,
  steps = [
    'Analyzing ride request...',
    'Checking real-time demand...',
    'Evaluating driver availability...',
    'Calculating optimal price...',
    'Finalizing recommendation...'
  ]
}: AIThinkingAnimationProps) {
  const [elapsedTime, setElapsedTime] = useState(0);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    if (!isThinking) {
      setElapsedTime(0);
      setCurrentStepIndex(0);
      return;
    }

    const timer = setInterval(() => {
      setElapsedTime(prev => prev + 0.1);
    }, 100);

    return () => clearInterval(timer);
  }, [isThinking]);

  useEffect(() => {
    if (!isThinking) return;

    const stepInterval = setInterval(() => {
      setCurrentStepIndex(prev => {
        if (prev < steps.length - 1) {
          return prev + 1;
        }
        return prev;
      });
    }, 1500);

    return () => clearInterval(stepInterval);
  }, [isThinking, steps.length]);

  if (!isThinking) return null;

  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 shadow-lg border border-blue-200">
      {/* Header with Timer */}
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
          </span>
          AI Processing
        </h3>
        <div className="text-2xl font-mono font-bold text-blue-600">
          {elapsedTime.toFixed(1)}s
        </div>
      </div>

      {/* Gemini-inspired animated dots */}
      <div className="flex justify-center items-center gap-2 mb-6">
        {[0, 1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="w-3 h-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-500"
            style={{
              animation: `bounce 1.4s ease-in-out ${i * 0.16}s infinite`,
            }}
          />
        ))}
      </div>

      {/* Progress Steps */}
      <div className="space-y-3">
        {steps.map((step, index) => (
          <div
            key={index}
            className={`flex items-center gap-3 transition-all duration-300 ${
              index <= currentStepIndex ? 'opacity-100' : 'opacity-30'
            }`}
          >
            {index < currentStepIndex ? (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500 flex items-center justify-center">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
            ) : index === currentStepIndex ? (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center">
                <div className="w-3 h-3 rounded-full bg-white animate-pulse" />
              </div>
            ) : (
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-gray-300" />
            )}
            <span
              className={`text-sm ${
                index <= currentStepIndex ? 'text-gray-800 font-medium' : 'text-gray-400'
              }`}
            >
              {step}
            </span>
          </div>
        ))}
      </div>

      <style jsx>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
          }
          40% {
            transform: scale(1);
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
}

