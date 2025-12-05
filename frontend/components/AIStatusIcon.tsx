/**
 * AI Status Icon
 * 
 * Floating icon that shows AI processing status with animation.
 * Requested by team for better visibility of AI activity.
 */

'use client';

interface AIStatusIconProps {
  isProcessing: boolean;
  onClick?: () => void;
}

export default function AIStatusIcon({ isProcessing, onClick }: AIStatusIconProps) {
  return (
    <button
      onClick={onClick}
      className={`fixed bottom-24 right-6 z-50 w-16 h-16 rounded-full shadow-2xl transition-all duration-300 flex items-center justify-center ${
        isProcessing 
          ? 'bg-gradient-to-br from-purple-500 to-pink-500 animate-pulse scale-110' 
          : 'bg-gradient-to-br from-blue-500 to-cyan-500 hover:scale-110'
      }`}
      title={isProcessing ? 'AI is calculating...' : 'AI Ready'}
    >
      {isProcessing ? (
        // Processing animation
        <div className="relative w-10 h-10">
          <div className="absolute inset-0 flex items-center justify-center">
            <svg className="w-8 h-8 text-white animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
          {/* Pulsing rings */}
          <div className="absolute inset-0 rounded-full border-2 border-white opacity-50 animate-ping"></div>
        </div>
      ) : (
        // Idle state - Brain/Sparkle icon
        <div className="relative">
          <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
          </svg>
          {/* Sparkle effect */}
          {!isProcessing && (
            <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-300 rounded-full animate-pulse"></div>
          )}
        </div>
      )}
      
      {/* Tooltip on hover */}
      {isProcessing && (
        <div className="absolute bottom-full mb-2 px-3 py-1 bg-gray-900 text-white text-xs rounded-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
          AI Calculating...
        </div>
      )}
    </button>
  );
}

