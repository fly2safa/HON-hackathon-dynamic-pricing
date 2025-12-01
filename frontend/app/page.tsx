'use client';

import { useState } from 'react';
import Image from 'next/image';
import HeroSection from '@/components/HeroSection';
import RideRequestCard from '@/components/RideRequestCard';
import PricingDisplay from '@/components/PricingDisplay';
import AIThinkingAnimation from '@/components/AIThinkingAnimation';
import { 
  mockRideRequests, 
  mockMarketConditions,
  simulateAIPricing,
  generateRandomRide,
  type RideRequest,
  type PricingResult 
} from '@/lib/mockData';

export default function Home() {
  const [selectedRide, setSelectedRide] = useState<RideRequest | null>(null);
  const [pricingResult, setPricingResult] = useState<PricingResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [rides, setRides] = useState<RideRequest[]>(mockRideRequests);

  const handleCalculatePrice = async (ride: RideRequest) => {
    setSelectedRide(ride);
    setPricingResult(null);
    setIsProcessing(true);

    try {
      const result = await simulateAIPricing(ride.id);
      setPricingResult(result);
    } catch (error) {
      console.error('Error calculating price:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAddRandomRide = () => {
    const newRide = generateRandomRide();
    setRides([newRide, ...rides]);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
      {/* Header */}
      <header className="bg-black shadow-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Image 
                src="/images/honeygo-logo.png" 
                alt="HoneyGo Logo" 
                width={48} 
                height={48}
                className="rounded-lg"
              />
              <div>
                <h1 className="text-2xl font-bold text-white">
                  HoneyGo
                </h1>
                <p className="text-sm text-gray-400">
                  AI-Powered Pricing Platform
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-xs text-gray-400">Powered by</p>
              <p className="text-sm font-semibold text-[#FF6A13]">
                Honeywell AI
              </p>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <HeroSection />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Market Conditions Banner */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900">
              Live Market Conditions
            </h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
            <div className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Demand</p>
              <p className={`text-2xl font-bold ${
                mockMarketConditions.currentDemand === 'surge' ? 'text-red-600' :
                mockMarketConditions.currentDemand === 'high' ? 'text-orange-600' :
                mockMarketConditions.currentDemand === 'medium' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {mockMarketConditions.currentDemand.toUpperCase()}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Available Drivers</p>
              <p className="text-2xl font-bold text-blue-600">
                {mockMarketConditions.availableDrivers}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Active Rides</p>
              <p className="text-2xl font-bold text-purple-600">
                {mockMarketConditions.activeRides}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Weather</p>
              <p className="text-base font-bold text-gray-800">
                {mockMarketConditions.weatherCondition}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Traffic</p>
              <p className={`text-2xl font-bold ${
                mockMarketConditions.trafficLevel === 'heavy' ? 'text-red-600' :
                mockMarketConditions.trafficLevel === 'moderate' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {mockMarketConditions.trafficLevel.toUpperCase()}
              </p>
            </div>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Ride Requests */}
          <div>
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">
                Ride Requests
              </h2>
              <button
                onClick={handleAddRandomRide}
                className="px-5 py-2.5 bg-gradient-to-r from-[#FF6A13] to-[#E55A0A] hover:from-[#E55A0A] hover:to-[#D54A00] text-white rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105"
              >
                + Add Ride
              </button>
            </div>
            <div className="space-y-4">
              {rides.map((ride) => (
                <RideRequestCard
                  key={ride.id}
                  ride={ride}
                  onCalculatePrice={handleCalculatePrice}
                  isSelected={selectedRide?.id === ride.id}
                />
              ))}
            </div>
          </div>

          {/* Right Column: AI Processing & Results */}
          <div className="space-y-6">
            {isProcessing && (
              <AIThinkingAnimation isThinking={isProcessing} />
            )}
            
            {pricingResult && !isProcessing && (
              <PricingDisplay 
                result={pricingResult}
                ride={selectedRide!}
              />
            )}

            {!selectedRide && !isProcessing && (
              <div className="bg-white rounded-xl shadow-sm p-12 text-center border border-gray-200">
                <div className="text-6xl mb-4">🚗</div>
                <h3 className="text-xl font-semibold text-gray-800 mb-2">
                  Select a Ride Request
                </h3>
                <p className="text-gray-600">
                  Click "Calculate Price" on any ride request to see AI-powered dynamic pricing in action
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-8 bg-blue-50 rounded-xl p-6 border border-blue-200">
          <div className="flex items-start gap-3">
            <div className="text-2xl">ℹ️</div>
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">
                Demo Mode - Using Mock Data
              </h3>
              <p className="text-sm text-blue-800">
                This frontend is currently running with mock data to demonstrate the UI/UX. 
                Once the backend (FastAPI + LangChain Agent) and databases (MongoDB + ChromaDB) 
                are ready, this will connect to real AI-powered pricing decisions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
