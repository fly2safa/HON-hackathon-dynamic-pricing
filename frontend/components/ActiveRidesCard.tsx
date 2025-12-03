'use client';

import { useEffect, useState } from 'react';

interface ActiveRidesCardProps {
  count: number;
}

// Car with passenger (different style from available drivers)
const RideCar = ({ delay, duration, yPosition }: { delay: number; duration: number; yPosition: number }) => (
  <div 
    className="absolute"
    style={{
      top: `${yPosition}%`,
      animation: `rideCarDrive ${duration}s linear infinite`,
      animationDelay: `${delay}s`,
    }}
  >
    <svg width="28" height="16" viewBox="0 0 28 16" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Car body */}
      <path 
        d="M4 9h20l-2.5-5H8L4 9z" 
        fill="#9333EA"
      />
      <rect x="2" y="9" width="24" height="5" rx="1" fill="#7C3AED" />
      {/* Windows with passenger silhouette */}
      <path d="M9 5.5h3.5v3H9V5.5z" fill="#C4B5FD" />
      <path d="M14.5 5.5H18v3h-3.5V5.5z" fill="#C4B5FD" />
      {/* Passenger head silhouette in back */}
      <circle cx="16" cy="6.5" r="1.2" fill="#7C3AED" />
      {/* Wheels */}
      <circle cx="7" cy="14" r="2" fill="#1F2937" />
      <circle cx="21" cy="14" r="2" fill="#1F2937" />
      <circle cx="7" cy="14" r="1" fill="#6B7280" />
      <circle cx="21" cy="14" r="1" fill="#6B7280" />
      {/* Headlights glow effect */}
      <circle cx="25" cy="11" r="1" fill="#FCD34D" />
    </svg>
  </div>
);

export default function ActiveRidesCard({ count }: ActiveRidesCardProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  // Calculate number of cars to show (1-8 cars based on count)
  const numCars = Math.min(8, Math.max(1, Math.ceil(count / 20)));
  
  // Generate cars with staggered positions and timing
  const cars = Array.from({ length: numCars }, (_, i) => ({
    id: i,
    delay: i * 0.6,
    duration: 2.5 + (i % 4) * 0.4,
    yPosition: 10 + (i * 10) % 55,
  }));

  return (
    <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200 relative overflow-hidden min-h-[100px]">
      {/* Animated cars background */}
      {mounted && (
        <div className="absolute inset-0 pointer-events-none">
          {cars.map((car) => (
            <RideCar key={car.id} delay={car.delay} duration={car.duration} yPosition={car.yPosition} />
          ))}
        </div>
      )}
      
      {/* Content overlay */}
      <div className="relative z-10">
        <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Active Rides</p>
        <p className="text-2xl font-bold text-purple-600">
          {count}
        </p>
      </div>
      
      {/* CSS for car animation */}
      <style jsx>{`
        @keyframes rideCarDrive {
          0% {
            left: -35px;
            opacity: 0;
          }
          5% {
            opacity: 1;
          }
          95% {
            opacity: 1;
          }
          100% {
            left: calc(100% + 35px);
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
