'use client';

import { useEffect, useState } from 'react';

interface DemandThermometerCardProps {
  demand: 'low' | 'medium' | 'high' | 'surge';
}

const demandLevels = {
  low: { height: 25, color: 'from-green-400 to-green-500', label: 'LOW', textColor: 'text-green-700' },
  medium: { height: 50, color: 'from-yellow-400 to-yellow-500', label: 'MEDIUM', textColor: 'text-yellow-700' },
  high: { height: 75, color: 'from-orange-400 to-orange-500', label: 'HIGH', textColor: 'text-orange-700' },
  surge: { height: 95, color: 'from-red-500 to-red-600', label: 'SURGE', textColor: 'text-red-700' },
};

export default function DemandThermometerCard({ demand }: DemandThermometerCardProps) {
  const [mounted, setMounted] = useState(false);
  const [animatedHeight, setAnimatedHeight] = useState(0);
  
  const level = demandLevels[demand] || demandLevels.medium;
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  useEffect(() => {
    if (!mounted) return;
    
    // Animate to target height
    const timer = setTimeout(() => {
      setAnimatedHeight(level.height);
    }, 100);
    
    return () => clearTimeout(timer);
  }, [mounted, level.height, demand]);
  
  return (
    <div className="relative text-center p-4 bg-gray-100 rounded-xl border-2 border-gray-300 overflow-hidden min-h-[140px] flex flex-col justify-between">
      {/* Mercury fill - rises from bottom */}
      <div 
        className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t ${level.color} transition-all duration-1000 ease-out`}
        style={{ height: `${mounted ? animatedHeight : 0}%` }}
      >
        {/* Shine effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-white/20 via-transparent to-transparent w-1/3" />
        
        {/* Bubble animation at top of fill */}
        {mounted && animatedHeight > 30 && (
          <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2">
            <div className="w-3 h-3 bg-white/50 rounded-full animate-pulse" />
          </div>
        )}
      </div>
      
      {/* Content - positioned above the fill */}
      <div className="relative z-10">
        <p className="text-xs font-semibold text-gray-700 mb-2 uppercase tracking-wide drop-shadow-sm">
          Demand
        </p>
        <p className={`text-2xl font-bold ${level.textColor} drop-shadow-sm`}>
          {level.label}
        </p>
      </div>
      
      {/* Temperature marks on the side */}
      <div className="absolute right-2 top-2 bottom-2 flex flex-col justify-between pointer-events-none opacity-30">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="w-1 h-0.5 bg-gray-600" />
        ))}
      </div>
    </div>
  );
}

