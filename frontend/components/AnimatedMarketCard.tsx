'use client';

import { useEffect, useState, useRef } from 'react';

interface AnimatedMarketCardProps {
  label: string;
  value: string | number;
  type: 'demand' | 'drivers' | 'rides' | 'weather' | 'traffic';
  weatherData?: {
    isLive?: boolean;
    location?: string;
    weatherType?: string;
  };
}

// Determine if value is "good" or "bad" for coloring
const getValueSentiment = (type: string, value: string | number): 'positive' | 'negative' | 'neutral' => {
  const strValue = String(value).toLowerCase();
  
  switch (type) {
    case 'demand':
      if (strValue === 'surge' || strValue === 'high') return 'negative';
      if (strValue === 'low') return 'positive';
      return 'neutral';
    case 'drivers':
      const driverCount = typeof value === 'number' ? value : parseInt(String(value));
      if (driverCount >= 50) return 'positive';
      if (driverCount <= 20) return 'negative';
      return 'neutral';
    case 'rides':
      return 'neutral'; // Rides are informational
    case 'traffic':
      if (strValue === 'heavy') return 'negative';
      if (strValue === 'light') return 'positive';
      return 'neutral';
    case 'weather':
      if (strValue.includes('storm') || strValue.includes('snow')) return 'negative';
      if (strValue.includes('clear') || strValue.includes('sunny')) return 'positive';
      return 'neutral';
    default:
      return 'neutral';
  }
};

// Get border color based on sentiment
const getBorderColor = (sentiment: 'positive' | 'negative' | 'neutral'): string => {
  switch (sentiment) {
    case 'positive':
      return 'border-green-300';
    case 'negative':
      return 'border-red-300';
    default:
      return 'border-gray-200';
  }
};

// Get text color based on type and value
const getTextColor = (type: string, value: string | number): string => {
  const strValue = String(value).toLowerCase();
  
  switch (type) {
    case 'demand':
      if (strValue === 'surge') return 'text-red-600';
      if (strValue === 'high') return 'text-orange-600';
      if (strValue === 'medium') return 'text-yellow-600';
      return 'text-green-600';
    case 'drivers':
      return 'text-blue-600';
    case 'rides':
      return 'text-purple-600';
    case 'traffic':
      if (strValue === 'heavy') return 'text-red-600';
      if (strValue === 'moderate') return 'text-yellow-600';
      return 'text-green-600';
    default:
      return 'text-gray-800';
  }
};

// Animated number component
const AnimatedNumber = ({ value, duration = 800 }: { value: number; duration?: number }) => {
  const [displayValue, setDisplayValue] = useState(value);
  const previousValueRef = useRef(value);
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  useEffect(() => {
    if (!mounted) return;
    
    const startValue = previousValueRef.current;
    const endValue = value;
    const startTime = Date.now();
    
    const animate = () => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      
      // Easing function
      const easeOutQuart = 1 - Math.pow(1 - progress, 4);
      const current = Math.round(startValue + (endValue - startValue) * easeOutQuart);
      
      setDisplayValue(current);
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      } else {
        previousValueRef.current = endValue;
      }
    };
    
    if (startValue !== endValue) {
      requestAnimationFrame(animate);
    }
  }, [value, duration, mounted]);
  
  // Show initial value without animation on server/initial render
  if (!mounted) return <span>{value}</span>;
  
  return <span>{displayValue}</span>;
};

