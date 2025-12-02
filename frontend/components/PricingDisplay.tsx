'use client';

import React from 'react';
import { type PricingResult, type RideRequest } from '@/lib/mockData';
import { formatDistance } from '@/lib/formatUtils';

interface PricingDisplayProps {
  result: PricingResult;
  ride: RideRequest;
}

export default function PricingDisplay({ result, ride }: PricingDisplayProps) {
  const savingsForDriver = result.driverEarnings - (result.basePrice * 0.8);
  const savingsPercentage = ((savingsForDriver / (result.basePrice * 0.8)) * 100).toFixed(0);

  return (
    <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200 animate-fadeIn">
      {/* Ride Info Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl p-4 mb-6 border border-blue-200">
        <div className="flex items-center justify-between mb-2">
          <p className="text-xs font-semibold text-blue-600 uppercase tracking-wide">Calculation for</p>
          {ride.isScheduled ? (
            <span className="px-3 py-1 bg-purple-600 text-white text-xs font-bold rounded-full flex items-center gap-1">
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              Scheduled: {new Date(ride.scheduledTime!).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
            </span>
          ) : (
            <span className="px-3 py-1 bg-blue-600 text-white text-xs font-bold rounded-full flex items-center gap-1">
              <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
              </svg>
              Pickup Now
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="font-bold text-gray-900">Ride #{ride.id.split('-')[1]}</span>
          <span className="text-gray-400">•</span>
          <span className="text-gray-700">{ride.pickupLocation}</span>
          <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span className="text-gray-700">{ride.dropoffLocation}</span>
        </div>
        {ride.isScheduled && (
          <div className="mt-3 flex items-start gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
            <svg className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <p className="text-xs font-semibold text-yellow-800 mb-1">Estimated Price</p>
              <p className="text-xs text-yellow-700">
                Final price may vary based on real-time market conditions at scheduled pickup time.
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center">
            <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">AI Pricing Complete</h2>
            <div className="flex gap-4 text-sm text-gray-500">
              <span>⚡ AI Processing: <span className="font-semibold text-blue-600">
                {result.processingTime < 1 
                  ? `${(result.processingTime * 1000).toFixed(0)}ms` 
                  : `${result.processingTime.toFixed(2)}s`}
              </span></span>
              {result.totalTime !== undefined && (
                <span>⏱️ Total Time: <span className="font-semibold text-gray-700">
                  {result.totalTime < 1 
                    ? `${(result.totalTime * 1000).toFixed(0)}ms` 
                    : `${result.totalTime.toFixed(2)}s`}
                </span></span>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Competitor Comparison Banner */}
      {result.competitorPricing && result.competitorPricing.savings > 0 && (
        <div className="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-2xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
                <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <p className="text-sm font-semibold text-green-800 uppercase tracking-wide">Best Price Guarantee</p>
                <p className="text-2xl font-bold text-green-700">Save ${result.competitorPricing.savings.toFixed(2)} ({result.competitorPricing.savingsPercent.toFixed(0)}%)</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xs text-green-700 mb-1">vs Competitors</p>
              <div className="flex gap-2 text-xs flex-wrap justify-end">
                <span className="px-2 py-1 bg-white rounded border border-green-200 text-gray-600">
                  Uber: ${result.competitorPricing.uber.toFixed(2)}
                </span>
                <span className="px-2 py-1 bg-white rounded border border-green-200 text-gray-600">
                  Lyft: ${result.competitorPricing.lyft.toFixed(2)}
                </span>
                {result.competitorPricing.hasWaymo && result.competitorPricing.waymo && (
                  <span className="px-2 py-1 bg-white rounded border border-green-200 text-gray-600 flex items-center gap-1">
                    🤖 Waymo: ${result.competitorPricing.waymo.toFixed(2)}
                  </span>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Price Comparison */}
      <div className="grid grid-cols-2 gap-6 mb-8">
        <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-6 border border-gray-200">
          <p className="text-sm font-semibold text-gray-600 mb-2 uppercase tracking-wide">Standard Price</p>
          <p className="text-4xl font-bold text-gray-700">${result.basePrice.toFixed(2)}</p>
          <p className="text-xs text-gray-500 mt-2">Traditional pricing</p>
        </div>
        <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 border-2 border-[#FF6A13] shadow-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 w-20 h-20 bg-[#FF6A13] opacity-10 rounded-full -mr-10 -mt-10"></div>
          <p className="text-sm font-bold text-[#E55A0A] mb-2 uppercase tracking-wide">AI Dynamic Price</p>
          <p className="text-4xl font-bold text-[#FF6A13]">${result.dynamicPrice.toFixed(2)}</p>
          <p className="text-xs text-orange-700 mt-2 font-medium">Optimized by AI</p>
        </div>
      </div>

      {/* Surge Multiplier */}
      {result.surgeMultiplier > 1.0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2 mb-2">
            <svg className="w-5 h-5 text-yellow-600" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p className="font-semibold text-yellow-800">Surge Pricing Active</p>
          </div>
          <p className="text-sm text-yellow-700">
            {result.surgeMultiplier}x multiplier applied due to high demand
          </p>
        </div>
      )}

      {/* Driver Earnings - Highlighted Feature */}
      <div className="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-300 rounded-2xl p-6 mb-8 shadow-md">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
            <svg className="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="flex-1">
            <p className="text-sm font-bold text-green-800 uppercase tracking-wide">Driver Earnings</p>
            <p className="text-3xl font-bold text-green-700">${result.driverEarnings.toFixed(2)}</p>
          </div>
        </div>
        {savingsForDriver > 0 && (
          <div className="bg-white rounded-lg p-3 border border-green-200">
            <p className="text-sm font-semibold text-green-800 flex items-center gap-2">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              Bonus: +${savingsForDriver.toFixed(2)} ({savingsPercentage}%) above standard rate
            </p>
          </div>
        )}
      </div>

      {/* Confidence Score */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <p className="text-sm font-medium text-gray-700">AI Confidence</p>
          <p className="text-sm font-bold text-blue-600">{(result.confidence * 100).toFixed(0)}%</p>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-500"
            style={{ width: `${result.confidence * 100}%` }}
          ></div>
        </div>
      </div>

      {/* AI Reasoning */}
      <div>
        <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
          <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
          AI Reasoning
        </h3>
        <div className="space-y-2">
          {result.reasoning.map((reason, index) => (
            <div 
              key={index}
              className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg border border-purple-100"
            >
              <div className="flex-shrink-0 w-6 h-6 rounded-full bg-purple-500 text-white flex items-center justify-center text-xs font-bold">
                {index + 1}
              </div>
              <p className="text-sm text-gray-700 flex-1">{reason}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Trip Summary */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h4 className="text-sm font-semibold text-gray-600 mb-3">Trip Summary</h4>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <p className="text-gray-500">From</p>
            <p className="font-medium text-gray-800">{ride.pickupLocation}</p>
          </div>
          <div>
            <p className="text-gray-500">To</p>
            <p className="font-medium text-gray-800">{ride.dropoffLocation}</p>
          </div>
          <div>
            <p className="text-gray-500">Distance</p>
            <p className="font-medium text-gray-800">{formatDistance(ride.distance)}</p>
          </div>
          <div>
            <p className="text-gray-500">Duration</p>
            <p className="font-medium text-gray-800">{ride.estimatedDuration} min</p>
          </div>
        </div>
      </div>
    </div>
  );
}

