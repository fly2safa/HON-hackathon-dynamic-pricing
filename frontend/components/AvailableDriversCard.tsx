'use client';

import { useEffect, useState } from 'react';

interface AvailableDriversCardProps {
  count: number;
}

// Simple car SVG component
const Car = ({ delay, duration, yPosition }: { delay: number; duration: number; yPosition: number }) => (
  <div 
    className="absolute"
    style={{
      top: `${yPosition}%`,
      animation: `carDrive ${duration}s linear infinite`,
      animationDelay: `${delay}s`,
    }}
  >
    <svg width="24" height="14" viewBox="0 0 24 14" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Car body */}
      <path 
        d="M3 8h18l-2-4H7L3 8z" 
        fill="#3B82F6"
      />
      <rect x="1" y="8" width="22" height="4" rx="1" fill="#2563EB" />
      {/* Windows */}
      <path d="M8 5h3v3H8V5z" fill="#93C5FD" />
      <path d="M13 5h3v3h-3V5z" fill="#93C5FD" />
      {/* Wheels */}
      <circle cx="6" cy="12" r="2" fill="#1F2937" />
      <circle cx="18" cy="12" r="2" fill="#1F2937" />
      <circle cx="6" cy="12" r="1" fill="#6B7280" />
      <circle cx="18" cy="12" r="1" fill="#6B7280" />
    </svg>
  </div>
);

export default function AvailableDriversCard({ count }: AvailableDriversCardProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  // Calculate number of cars to show (1-6 cars based on count)
  const numCars = Math.min(6, Math.max(1, Math.ceil(count / 15)));
  
  // Generate cars with staggered positions and timing
  const cars = Array.from({ length: numCars }, (_, i) => ({
    id: i,
    delay: i * 0.8,
    duration: 3 + (i % 3) * 0.5,
    yPosition: 15 + (i * 12) % 50,
  }));

  return (
    <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200 relative overflow-hidden min-h-[100px]">
      {/* Animated cars background */}
      {mounted && (
        <div className="absolute inset-0 pointer-events-none">
          {cars.map((car) => (
            <Car key={car.id} delay={car.delay} duration={car.duration} yPosition={car.yPosition} />
          ))}
        </div>
      )}
      
      {/* Content overlay */}
      <div className="relative z-10">
        <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Available Drivers</p>
        <p className="text-2xl font-bold text-blue-600">
          {count}
        </p>
      </div>
      
      {/* CSS for car animation */}
      <style jsx>{`
        @keyframes carDrive {
          0% {
            left: -30px;
            opacity: 0;
          }
          5% {
            opacity: 1;
          }
          95% {
            opacity: 1;
          }
          100% {
            left: calc(100% + 30px);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
