/**
 * Data Adapter for Frontend-Backend Integration
 * 
 * Converts between frontend data structures (mockData.ts) and backend API structures.
 * Handles unit conversions, field name mappings, and format differences.
 */

import { RideRequest, PricingResult } from './mockData';
import { 
  BackendPricingRequest, 
  BackendPricingResponse, 
  calculatePricing 
} from './apiClient';

/**
 * Convert miles to kilometers
 */
function milesToKm(miles: number): number {
  return miles * 1.60934;
}

/**
 * Convert kilometers to miles
 */
function kmToMiles(km: number): number {
  return km / 1.60934;
}

/**
 * Determine time of day from current time or scheduled time
 */
function getTimeOfDay(date: Date = new Date()): string {
  const hour = date.getHours();
  
  if (hour >= 7 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 17) return 'afternoon';
  if (hour >= 17 && hour < 21) return 'evening';
  return 'night';
}

/**
 * Map frontend weather type to backend weather condition
 */
function mapWeatherCondition(weatherType: string): string {
  const weatherMap: Record<string, string> = {
    'clear': 'clear',
    'rain': 'rainy',
    'storm': 'stormy',
    'snow': 'snowy',
    'fog': 'cloudy',
  };
  
  return weatherMap[weatherType] || 'clear';
}

/**
 * Convert frontend RideRequest to backend PricingRequest
 */
export function frontendToBackendRequest(
  ride: RideRequest,
  weatherType?: string
): BackendPricingRequest {
  // Determine time of day
  const timeOfDay = ride.isScheduled && ride.scheduledTime
    ? getTimeOfDay(new Date(ride.scheduledTime))
    : getTimeOfDay();
  
  // Map weather condition
  const weatherCondition = weatherType ? mapWeatherCondition(weatherType) : undefined;
  
  return {
    pickup_location: ride.pickupLocation,
    dropoff_location: ride.dropoffLocation,
    distance_km: milesToKm(ride.distance),
    customer_id: `CUST_${ride.id.replace('ride-', '')}`, // Generate customer ID from ride ID
    time_of_day: timeOfDay,
    weather_condition: weatherCondition,
  };
}

/**
 * Calculate competitor prices (same logic as mockData.ts)
 */
function calculateCompetitorPrices(ourPrice: number, city: string) {
  // Add some randomness to make it realistic
  const uberPrice = ourPrice * (1.05 + Math.random() * 0.1);
  const lyftPrice = ourPrice * (1.03 + Math.random() * 0.08);
  
  // Waymo only available in Phoenix & San Francisco
  const hasWaymo = city === 'Phoenix' || city === 'San Francisco';
  const waymoPrice = hasWaymo ? ourPrice * (1.08 + Math.random() * 0.12) : undefined;
  
  // Calculate average competitor price
  const competitorAvg = hasWaymo 
    ? (uberPrice + lyftPrice + waymoPrice!) / 3
    : (uberPrice + lyftPrice) / 2;
  
  const savings = competitorAvg - ourPrice;
  const savingsPercent = (savings / competitorAvg) * 100;
  
  return {
    uber: parseFloat(uberPrice.toFixed(2)),
    lyft: parseFloat(lyftPrice.toFixed(2)),
    waymo: waymoPrice ? parseFloat(waymoPrice.toFixed(2)) : undefined,
    savings: parseFloat(savings.toFixed(2)),
    savingsPercent: parseFloat(savingsPercent.toFixed(1)),
    hasWaymo,
  };
}

/**
 * Convert backend PricingResponse to frontend PricingResult
 */
export function backendToFrontendResult(
  backendResponse: BackendPricingResponse,
  processingTime: number,
  city: string
): PricingResult {
  // Split reasoning string into array
  // Backend returns single string, frontend expects array
  const reasoningArray = backendResponse.reasoning
    .split('. ')
    .filter(r => r.trim().length > 0)
    .map(r => {
      const trimmed = r.trim();
      return trimmed.endsWith('.') ? trimmed : trimmed + '.';
    });

  // Calculate driver earnings (80% of final price)
  const driverEarnings = backendResponse.final_price * 0.8;

  // Calculate competitor pricing
  const competitorPricing = calculateCompetitorPrices(
    backendResponse.final_price,
    city
  );

  return {
    basePrice: backendResponse.base_price,
    dynamicPrice: backendResponse.final_price,
    surgeMultiplier: backendResponse.surge_multiplier,
    driverEarnings: parseFloat(driverEarnings.toFixed(2)),
    reasoning: reasoningArray,
    confidence: backendResponse.confidence_score || 0.75,
    processingTime: processingTime,
    competitorPricing: competitorPricing,
  };
}

/**
 * Main integration function - replaces simulateAIPricing from mockData.ts
 * 
 * This function:
 * 1. Converts frontend format to backend format
 * 2. Calls backend API
 * 3. Converts backend response to frontend format
 * 4. Falls back to mock data if backend fails
 */
export async function calculatePricingWithBackend(
  ride: RideRequest,
  weatherType?: string
): Promise<PricingResult> {
  const startTime = Date.now();
  
  try {
    // Convert frontend format to backend format
    const backendRequest = frontendToBackendRequest(ride, weatherType);
    
    console.log('🔄 Calling backend API:', backendRequest);
    
    // Call backend API
    const backendResponse = await calculatePricing(backendRequest);
    
    console.log('✅ Backend response:', backendResponse);
    
    // Calculate processing time
    const processingTime = (Date.now() - startTime) / 1000;
    
    // Convert backend format to frontend format
    const frontendResult = backendToFrontendResult(
      backendResponse,
      processingTime,
      ride.city
    );
    
    console.log('✅ Frontend result:', frontendResult);
    
    return frontendResult;
    
  } catch (error) {
    console.error('❌ Backend pricing failed, falling back to mock:', error);
    
    // Fallback to mock data if backend fails
    const { simulateAIPricing } = await import('./mockData');
    return simulateAIPricing(ride.id, ride, weatherType);
  }
}

/**
 * Check if backend is available
 */
export async function isBackendAvailable(): Promise<boolean> {
  try {
    const { healthCheck } = await import('./apiClient');
    const health = await healthCheck();
    return health.status === 'healthy';
  } catch (error) {
    console.warn('Backend health check failed:', error);
    return false;
  }
}

