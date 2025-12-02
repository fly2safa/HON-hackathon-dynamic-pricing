'use client';

import { useState, useEffect } from 'react';

interface StatusBarProps {
  backendConnected: boolean;
  weatherConnected: boolean;
  onRestore: () => void;
}

export default function StatusBar({ backendConnected, weatherConnected, onRestore }: StatusBarProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) return null;

  return (
    <div 
      className="fixed top-0 left-0 right-0 z-50 bg-black text-white shadow-md cursor-pointer hover:bg-gray-900 transition-colors"
      onClick={onRestore}
      title="Click to restore hidden banners"
    >
      <div className="max-w-7xl mx-auto px-4 py-1.5 flex items-center justify-between">
        <div className="flex items-center gap-4 text-xs font-medium">
          <div className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-green-400' : 'bg-orange-400'}`}></div>
            <span>Backend</span>
          </div>
          <div className="text-gray-500">|</div>
          <div className="flex items-center gap-1.5">
            <div className={`w-2 h-2 rounded-full ${weatherConnected ? 'bg-green-400' : 'bg-orange-400'}`}></div>
            <span>Weather</span>
          </div>
        </div>
        <div className="text-xs text-gray-400">
          Click to expand
        </div>
      </div>
    </div>
  );
}