export default function AnimatedMarketCard({ 
  label, 
  value, 
  type, 
  weatherData 
}: AnimatedMarketCardProps) {
  const [mounted, setMounted] = useState(false);
  const [isAnimating, setIsAnimating] = useState(false);
  const [showShimmer, setShowShimmer] = useState(false);
  const prevValueRef = useRef(value);
  
  // Handle hydration
  useEffect(() => {
    setMounted(true);
  }, []);
  
  const sentiment = getValueSentiment(type, value);
  const borderColor = getBorderColor(sentiment);
  const textColor = getTextColor(type, value);
  
  // Trigger animation when value changes (only after mounted)
  useEffect(() => {
    if (!mounted) return;
    
    if (prevValueRef.current !== value) {
      setIsAnimating(true);
      setShowShimmer(true);
      
      const shimmerTimeout = setTimeout(() => setShowShimmer(false), 1200);
      const animateTimeout = setTimeout(() => setIsAnimating(false), 400);
      
      prevValueRef.current = value;
      
      return () => {
        clearTimeout(shimmerTimeout);
        clearTimeout(animateTimeout);
      };
    }
  }, [value, mounted]);
  
  // Periodic subtle shimmer (only after mounted)
  useEffect(() => {
    if (!mounted) return;
    
    const interval = setInterval(() => {
      setShowShimmer(true);
      setTimeout(() => setShowShimmer(false), 1200);
    }, 10000 + Math.random() * 5000); // 10-15 seconds
    
    return () => clearInterval(interval);
  }, [mounted]);
  
  const isNumeric = typeof value === 'number' || !isNaN(Number(value));
  
  // Get background gradient based on type
  const getBackgroundGradient = () => {
    if (type === 'weather' && weatherData?.weatherType) {
      const wt = weatherData.weatherType;
      if (wt === 'storm') return 'from-red-50 to-orange-50';
      if (wt === 'snow') return 'from-blue-50 to-cyan-50';
      if (wt === 'rain') return 'from-blue-50 to-gray-50';
      if (wt === 'fog') return 'from-gray-100 to-gray-50';
      if (wt === 'clouds') return 'from-gray-50 to-white';
      return 'from-yellow-50 to-white';
    }
    
    switch (type) {
      case 'drivers':
        return 'from-blue-50 to-white';
      case 'rides':
        return 'from-purple-50 to-white';
      default:
        return 'from-gray-50 to-white';
    }
  };
  
  // Get weather emoji - only render on client
  const getWeatherEmoji = () => {
    if (!weatherData?.weatherType) return null;
    const wt = weatherData.weatherType;
    if (wt === 'storm') return '⛈️';
    if (wt === 'snow') return '❄️';
    if (wt === 'rain') return '🌧️';
    if (wt === 'fog') return '🌫️';
    if (wt === 'clouds') return '☁️';
    return '☀️';
  };
  
  return (
    <div 
      className={`
        relative text-center p-4 
        bg-gradient-to-br ${getBackgroundGradient()} 
        rounded-xl border-2 
        ${borderColor}
        transition-all duration-300 ease-out
        ${isAnimating ? 'scale-[1.02] shadow-md' : 'scale-100 shadow-sm'}
        overflow-hidden
      `}
      suppressHydrationWarning
    >
      {/* Shimmer overlay */}
      {showShimmer && mounted && (
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div 
            className="absolute inset-0 -translate-x-full"
            style={{
              background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent)',
              animation: 'shimmer 1.2s ease-in-out forwards'
            }}
          />
        </div>
      )}
      
      {/* Live badge for weather */}
      {type === 'weather' && weatherData?.isLive && mounted && (
        <div className="absolute top-1 right-1">
          <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 border border-green-300">
            🌐 Live
          </span>
        </div>
      )}
      
      {/* Label */}
      <p 
        className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide flex items-center justify-center gap-1"
        suppressHydrationWarning
      >
        {type === 'weather' && mounted && getWeatherEmoji()}
        {label}
      </p>
      
      {/* Value with animation */}
      <p 
        className={`text-2xl font-bold ${textColor} transition-transform duration-300 ${isAnimating ? 'scale-105' : 'scale-100'}`}
        suppressHydrationWarning
      >
        {isNumeric && mounted ? (
          <AnimatedNumber value={Number(value)} duration={600} />
        ) : (
          <span>{String(value).toUpperCase()}</span>
        )}
      </p>
      
      {/* Weather location */}
      {type === 'weather' && weatherData?.location && mounted && (
        <p className="text-xs text-gray-500 mt-1" suppressHydrationWarning>
          {weatherData.location}
        </p>
      )}
      
      {/* Subtle sentiment indicator line at bottom */}
      <div 
        className={`
          absolute bottom-0 left-0 right-0 h-1 
          transition-all duration-500
          ${sentiment === 'positive' ? 'bg-gradient-to-r from-green-400 to-green-300' : 
            sentiment === 'negative' ? 'bg-gradient-to-r from-red-400 to-red-300' : 
            'bg-gradient-to-r from-gray-300 to-gray-200'}
          ${isAnimating ? 'opacity-100' : 'opacity-60'}
        `} 
      />
    </div>
  );
}
