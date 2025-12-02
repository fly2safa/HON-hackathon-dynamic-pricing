'use client';

import React from 'react';
import { type RideRequest, getLoyaltyBadge } from '@/lib/mockData';
import { formatDistance } from '@/lib/formatUtils';

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
      className={`bg-white rounded-2xl shadow-sm p-6 border-2 transition-all duration-300 hover:shadow-md animate-slideIn ${
        isSelected 
          ? 'border-[#FF6A13] shadow-lg scale-[1.02]' 
          : 'border-gray-200 hover:border-gray-300'
      }`}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-2 mb-1 flex-wrap">
            <h3 className="text-xl font-bold text-gray-900">
              Ride #{ride.id.split('-')[1]}
            </h3>
            <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs font-semibold rounded-full flex items-center gap-1">
              📍 {ride.city}
            </span>
            {ride.loyaltyTier && ride.loyaltyTier !== 'new' && (
              <span className={`px-2 py-1 text-xs font-semibold rounded-full flex items-center gap-1 ${
                ride.loyaltyTier === 'platinum' ? 'bg-purple-100 text-purple-700' :
                ride.loyaltyTier === 'gold' ? 'bg-yellow-100 text-yellow-700' :
                ride.loyaltyTier === 'silver' ? 'bg-gray-200 text-gray-700' :
                'bg-orange-100 text-orange-700'
              }`}>
                {getLoyaltyBadge(ride.loyaltyTier)} {ride.loyaltyTier.toUpperCase()}
              </span>
            )}
            {ride.isScheduled ? (
              <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs font-semibold rounded-full flex items-center gap-1">
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                SCHEDULED
              </span>
            ) : (
              <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs font-semibold rounded-full">
                NOW
              </span>
            )}
          </div>
          <p className="text-sm text-gray-500">
            {ride.isScheduled && ride.scheduledTime 
              ? `Scheduled for ${new Date(ride.scheduledTime).toLocaleString([], { 
                  month: 'short', 
                  day: 'numeric', 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}`
              : `Requested ${new Date(ride.requestTime).toLocaleTimeString()}`
            }
          </p>
        </div>
        <div className="flex items-center gap-2 px-3 py-2 bg-gray-50 rounded-lg">
          <svg className="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <span className="text-sm font-semibold text-gray-700">
            {ride.passengerCount}
          </span>
        </div>
      </div>

      {/* Route */}
      <div className="space-y-4 mb-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
            <div className="w-4 h-4 rounded-full bg-green-500"></div>
          </div>
          <div className="flex-1 pt-1">
            <p className="text-xs font-semibold text-green-700 mb-1 uppercase tracking-wide">Pickup</p>
            <p className="text-base font-semibold text-gray-900">{ride.pickupLocation}</p>
          </div>
        </div>

        <div className="ml-5 border-l-2 border-dashed border-gray-300 h-6"></div>

        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-10 h-10 rounded-full bg-red-100 flex items-center justify-center">
            <div className="w-4 h-4 rounded-full bg-red-500"></div>
          </div>
          <div className="flex-1 pt-1">
            <p className="text-xs font-semibold text-red-700 mb-1 uppercase tracking-wide">Dropoff</p>
            <p className="text-base font-semibold text-gray-900">{ride.dropoffLocation}</p>
          </div>
        </div>
      </div>

      {/* Trip Details */}
      <div className="grid grid-cols-2 gap-4 mb-6 p-4 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200">
        <div>
          <p className="text-xs font-medium text-gray-500 mb-1">Distance</p>
          <p className="text-lg font-bold text-gray-900">{formatDistance(ride.distance)}</p>
        </div>
        <div>
          <p className="text-xs font-medium text-gray-500 mb-1">Est. Duration</p>
          <p className="text-2xl font-bold text-gray-900">{ride.estimatedDuration} <span className="text-base font-normal text-gray-600">min</span></p>
        </div>
      </div>

      {/* Calculate Button */}
      <button
        onClick={() => onCalculatePrice(ride)}
        className="w-full py-4 bg-gradient-to-r from-[#FF6A13] to-[#E55A0A] hover:from-[#E55A0A] hover:to-[#D54A00] text-white font-bold rounded-xl transition-all duration-300 flex items-center justify-center gap-2 shadow-md hover:shadow-lg transform hover:scale-[1.02]"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        Calculate AI Price
      </button>
    </div>
  );
}

