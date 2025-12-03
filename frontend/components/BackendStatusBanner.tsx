/**
 * Backend Status Banner
 * 
 * Shows whether the app is connected to the real backend or using mock data.
 */

'use client';

import { useState, useEffect } from 'react';
import { isBackendAvailable } from '@/lib/dataAdapter';

interface BackendStatusBannerProps {
  onClose?: () => void;
  onStatusChange?: (connected: boolean) => void;
  hasStatusBar?: boolean;
}

export default function BackendStatusBanner({ onClose, onStatusChange, hasStatusBar = false }: BackendStatusBannerProps = {}) {
  const [backendStatus, setBackendStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [showBanner, setShowBanner] = useState(true);

  useEffect(() => {
    checkBackendStatus();
    
    // Check every 30 seconds
    const interval = setInterval(checkBackendStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  const checkBackendStatus = async () => {
    const isAvailable = await isBackendAvailable();
    setBackendStatus(isAvailable ? 'connected' : 'disconnected');
    if (onStatusChange) {
      onStatusChange(isAvailable);
    }
  };

  if (!showBanner) return null;

  return (
    <div className={`fixed ${hasStatusBar ? 'top-8' : 'top-0'} left-0 right-0 z-50 ${
      backendStatus === 'checking' 
        ? 'bg-yellow-500' 
        : backendStatus === 'connected' 
          ? 'bg-green-600' 
          : 'bg-orange-500'
    } text-white transition-all duration-300`}>
      <div className="max-w-7xl mx-auto px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Status Icon */}
          <div className="flex items-center gap-2">
            {backendStatus === 'checking' && (
              <>
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Checking backend connection...</span>
              </>
            )}
            {backendStatus === 'connected' && (
              <>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium">
                  ✅ Connected to Backend + MongoDB
                </span>
                <span className="text-xs opacity-90 ml-2">
                  (Real AI pricing with database)
                </span>
              </>
            )}
            {backendStatus === 'disconnected' && (
              <>
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="text-sm font-medium">
                  ⚠️ Backend Offline - Using Mock Data
                </span>
                <span className="text-xs opacity-90 ml-2">
                  (Demo mode with simulated pricing)
                </span>
              </>
            )}
          </div>
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

