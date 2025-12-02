'use client';

import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import HeroSection from '@/components/HeroSection';
import RideRequestCard from '@/components/RideRequestCard';
import PricingDisplay from '@/components/PricingDisplay';
import AIThinkingAnimation from '@/components/AIThinkingAnimation';
import BackendStatusBanner from '@/components/BackendStatusBanner';
import AIStatusIcon from '@/components/AIStatusIcon';
import CityComparisonModal from '@/components/CityComparisonModal';
import { 
  mockRideRequests, 
  generateMarketConditions,
  simulateAIPricing,
  generateRandomRide,
  getLoyaltyBadge,
  type RideRequest,
  type PricingResult,
  type MarketConditions,
  type LoyaltyTier
} from '@/lib/mockData';
import { useRealWeather } from '@/hooks/useRealWeather';
import { formatWeatherDisplay, getWeatherEmoji } from '@/lib/weatherService';

export default function Home() {
  const [selectedRide, setSelectedRide] = useState<RideRequest | null>(null);
  const [pricingResult, setPricingResult] = useState<PricingResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [rides, setRides] = useState<RideRequest[]>(mockRideRequests);
  const [selectedCity, setSelectedCity] = useState<string>('Phoenix');
  const [selectedLoyaltyTier, setSelectedLoyaltyTier] = useState<LoyaltyTier>('new');
  const [marketConditions, setMarketConditions] = useState<MarketConditions>(generateMarketConditions('Phoenix'));
  const [showCityComparison, setShowCityComparison] = useState(false);
  const resultsSectionRef = useRef<HTMLDivElement>(null);

  // Fetch real-time weather for selected city
  const { weather, loading: weatherLoading, error: weatherError } = useRealWeather(selectedCity);

  // Update market conditions when city or weather changes
  const handleCityChange = (city: string) => {
    setSelectedCity(city);
    setMarketConditions(generateMarketConditions(city));
  };

  // Update weather in market conditions when real weather data arrives
  useEffect(() => {
    if (weather) {
      setMarketConditions(prev => ({
        ...prev,
        weatherCondition: formatWeatherDisplay(weather),
        weatherType: weather.weatherType,
        weatherSeverity: weather.weatherSeverity
      }));
      
      // Log to console for debugging
      console.log(`🌦️ Real weather loaded for ${selectedCity}:`, {
        temperature: weather.temperature,
        condition: weather.condition,
        isRealData: weather.isRealData,
        location: weather.location
      });
    }
  }, [weather, selectedCity]);

  // Scroll when processing starts
  useEffect(() => {
    if (isProcessing && resultsSectionRef.current) {
      const yOffset = -120; // Extra space above
      const element = resultsSectionRef.current;
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }, [isProcessing]);

  const handleCalculatePrice = async (ride: RideRequest) => {
    setSelectedRide(ride);
    setPricingResult(null);
    setIsProcessing(true);

    try {
      // Use backend integration (with automatic fallback to mock if backend unavailable)
      const result = await calculatePricingWithBackend(ride, marketConditions.weatherType);
      setPricingResult(result);
    } catch (error) {
      console.error('Error calculating price:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAddRandomRide = (scheduled: boolean = false) => {
    const newRide = generateRandomRide(scheduled, selectedCity, selectedLoyaltyTier);
    setRides([newRide, ...rides]);
  };

  const handleClearAllRides = () => {
    setRides(mockRideRequests); // Reset to original 3 rides
    setSelectedRide(null);
    setPricingResult(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 pt-10">
      {/* Backend Status Banner */}
      <BackendStatusBanner />
      
      {/* Header */}
      <header className="bg-black shadow-md sticky top-10 z-40">
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
        {/* Action Bar */}
        <div className="mb-6 flex justify-end">
          <button
            onClick={() => setShowCityComparison(true)}
            className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 text-white font-bold rounded-xl hover:from-purple-700 hover:to-blue-700 transition-all duration-300 flex items-center gap-2 shadow-lg hover:shadow-xl"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
            </svg>
            Compare Cities
          </button>
        </div>

        {/* City and Loyalty Selectors */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* City Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">Select Market</label>
          <div className="flex gap-3 flex-wrap">
            {['Phoenix', 'New York', 'San Francisco', 'Chicago', 'Orlando'].map((city) => (
              <button
                key={city}
                onClick={() => handleCityChange(city)}
                className={`px-6 py-3 rounded-xl font-semibold transition-all duration-300 ${
                  selectedCity === city
                    ? 'bg-gradient-to-r from-[#FF6A13] to-[#E55A0A] text-white shadow-lg scale-105'
                    : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-[#FF6A13] hover:shadow-md'
                }`}
              >
                {city === 'Phoenix' ? '🌵' : 
                 city === 'New York' ? '🗽' : 
                 city === 'San Francisco' ? '🌉' : 
                 city === 'Chicago' ? '🏙️' : 
                 city === 'Orlando' ? '🏰' : 
                 '🏜️'} {city}
              </button>
            ))}
          </div>
          </div>

          {/* Loyalty Tier Selector */}
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">Customer Loyalty Tier</label>
            <div className="flex gap-2 flex-wrap">
              {(['new', 'bronze', 'silver', 'gold', 'platinum'] as LoyaltyTier[]).map((tier) => (
                <button
                  key={tier}
                  onClick={() => setSelectedLoyaltyTier(tier)}
                  className={`px-4 py-3 rounded-xl font-semibold transition-all duration-300 text-sm ${
                    selectedLoyaltyTier === tier
                      ? tier === 'platinum' ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg scale-105' :
                        tier === 'gold' ? 'bg-gradient-to-r from-yellow-500 to-orange-500 text-white shadow-lg scale-105' :
                        tier === 'silver' ? 'bg-gradient-to-r from-gray-400 to-gray-500 text-white shadow-lg scale-105' :
                        tier === 'bronze' ? 'bg-gradient-to-r from-orange-700 to-orange-800 text-white shadow-lg scale-105' :
                        'bg-gray-600 text-white shadow-lg scale-105'
                      : 'bg-white text-gray-700 border-2 border-gray-300 hover:border-[#FF6A13] hover:shadow-md'
                  }`}
                >
                  {getLoyaltyBadge(tier)} {tier.charAt(0).toUpperCase() + tier.slice(1)}
                  {tier !== 'new' && <span className="ml-1 text-xs">({tier === 'platinum' ? '20' : tier === 'gold' ? '15' : tier === 'silver' ? '10' : '5'}% off)</span>}
                </button>
              ))}
            </div>
          </div>
        </div>

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
                marketConditions.currentDemand === 'surge' ? 'text-red-600' :
                marketConditions.currentDemand === 'high' ? 'text-orange-600' :
                marketConditions.currentDemand === 'medium' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {marketConditions.currentDemand.toUpperCase()}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Available Drivers</p>
              <p className="text-2xl font-bold text-blue-600">
                {marketConditions.availableDrivers}
              </p>
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-purple-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Active Rides</p>
              <p className="text-2xl font-bold text-purple-600">
                {marketConditions.activeRides}
              </p>
            </div>
            <div className={`text-center p-4 bg-gradient-to-br rounded-xl border-2 relative ${
              marketConditions.weatherType === 'storm' ? 'from-red-50 to-orange-50 border-red-300' :
              marketConditions.weatherType === 'snow' ? 'from-blue-50 to-cyan-50 border-blue-300' :
              marketConditions.weatherType === 'rain' ? 'from-blue-50 to-gray-50 border-blue-200' :
              marketConditions.weatherType === 'fog' ? 'from-gray-100 to-gray-50 border-gray-300' :
              marketConditions.weatherType === 'clouds' ? 'from-gray-50 to-white border-gray-300' :
              'from-yellow-50 to-white border-yellow-200'
            }`}>
              {weather && weather.isRealData && (
                <div className="absolute top-1 right-1">
                  <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 border border-green-300">
                    🌐 Live
                  </span>
                </div>
              )}
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide flex items-center justify-center gap-1">
                {marketConditions.weatherType === 'storm' && '⛈️'}
                {marketConditions.weatherType === 'snow' && '❄️'}
                {marketConditions.weatherType === 'rain' && '🌧️'}
                {marketConditions.weatherType === 'fog' && '🌫️'}
                {marketConditions.weatherType === 'clear' && '☀️'}
                {marketConditions.weatherType === 'clouds' && '☁️'}
                Weather
              </p>
              <p className={`text-base font-bold ${
                marketConditions.weatherSeverity === 'severe' ? 'text-red-700' :
                marketConditions.weatherSeverity === 'moderate' ? 'text-orange-700' :
                'text-gray-800'
              }`}>
                {marketConditions.weatherCondition}
              </p>
              {weather && weather.location && (
                <p className="text-xs text-gray-500 mt-1">
                  {weather.location}
                </p>
              )}
            </div>
            <div className="text-center p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200">
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide">Traffic</p>
              <p className={`text-2xl font-bold ${
                marketConditions.trafficLevel === 'heavy' ? 'text-red-600' :
                marketConditions.trafficLevel === 'moderate' ? 'text-yellow-600' :
                'text-green-600'
              }`}>
                {marketConditions.trafficLevel.toUpperCase()}
              </p>
            </div>
          </div>
        </div>

        {/* Two Column Layout - Responsive */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Left Column: Ride Requests */}
          <div>
            <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
              <h2 className="text-2xl font-bold text-gray-900">
                Ride Requests ({rides.length})
              </h2>
              <div className="flex gap-2 flex-wrap">
                <button
                  onClick={() => handleAddRandomRide(false)}
                  className="px-4 py-2.5 bg-gradient-to-r from-[#FF6A13] to-[#E55A0A] hover:from-[#E55A0A] hover:to-[#D54A00] text-white rounded-xl font-semibold transition-all duration-300 shadow-md hover:shadow-lg transform hover:scale-105 flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                  </svg>
                  Now
                </button>
                <button
                  onClick={() => handleAddRandomRide(true)}
                  className="px-4 py-2.5 bg-white hover:bg-gray-50 text-gray-700 border-2 border-gray-300 hover:border-[#FF6A13] rounded-xl font-semibold transition-all duration-300 shadow-sm hover:shadow-md transform hover:scale-105 flex items-center gap-2"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Schedule
                </button>
                {rides.length > 3 && (
                  <button
                    onClick={handleClearAllRides}
                    className="px-4 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-700 border border-gray-300 rounded-xl font-semibold transition-all duration-300 shadow-sm hover:shadow-md flex items-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                    Clear
                  </button>
                )}
              </div>
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
          <div ref={resultsSectionRef} className="space-y-6">
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

      {/* AI Status Icon - Floating */}
      <AIStatusIcon 
        isProcessing={isProcessing}
        onClick={() => {
          if (isProcessing && resultsSectionRef.current) {
            resultsSectionRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }}
      />

      {/* City Comparison Modal */}
      <CityComparisonModal 
        isOpen={showCityComparison}
        onClose={() => setShowCityComparison(false)}
      />
    </main>
  );
}
