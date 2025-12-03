'use client';

import { useEffect, useState } from 'react';

interface WeatherCardProps {
  weatherType: 'clear' | 'rain' | 'storm' | 'snow' | 'fog' | 'clouds';
  weatherCondition: string;
  weatherSeverity: 'none' | 'light' | 'moderate' | 'severe';
  isLive?: boolean;
  location?: string;
}

// Animated Sun
const AnimatedSun = () => (
  <div className="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
    <div className="relative">
      {/* Sun rays */}
      <div className="absolute inset-0 animate-spin-slow">
        {[...Array(8)].map((_, i) => (
          <div
            key={i}
            className="absolute w-1 h-8 bg-gradient-to-t from-yellow-400 to-transparent rounded-full"
            style={{
              left: '50%',
              top: '50%',
              transform: `translate(-50%, -100%) rotate(${i * 45}deg)`,
              transformOrigin: '50% 100%',
              opacity: 0.6,
            }}
          />
        ))}
      </div>
      {/* Sun core */}
      <div className="w-12 h-12 bg-gradient-to-br from-yellow-300 to-orange-400 rounded-full shadow-lg animate-pulse-gentle">
        <div className="absolute inset-1 bg-gradient-to-br from-yellow-200 to-yellow-400 rounded-full" />
      </div>
    </div>
  </div>
);

// Animated Clouds
const AnimatedClouds = () => (
  <div className="absolute inset-0 pointer-events-none overflow-hidden">
    {/* Cloud 1 */}
    <div 
      className="absolute animate-cloud-float"
      style={{ top: '15%' }}
    >
      <svg width="50" height="30" viewBox="0 0 50 30" fill="none">
        <ellipse cx="25" cy="20" rx="20" ry="10" fill="#E5E7EB" />
        <ellipse cx="15" cy="18" rx="12" ry="8" fill="#F3F4F6" />
        <ellipse cx="35" cy="17" rx="10" ry="7" fill="#F3F4F6" />
        <ellipse cx="25" cy="14" rx="14" ry="9" fill="white" />
      </svg>
    </div>
    {/* Cloud 2 */}
    <div 
      className="absolute animate-cloud-float-delayed"
      style={{ top: '40%', left: '30%' }}
    >
      <svg width="40" height="25" viewBox="0 0 40 25" fill="none">
        <ellipse cx="20" cy="16" rx="16" ry="8" fill="#E5E7EB" />
        <ellipse cx="12" cy="14" rx="10" ry="6" fill="#F3F4F6" />
        <ellipse cx="28" cy="13" rx="8" ry="5" fill="#F3F4F6" />
        <ellipse cx="20" cy="11" rx="11" ry="7" fill="white" />
      </svg>
    </div>
  </div>
);

// Animated Rain
const AnimatedRain = () => (
  <div className="absolute inset-0 pointer-events-none overflow-hidden">
    {/* Rain cloud */}
    <div className="absolute top-2 left-1/2 -translate-x-1/2">
      <svg width="40" height="20" viewBox="0 0 40 20" fill="none">
        <ellipse cx="20" cy="12" rx="16" ry="8" fill="#9CA3AF" />
        <ellipse cx="12" cy="10" rx="10" ry="6" fill="#D1D5DB" />
        <ellipse cx="28" cy="9" rx="8" ry="5" fill="#D1D5DB" />
      </svg>
    </div>
    {/* Rain drops */}
    {[...Array(12)].map((_, i) => (
      <div
        key={i}
        className="absolute w-0.5 h-3 bg-gradient-to-b from-blue-400 to-blue-300 rounded-full animate-rain-fall"
        style={{
          left: `${10 + (i * 7) % 80}%`,
          animationDuration: `${0.6 + (i % 3) * 0.2}s`,
          animationDelay: `${(i * 0.1) % 0.6}s`,
          top: '25%',
        }}
      />
    ))}
  </div>
);

