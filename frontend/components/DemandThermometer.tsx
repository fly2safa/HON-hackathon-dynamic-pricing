'use client';

import { useEffect, useState } from 'react';

interface DemandThermometerProps {
  demand: 'low' | 'medium' | 'high' | 'surge';
}

const demandLevels = {
  low: { height: 20, color: 'from-green-400 to-green-500', bgColor: 'bg-green-500' },
  medium: { height: 45, color: 'from-yellow-400 to-yellow-500', bgColor: 'bg-yellow-500' },
  high: { height: 70, color: 'from-orange-400 to-orange-500', bgColor: 'bg-orange-500' },
  surge: { height: 95, color: 'from-red-500 to-red-600', bgColor: 'bg-red-500' },
};

export default function DemandThermometer({ demand }: DemandThermometerProps) {
  const [mounted, setMounted] = useState(false);
  const [animatedHeight, setAnimatedHeight] = useState(0);
  
  const level = demandLevels[demand] || demandLevels.medium;
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  useEffect(() => {
    if (!mounted) return;
    
    // Reset and animate when demand changes
    setAnimatedHeight(0);
    const timer = setTimeout(() => {
      setAnimatedHeight(level.height);
    }, 100);
    
    return () => clearTimeout(timer);
  }, [mounted, demand, level.height]);

  const getTextColor = () => {
    switch (demand) {
      case 'surge': return 'text-red-600';
      case 'high': return 'text-orange-600';
      case 'medium': return 'text-yellow-600';
      default: return 'text-green-600';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-full">
      <p className="text-xs font-semibold text-gray-500 mb-3 uppercase tracking-wide">Demand</p>
      
      <div className="flex items-end gap-3">
        {/* Thermometer */}
        <div className="relative">
          {/* Tube */}
          <div className="relative w-6 h-16 bg-gray-200 rounded-t-full overflow-hidden border-2 border-gray-300 shadow-inner">
            {/* Mercury fill - animated */}
            <div 
              className={`absolute bottom-0 left-0 right-0 bg-gradient-to-t ${level.color} transition-all duration-1000 ease-out`}
              style={{ height: `${mounted ? animatedHeight : 0}%` }}
            >
              {/* Shine effect on mercury */}
              <div className="absolute inset-0 bg-gradient-to-r from-white/40 via-transparent to-transparent w-1/2" />
            </div>
            
            {/* Temperature tick marks */}
            <div className="absolute inset-0 flex flex-col justify-between py-1.5 pointer-events-none">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="w-full flex justify-end pr-0.5">
                  <div className="w-1.5 h-0.5 bg-gray-400/60 rounded-full" />
                </div>
              ))}
            </div>
          </div>
          
          {/* Bulb at bottom */}
          <div className={`relative -mt-1 w-8 h-8 rounded-full ${level.bgColor} border-2 border-gray-300 shadow-md mx-auto left-[-4px]`}>
            {/* Shine on bulb */}
            <div className="absolute top-1 left-1 w-2 h-2 bg-white/40 rounded-full" />
          </div>
        </div>
        
        {/* Label */}
        <span className={`text-xl font-bold ${getTextColor()} pb-2`}>
          {demand.toUpperCase()}
        </span>
      </div>
    </div>
  );
}
