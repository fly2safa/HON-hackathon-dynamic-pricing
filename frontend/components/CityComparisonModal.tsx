/**
 * City Comparison Modal
 * 
 * Compares dynamic pricing across different cities for similar rides.
 * Shows how location-specific rules and regulations affect pricing.
 * Requested by team to demonstrate geographic pricing intelligence.
 */

'use client';

import { useState } from 'react';
import { type RideRequest, type PricingResult, generateMarketConditions } from '@/lib/mockData';
import { calculatePricingWithBackend } from '@/lib/dataAdapter';
import { formatDistance } from '@/lib/formatUtils';

interface CityComparisonModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CITIES = ['Phoenix', 'New York', 'San Francisco', 'Chicago', 'Tampa'];

export default function CityComparisonModal({ isOpen, onClose }: CityComparisonModalProps) {
  const [city1, setCity1] = useState('Phoenix');
  const [city2, setCity2] = useState('New York');
  const [distance, setDistance] = useState(10);
  const [isComparing, setIsComparing] = useState(false);
  const [result1, setResult1] = useState<PricingResult | null>(null);
  const [result2, setResult2] = useState<PricingResult | null>(null);

  if (!isOpen) return null;

  const handleCompare = async () => {
    setIsComparing(true);
    setResult1(null);
    setResult2(null);

    try {
      // Create similar rides for both cities
      const ride1: RideRequest = {
        id: 'compare-1',
        pickupLocation: `${city1} Downtown`,
        dropoffLocation: `${city1} Airport`,
        city: city1,
        distance: distance,
        estimatedDuration: Math.round(distance * 2.5),
        requestTime: new Date().toISOString(),
        passengerCount: 1,
        loyaltyTier: 'silver',
      };

      const ride2: RideRequest = {
        ...ride1,
        id: 'compare-2',
        pickupLocation: `${city2} Downtown`,
        dropoffLocation: `${city2} Airport`,
        city: city2,
      };

      // Get market conditions for both cities
      const market1 = generateMarketConditions(city1);
      const market2 = generateMarketConditions(city2);

      // Calculate pricing for both
      const [pricing1, pricing2] = await Promise.all([
        calculatePricingWithBackend(ride1, market1.weatherType),
        calculatePricingWithBackend(ride2, market2.weatherType),
      ]);

      setResult1(pricing1);
      setResult2(pricing2);
    } catch (error) {
      console.error('Error comparing cities:', error);
    } finally {
      setIsComparing(false);
    }
  };

  const priceDifference = result1 && result2 
    ? Math.abs(result1.dynamicPrice - result2.dynamicPrice)
    : 0;

  const percentDifference = result1 && result2
    ? ((priceDifference / Math.min(result1.dynamicPrice, result2.dynamicPrice)) * 100).toFixed(1)
    : 0;

  const cheaperCity = result1 && result2
    ? result1.dynamicPrice < result2.dynamicPrice ? city1 : city2
    : null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-2">🏙️ City Pricing Comparison</h2>
              <p className="text-blue-100 text-sm">
                Compare how location-specific rules and regulations affect dynamic pricing
              </p>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>

        {/* Configuration */}
        <div className="p-6 border-b border-gray-200 bg-gray-50">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">City 1</label>
              <select
                value={city1}
                onChange={(e) => {
                  setCity1(e.target.value);
                  setResult1(null);
                  setResult2(null);
                }}
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 font-semibold text-base cursor-pointer hover:border-blue-400"
              >
                {CITIES.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">City 2</label>
              <select
                value={city2}
                onChange={(e) => {
                  setCity2(e.target.value);
                  setResult1(null);
                  setResult2(null);
                }}
                className="w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white text-gray-900 font-semibold text-base cursor-pointer hover:border-blue-400"
              >
                {CITIES.map(city => (
                  <option key={city} value={city}>{city}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Distance: {distance} miles
              </label>
              <input
                type="range"
                min="5"
                max="30"
                value={distance}
                onChange={(e) => {
                  setDistance(Number(e.target.value));
                  setResult1(null);
                  setResult2(null);
                }}
                className="w-full"
              />
            </div>
          </div>
          <button
            onClick={handleCompare}
            disabled={isComparing || city1 === city2}
            className="mt-4 w-full py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-bold rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center gap-2"
          >
            {isComparing ? (
              <>
                <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Comparing...
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Compare Pricing
              </>
            )}
          </button>
          {city1 === city2 && (
            <p className="text-sm text-red-600 mt-2 text-center">Please select different cities to compare</p>
          )}
        </div>

        {/* Results */}
        {(result1 || result2) && (
          <div className="p-6">
            {/* Summary Banner */}
            {result1 && result2 && cheaperCity && (
              <div className="mb-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-300 rounded-xl">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-semibold text-green-800 mb-1">💰 Best Value</p>
                    <p className="text-2xl font-bold text-green-900">{cheaperCity}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-green-700">Save</p>
                    <p className="text-2xl font-bold text-green-900">${priceDifference.toFixed(2)}</p>
                    <p className="text-xs text-green-600">({percentDifference}% cheaper)</p>
                  </div>
                </div>
              </div>
            )}

            {/* Side-by-side comparison */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* City 1 */}
              <div className="border-2 border-gray-200 rounded-xl p-6 bg-white">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span className="text-2xl">📍</span>
                  {city1}
                </h3>
                {result1 ? (
                  <>
                    <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Route</p>
                      <p className="font-semibold text-gray-900">{city1} Downtown → {city1} Airport</p>
                      <p className="text-sm text-gray-600 mt-2">{formatDistance(distance)}</p>
                    </div>
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 mb-2">AI Dynamic Price</p>
                      <p className="text-4xl font-bold text-[#FF6A13]">${result1.dynamicPrice.toFixed(2)}</p>
                      <p className="text-sm text-gray-500 mt-1">
                        Base: ${result1.basePrice.toFixed(2)} × {result1.surgeMultiplier}x surge
                      </p>
                    </div>
                    <div className="space-y-2">
                      <p className="text-sm font-semibold text-gray-700">Pricing Factors:</p>
                      {result1.reasoning.slice(0, 3).map((reason, idx) => (
                        <p key={idx} className="text-xs text-gray-600 flex items-start gap-2">
                          <span className="text-blue-500">•</span>
                          {reason}
                        </p>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="animate-pulse space-y-4">
                    <div className="h-20 bg-gray-200 rounded"></div>
                    <div className="h-16 bg-gray-200 rounded"></div>
                    <div className="h-24 bg-gray-200 rounded"></div>
                  </div>
                )}
              </div>

              {/* City 2 */}
              <div className="border-2 border-gray-200 rounded-xl p-6 bg-white">
                <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span className="text-2xl">📍</span>
                  {city2}
                </h3>
                {result2 ? (
                  <>
                    <div className="mb-4 p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600 mb-1">Route</p>
                      <p className="font-semibold text-gray-900">{city2} Downtown → {city2} Airport</p>
                      <p className="text-sm text-gray-600 mt-2">{formatDistance(distance)}</p>
                    </div>
                    <div className="mb-4">
                      <p className="text-sm text-gray-600 mb-2">AI Dynamic Price</p>
                      <p className="text-4xl font-bold text-[#FF6A13]">${result2.dynamicPrice.toFixed(2)}</p>
                      <p className="text-sm text-gray-500 mt-1">
                        Base: ${result2.basePrice.toFixed(2)} × {result2.surgeMultiplier}x surge
                      </p>
                    </div>
                    <div className="space-y-2">
                      <p className="text-sm font-semibold text-gray-700">Pricing Factors:</p>
                      {result2.reasoning.slice(0, 3).map((reason, idx) => (
                        <p key={idx} className="text-xs text-gray-600 flex items-start gap-2">
                          <span className="text-blue-500">•</span>
                          {reason}
                        </p>
                      ))}
                    </div>
                  </>
                ) : (
                  <div className="animate-pulse space-y-4">
                    <div className="h-20 bg-gray-200 rounded"></div>
                    <div className="h-16 bg-gray-200 rounded"></div>
                    <div className="h-24 bg-gray-200 rounded"></div>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Empty state */}
        {!result1 && !result2 && !isComparing && (
          <div className="p-12 text-center text-gray-500">
            <svg className="w-16 h-16 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            <p className="text-lg font-semibold mb-2">Select cities and click Compare</p>
            <p className="text-sm">See how location affects dynamic pricing for similar rides</p>
          </div>
        )}
      </div>
    </div>
  );
}