// Animated Storm with Lightning
const AnimatedStorm = () => {
  const [flash, setFlash] = useState(false);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setFlash(true);
      setTimeout(() => setFlash(false), 150);
    }, 3000 + Math.random() * 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="absolute inset-0 pointer-events-none overflow-hidden">
      {/* Flash overlay */}
      {flash && (
        <div className="absolute inset-0 bg-white/40 z-20" />
      )}
      {/* Dark storm cloud */}
      <div className="absolute top-1 left-1/2 -translate-x-1/2">
        <svg width="50" height="25" viewBox="0 0 50 25" fill="none">
          <ellipse cx="25" cy="15" rx="20" ry="10" fill="#4B5563" />
          <ellipse cx="15" cy="13" rx="12" ry="7" fill="#6B7280" />
          <ellipse cx="35" cy="12" rx="10" ry="6" fill="#6B7280" />
        </svg>
      </div>
      {/* Lightning bolt */}
      <div 
        className="absolute left-1/2 top-6 -translate-x-1/2 z-10"
        style={{ opacity: flash ? 1 : 0.3, transition: 'opacity 0.1s' }}
      >
        <svg width="20" height="35" viewBox="0 0 20 35" fill="none">
          <path 
            d="M12 0L4 15H9L6 35L18 14H12L16 0H12Z" 
            fill={flash ? "#FBBF24" : "#FCD34D"}
            className={flash ? "drop-shadow-[0_0_8px_#FCD34D]" : ""}
          />
        </svg>
      </div>
      {/* Rain */}
      {[...Array(8)].map((_, i) => (
        <div
          key={i}
          className="absolute w-0.5 h-4 bg-gradient-to-b from-blue-500 to-blue-400 rounded-full animate-rain-fall"
          style={{
            left: `${15 + (i * 9) % 70}%`,
            animationDuration: `${0.5 + (i % 3) * 0.15}s`,
            animationDelay: `${(i * 0.08) % 0.5}s`,
            top: '30%',
          }}
        />
      ))}
    </div>
  );
};

export default function WeatherCard({ 
  weatherType, 
  weatherCondition, 
  weatherSeverity,
  isLive,
  location 
}: WeatherCardProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  const getBackgroundGradient = () => {
    switch (weatherType) {
      case 'storm': return 'from-gray-700 to-gray-500';
      case 'rain': return 'from-blue-100 to-gray-200';
      case 'snow': return 'from-blue-50 to-cyan-100';
      case 'fog': return 'from-gray-200 to-gray-100';
      case 'clouds': return 'from-gray-100 to-white';
      case 'clear': return 'from-yellow-100 to-orange-50';
      default: return 'from-gray-50 to-white';
    }
  };

  const getBorderColor = () => {
    switch (weatherType) {
      case 'storm': return 'border-red-300';
      case 'rain': return 'border-blue-200';
      case 'snow': return 'border-blue-300';
      case 'fog': return 'border-gray-300';
      case 'clouds': return 'border-gray-300';
      case 'clear': return 'border-yellow-200';
      default: return 'border-gray-200';
    }
  };

  const getTextColor = () => {
    switch (weatherSeverity) {
      case 'severe': return 'text-red-700';
      case 'moderate': return 'text-orange-700';
      default: return weatherType === 'storm' ? 'text-white' : 'text-gray-800';
    }
  };

  const renderWeatherAnimation = () => {
    if (!mounted) return null;
    
    switch (weatherType) {
      case 'clear': return <AnimatedSun />;
      case 'clouds': return <AnimatedClouds />;
      case 'rain': return <AnimatedRain />;
      case 'storm': return <AnimatedStorm />;
      default: return null;
    }
  };

  return (
    <div 
      className={`text-center p-4 bg-gradient-to-br ${getBackgroundGradient()} rounded-xl border-2 ${getBorderColor()} relative overflow-hidden min-h-[100px]`}
      suppressHydrationWarning
    >
      {/* Weather animation background */}
      {renderWeatherAnimation()}
      
      {/* Live badge */}
      {isLive && mounted && (
        <div className="absolute top-1 right-1 z-20">
          <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 border border-green-300">
            🌐 Live
          </span>
        </div>
      )}
      
      {/* Content */}
      <div className="relative z-10">
        <p className={`text-xs font-semibold mb-2 uppercase tracking-wide flex items-center justify-center gap-1 ${weatherType === 'storm' ? 'text-gray-200' : 'text-gray-500'}`}>
          {weatherType === 'storm' && '⛈️'}
          {weatherType === 'snow' && '❄️'}
          {weatherType === 'rain' && '🌧️'}
          {weatherType === 'fog' && '🌫️'}
          {weatherType === 'clear' && '☀️'}
          {weatherType === 'clouds' && '☁️'}
          Weather
        </p>
        <p className={`text-base font-bold ${getTextColor()}`} suppressHydrationWarning>
          {weatherCondition}
        </p>
        {location && (
          <p className={`text-xs mt-1 ${weatherType === 'storm' ? 'text-gray-300' : 'text-gray-500'}`} suppressHydrationWarning>
            {location}
          </p>
        )}
      </div>
    </div>
  );
}
