'use client';

import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import HeroSection from '@/components/HeroSection';
import RideRequestCard from '@/components/RideRequestCard';
import PricingDisplay from '@/components/PricingDisplay';
import AIThinkingAnimation from '@/components/AIThinkingAnimation';
import BackendStatusBanner from '@/components/BackendStatusBanner';
import WeatherStatusBanner from '@/components/WeatherStatusBanner';
import StatusBar from '@/components/StatusBar';
import AIStatusIcon from '@/components/AIStatusIcon';
import CityComparisonModal from '@/components/CityComparisonModal';
import ActiveRidesCard from '@/components/ActiveRidesCard';
import AvailableDriversCard from '@/components/AvailableDriversCard';
import DemandThermometer from '@/components/DemandThermometer';
import DemandThermometerCard from '@/components/DemandThermometerCard';
import ChatBot from '@/components/ChatBot';
import N8nNotificationContainer from '@/components/N8nNotificationContainer';
import ExecutiveAlertNotification, { ExecutiveAlertNotificationRef } from '@/components/ExecutiveAlertNotification';
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
import { calculatePricingWithBackend } from '@/lib/dataAdapter';
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
  const [showBackendBanner, setShowBackendBanner] = useState(true);
  const [showWeatherBanner, setShowWeatherBanner] = useState(true);
  const [backendConnected, setBackendConnected] = useState(false);
  const [showSchedulePicker, setShowSchedulePicker] = useState(false);
  const [scheduledDateTime, setScheduledDateTime] = useState('');
  const [isScrolled, setIsScrolled] = useState(false);
  const resultsSectionRef = useRef<HTMLDivElement>(null);
  const executiveAlertRef = useRef<ExecutiveAlertNotificationRef>(null);

  // Fetch real-time weather for selected city
  const { weather, loading: weatherLoading, error: weatherError } = useRealWeather(selectedCity);

  // Scroll detection to auto-hide/show banners with hysteresis to prevent flickering
  useEffect(() => {
    const handleScroll = () => {
      const scrollPosition = window.scrollY;
      // Hide banners when scrolled down more than 150px
      if (scrollPosition > 150 && !isScrolled) {
        setIsScrolled(true);
        setShowBackendBanner(false);
        setShowWeatherBanner(false);
      } 
      // Show banners only when scrolled to the very top (within 10px)
      else if (scrollPosition <= 10 && isScrolled) {
        setIsScrolled(false);
        setShowBackendBanner(true);
        setShowWeatherBanner(true);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [isScrolled]);

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

  // Auto-recalculate price when loyalty tier changes (if a ride is already selected and priced)
  useEffect(() => {
    if (selectedRide && pricingResult && !isProcessing) {
      console.log(`🎟️ Loyalty tier changed to ${selectedLoyaltyTier}, recalculating price...`);
      
      // Update the selected ride with new loyalty tier
      const updatedRide = {
        ...selectedRide,
        loyaltyTier: selectedLoyaltyTier
      };
      
      setSelectedRide(updatedRide);
      
      // Recalculate pricing with new loyalty tier
      handleCalculatePrice(updatedRide);
    }
  }, [selectedLoyaltyTier]); // Only trigger when loyalty tier changes

  // Scroll when processing starts
  useEffect(() => {
    if (isProcessing && resultsSectionRef.current) {
      const yOffset = -220; // Extra space above (adjusted for banner layout)
      const element = resultsSectionRef.current;
      const y = element.getBoundingClientRect().top + window.pageYOffset + yOffset;
      
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }, [isProcessing]);

  const handleCalculatePrice = async (ride: RideRequest) => {
    // Apply the currently selected loyalty tier to the ride
    const rideWithLoyaltyTier = {
      ...ride,
      loyaltyTier: selectedLoyaltyTier
    };
    
    setSelectedRide(rideWithLoyaltyTier);
    setPricingResult(null);
    setIsProcessing(true);

    // Track total time from user's perspective
    const totalStartTime = Date.now();

    try {
      // Use backend integration (with automatic fallback to mock if backend unavailable)
      const result = await calculatePricingWithBackend(rideWithLoyaltyTier, marketConditions.weatherType, marketConditions.currentDemand);
      
      // Calculate total time (should always be >= processingTime)
      const totalTime = (Date.now() - totalStartTime) / 1000;
      
      // Ensure totalTime is at least as large as processingTime
      const adjustedTotalTime = Math.max(totalTime, result.processingTime);
      
      // Add total time to result
      setPricingResult({
        ...result,
        totalTime: adjustedTotalTime
      });
    } catch (error) {
      console.error('Error calculating price:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleAddRandomRide = (scheduled: boolean = false, customDateTime?: string) => {
    const newRide = generateRandomRide(scheduled, selectedCity, selectedLoyaltyTier, customDateTime);
    setRides([newRide, ...rides]);
    setShowSchedulePicker(false);
    setScheduledDateTime('');
  };

  const handleClearAllRides = () => {
    setRides(mockRideRequests); // Reset to original 3 rides
    setSelectedRide(null);
    setPricingResult(null);
  };

  // Calculate header sticky position based on visible banners
  const hasStatusBar = !showBackendBanner || !showWeatherBanner;
  const headerTop = (showBackendBanner && showWeatherBanner) ? 'top-[5.5rem]' : // Both banners (88px)
                    showBackendBanner ? 'top-[4.5rem]' : // Backend + status bar (72px)
                    showWeatherBanner ? 'top-[4.5rem]' : // Weather + status bar (72px)
                    'top-[1.75rem]'; // Status bar only (28px)
  
  return (
    <main className="min-h-screen bg-black">
      {/* Compact Status Bar - Shows when at least one banner is closed */}
      {hasStatusBar && (
        <StatusBar
          backendConnected={backendConnected}
          weatherConnected={weather?.isRealData || false}
          onRestore={() => {
            setShowBackendBanner(true);
            setShowWeatherBanner(true);
          }}
        />
      )}
      
      {/* Individual Status Banners */}
      {showBackendBanner && (
        <BackendStatusBanner 
          onClose={() => setShowBackendBanner(false)}
          onStatusChange={setBackendConnected}
          hasStatusBar={hasStatusBar}
        />
      )}
      {showWeatherBanner && (
        <WeatherStatusBanner 
          isRealWeather={weather?.isRealData || false}
          onClose={() => setShowWeatherBanner(false)}
          hasStatusBar={hasStatusBar}
          hasBackendBanner={showBackendBanner}
        />
      )}
      
      {/* Header */}
      <header className={`bg-black shadow-md sticky ${headerTop} z-40 transition-all duration-300`}>
        <div className={`max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 transition-all duration-300 ${isScrolled ? 'py-2' : 'py-2 sm:py-3'}`}>
          <div className="flex items-center justify-between gap-2 sm:gap-4">
            <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-shrink">
              <Image 
                src="/images/honeygo-logo.png" 
                alt="HoneyGo Logo" 
                width={isScrolled ? 32 : 40} 
                height={isScrolled ? 32 : 40}
                className="rounded-lg flex-shrink-0 transition-all duration-300 w-8 h-8 sm:w-10 sm:h-10"
              />
              <div className="min-w-0">
                <div className="flex items-center gap-2 sm:gap-3">
                  <h1 className={`font-bold text-white transition-all duration-300 ${isScrolled ? 'text-lg sm:text-xl' : 'text-lg sm:text-xl md:text-2xl'} truncate`}>
                    HoneyGo
                  </h1>
                  {!isScrolled && (
                    <span className="px-2 font-semibold bg-[#FF6A13] text-white rounded-full py-0.5 text-xs hidden sm:inline-block">
                      v1.0.0
                    </span>
                  )}
                </div>
                {!isScrolled && (
                  <p className="text-xs sm:text-sm text-gray-400 hidden sm:block">
                    AI-Powered Pricing Platform
                  </p>
                )}
              </div>
            </div>
            <div className="flex items-center gap-2 sm:gap-4 lg:gap-6 flex-shrink-0">
              {!isScrolled && (
                <nav className="flex items-center gap-2 sm:gap-3 lg:gap-4">
                  <Link
                    href="/"
                    className="text-sm sm:text-base text-white border-b-2 border-[#FF6A13] pb-0.5 sm:pb-1 transition-colors font-medium whitespace-nowrap"
                  >
                    Pricing
                  </Link>
                  <Link
                    href="/surge-pricing"
                    className="text-sm sm:text-base text-gray-300 hover:text-white transition-colors font-medium whitespace-nowrap"
                  >
                    Surge Pricing
                  </Link>
                </nav>
              )}
              {!isScrolled && (
                <div className="text-right border-l border-gray-700 pl-2 sm:pl-4 lg:pl-6 hidden md:block">
                  <p className="text-xs text-gray-400">Powered by</p>
                  <p className="text-sm lg:text-base font-semibold text-[#FF6A13]">
                    Honeywell AI
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Content Area with Gradient Background */}
      <div className="bg-gradient-to-br from-gray-50 via-white to-gray-100 pt-12 sm:pt-16 md:pt-20">
        {/* Hero Section */}
        <HeroSection />

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Action Bar */}
        <div className="mb-6 flex justify-end items-center gap-3">
          <button
            onClick={() => executiveAlertRef.current?.triggerAlert()}
            className="p-3 bg-white hover:bg-gray-50 border-2 border-gray-300 hover:border-gray-400 rounded-xl transition-all duration-300 flex items-center justify-center shadow-md hover:shadow-lg"
            title="Trigger Executive Alert"
            aria-label="Trigger Executive Alert"
          >
            <svg className="w-5 h-5 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
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
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <DemandThermometerCard demand={marketConditions.currentDemand as 'low' | 'medium' | 'high' | 'surge'} />
            <AvailableDriversCard count={marketConditions.availableDrivers} />
            <ActiveRidesCard count={marketConditions.activeRides} />
            <div className={`text-center p-4 bg-gradient-to-br rounded-xl border-2 relative ${
              marketConditions.weatherType === 'storm' ? 'from-red-50 to-orange-50 border-red-300' :
              marketConditions.weatherType === 'snow' ? 'from-blue-50 to-cyan-50 border-blue-300' :
              marketConditions.weatherType === 'rain' ? 'from-blue-50 to-gray-50 border-blue-200' :
              marketConditions.weatherType === 'fog' ? 'from-gray-100 to-gray-50 border-gray-300' :
              marketConditions.weatherType === 'clouds' ? 'from-gray-50 to-white border-gray-300' :
              'from-yellow-50 to-white border-yellow-200'
            }`} suppressHydrationWarning>
              {weather && weather.isRealData && (
                <div className="absolute top-1 right-1">
                  <span className="inline-flex items-center px-1.5 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800 border border-green-300">
                    🌐 Live
                  </span>
                </div>
              )}
              <p className="text-xs font-semibold text-gray-500 mb-2 uppercase tracking-wide flex items-center justify-center gap-1" suppressHydrationWarning>
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
              }`} suppressHydrationWarning>
                {marketConditions.weatherCondition}
              </p>
              {weather && weather.location && (
                <p className="text-xs text-gray-500 mt-1" suppressHydrationWarning>
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
                <div className="relative">
                  <button
                    onClick={() => setShowSchedulePicker(!showSchedulePicker)}
                    className="px-4 py-2.5 bg-white hover:bg-gray-50 text-gray-700 border-2 border-gray-300 hover:border-[#FF6A13] rounded-xl font-semibold transition-all duration-300 shadow-sm hover:shadow-md transform hover:scale-105 flex items-center gap-2"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    Schedule
                    <svg className={`w-3 h-3 transition-transform ${showSchedulePicker ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  
                  {/* Schedule Picker Dropdown */}
                  {showSchedulePicker && (
                    <div className="absolute top-full mt-2 right-0 bg-white rounded-xl shadow-xl border border-gray-200 p-4 z-50 w-72">
                      <p className="text-sm font-semibold text-gray-700 mb-3">Select Pickup Date & Time</p>
                      <input
                        type="datetime-local"
                        value={scheduledDateTime}
                        onChange={(e) => setScheduledDateTime(e.target.value)}
                        min={new Date().toISOString().slice(0, 16)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg text-gray-700 focus:ring-2 focus:ring-[#FF6A13] focus:border-[#FF6A13] mb-3"
                      />
                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            if (scheduledDateTime) {
                              handleAddRandomRide(true, scheduledDateTime);
                            }
                          }}
                          disabled={!scheduledDateTime}
                          className={`flex-1 px-3 py-2 rounded-lg font-semibold text-sm transition-all ${
                            scheduledDateTime 
                              ? 'bg-[#FF6A13] text-white hover:bg-[#E55A0A]' 
                              : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                          }`}
                        >
                          Schedule Ride
                        </button>
                        <button
                          onClick={() => handleAddRandomRide(true)}
                          className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg font-semibold text-sm transition-all"
                        >
                          Random
                        </button>
                      </div>
                      <p className="text-xs text-gray-500 mt-2">
                        💡 Tip: Schedule for night (10PM-6AM) to see lower AI confidence
                      </p>
                    </div>
                  )}
                </div>
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

        {/* Footer Info - Dynamic based on connection status */}
        <div className={`mt-8 rounded-xl p-6 border ${
          backendConnected 
            ? 'bg-green-50 border-green-200' 
            : 'bg-blue-50 border-blue-200'
        }`}>
          <div className="flex items-start gap-3">
            <div className="text-2xl">{backendConnected ? '✅' : 'ℹ️'}</div>
            <div>
              <h3 className={`font-semibold mb-2 ${
                backendConnected ? 'text-green-900' : 'text-blue-900'
              }`}>
                {backendConnected 
                  ? 'Live Mode - Connected to Backend & Database' 
                  : 'Demo Mode - Using Mock Data'}
              </h3>
              <p className={`text-sm ${backendConnected ? 'text-green-800' : 'text-blue-800'}`}>
                {backendConnected 
                  ? 'Real-time AI pricing with LangChain Agent, MongoDB persistence, and ChromaDB RAG. All pricing decisions are saved and affect live statistics.'
                  : 'This frontend is currently running with mock data to demonstrate the UI/UX. Once the backend (FastAPI + LangChain Agent) and databases (MongoDB + ChromaDB) are ready, this will connect to real AI-powered pricing decisions.'}
              </p>
            </div>
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

      {/* ChatBot - Floating Assistant */}
      <ChatBot currentCity={selectedCity} />

      {/* N8n Notifications - Pop-out notifications for workflow events */}
      <N8nNotificationContainer />

      {/* Executive Alert Notification - n8n executive alerts */}
      <ExecutiveAlertNotification ref={executiveAlertRef} />

      {/* Test Alert Button - Demo trigger for executive notifications */}
      <button
        onClick={() => executiveAlertRef.current?.triggerAlert()}
        className="fixed bottom-44 right-6 z-40 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-4 py-3 rounded-full shadow-lg hover:shadow-xl transition-all duration-200 flex items-center gap-2 group"
        title="Trigger Demo Executive Alert"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span className="text-sm font-medium">Test Alert</span>
      </button>
    </main>
  );
}
