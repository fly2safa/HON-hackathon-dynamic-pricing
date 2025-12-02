'use client';

import { useEffect, useState } from 'react';

interface WeatherStatusBannerProps {
  isRealWeather: boolean;
  onClose?: () => void;
  hasStatusBar?: boolean;
  hasBackendBanner?: boolean;
}

export default function WeatherStatusBanner({ isRealWeather, onClose, hasStatusBar = false, hasBackendBanner = false }: WeatherStatusBannerProps) {
  const [mounted, setMounted] = useState(false);
  const [showBanner, setShowBanner] = useState(true);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted || !showBanner) return null;

  // Calculate top position based on what's showing above
  const topPosition = hasStatusBar && hasBackendBanner ? 'top-[8.5rem]' : 
                      hasStatusBar ? 'top-8' : 
                      hasBackendBanner ? 'top-10' : 
                      'top-0';
  
  return (
    <div className={`fixed ${topPosition} left-0 right-0 z-40 ${
      isRealWeather 
        ? 'bg-gradient-to-r from-green-500 to-emerald-600' 
        : 'bg-gradient-to-r from-orange-500 to-amber-600'
    } text-white py-2 shadow-lg`}>
      <div className="max-w-7xl mx-auto px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {isRealWeather ? (
            <>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium">
                🌐 Live Weather Data
              </span>
              <span className="text-xs opacity-90 ml-2">
                (Real-time data from OpenWeatherMap API)
              </span>
            </>
          ) : (
            <>
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              <span className="text-sm font-medium">
                ⚠️ Weather API Offline
              </span>
              <span className="text-xs opacity-90 ml-2">
                (Using Mock Weather Data)
              </span>
            </>
          )}
        </div>

        {/* Close Button */}
        <button
          onClick={() => {
            setShowBanner(false);
            if (onClose) onClose();
          }}
          className="text-white hover:text-gray-200 transition-colors"
          aria-label="Close banner"
        >
          <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
}

