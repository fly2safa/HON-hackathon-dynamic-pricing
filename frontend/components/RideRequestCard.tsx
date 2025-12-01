'use client';

import React from 'react';
import { type RideRequest } from '@/lib/mockData';

interface RideRequestCardProps {
  ride: RideRequest;
  onCalculatePrice: (ride: RideRequest) => void;
  isSelected: boolean;
}

export default function RideRequestCard({ 
  ride, 
  onCalculatePrice, 
  isSelected 
}: RideRequestCardProps) {
  return (
    <div 
      className={`bg-white rounded-xl shadow-sm p-6 border-2 transition-all ${
        isSelected 
          ? 'border-[#FF6A13] shadow-lg' 
          : 'border-gray-200 hover:border-gray-300'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">
            Ride #{ride.id.split('-')[1]}
          </h3>
          <p className="text-sm text-gray-500">
            {new Date(ride.requestTime).toLocaleTimeString()}
          </p>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          {ride.passengerCount} {ride.passengerCount === 1 ? 'passenger' : 'passengers'}
        </div>
      </div>

      {/* Route */}
      <div className="space-y-3 mb-4">
        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
            <div className="w-3 h-3 rounded-full bg-green-500"></div>
          </div>
          <div className="flex-1">
            <p className="text-xs text-gray-500 mb-1">Pickup</p>
            <p className="text-sm font-medium text-gray-800">{ride.pickupLocation}</p>
          </div>
        </div>

        <div className="ml-4 border-l-2 border-dashed border-gray-300 h-4"></div>

        <div className="flex items-start gap-3">
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-red-100 flex items-center justify-center">
            <div className="w-3 h-3 rounded-full bg-red-500"></div>
          </div>
          <div className="flex-1">
            <p className="text-xs text-gray-500 mb-1">Dropoff</p>
            <p className="text-sm font-medium text-gray-800">{ride.dropoffLocation}</p>
          </div>
        </div>
      </div>

      {/* Trip Details */}
      <div className="grid grid-cols-2 gap-4 mb-4 p-3 bg-gray-50 rounded-lg">
        <div>
          <p className="text-xs text-gray-500 mb-1">Distance</p>
          <p className="text-lg font-semibold text-gray-800">{ride.distance} mi</p>
        </div>
        <div>
          <p className="text-xs text-gray-500 mb-1">Est. Duration</p>
          <p className="text-lg font-semibold text-gray-800">{ride.estimatedDuration} min</p>
        </div>
      </div>

      {/* Calculate Button */}
      <button
        onClick={() => onCalculatePrice(ride)}
        className="w-full py-3 bg-[#FF6A13] hover:bg-[#E55A0A] text-white font-semibold rounded-lg transition-colors flex items-center justify-center gap-2"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        Calculate Price
      </button>
    </div>
  );
}

