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
    'sunny': 'clear',
    'clouds': 'cloudy',
    'cloudy': 'cloudy',
    'overcast': 'cloudy',
    'rain': 'rainy',
    'drizzle': 'rainy',
    'storm': 'stormy',
    'thunderstorm': 'stormy',
    'snow': 'snowy',
    'fog': 'cloudy',
    'mist': 'cloudy',
    'haze': 'cloudy',
  };
  
  // Case-insensitive matching
  const normalized = weatherType?.toLowerCase() || 'clear';
  return weatherMap[normalized] || 'cloudy'; // Default to cloudy instead of clear for unknown
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
 * Parse AI reasoning into an array of bullet points
 * Handles multiple formats: numbered lists, newline-separated, or period-separated
 */
function parseReasoningToArray(reasoning: string): string[] {
  // First, try to split by newlines (handles numbered lists like "1. reason\n2. reason")
  const lines = reasoning.split('\n').map(line => line.trim()).filter(line => line.length > 0);
  
  if (lines.length > 1) {
    // Multiple lines - clean up numbered prefixes like "1.", "2.", "-", "•"
    return lines.map(line => {
      // Remove leading numbers, bullets, dashes
      const cleaned = line.replace(/^[\d]+\.\s*/, '')  // "1. " -> ""
                          .replace(/^[-•*]\s*/, '')    // "- " or "• " -> ""
                          .trim();
      return cleaned.endsWith('.') ? cleaned : cleaned + '.';
    }).filter(line => line.length > 1); // Filter out empty lines that became just "."
  }
  
  // Single line/paragraph - split by period-space or period followed by capital letter
  const sentences = reasoning
    .split(/\.\s+(?=[A-Z])/)  // Split on ". " followed by capital letter
    .map(s => s.trim())
    .filter(s => s.length > 0)
    .map(s => s.endsWith('.') ? s : s + '.');
  
  return sentences.length > 0 ? sentences : [reasoning];
}

/**
 * Convert backend PricingResponse to frontend PricingResult
 */
export function backendToFrontendResult(
  backendResponse: BackendPricingResponse,
  processingTime: number,
  city: string,
  loyaltyTier?: string
): PricingResult {
  // Import loyalty functions (Jason's fix for loyalty tier pricing)
  const { getLoyaltyDiscount, getLoyaltyBadge } = require('./mockData');
  
  // Apply loyalty discount if provided
  const loyaltyDiscount = loyaltyTier ? getLoyaltyDiscount(loyaltyTier) : 0;
  const priceBeforeDiscount = backendResponse.final_price;
  const finalPrice = priceBeforeDiscount * (1 - loyaltyDiscount);
  
  // Split reasoning string into array - handles multiple formats (our improved parser)
  const reasoningArray = parseReasoningToArray(backendResponse.reasoning);

  // Add loyalty discount to reasoning if applicable
  if (loyaltyTier && loyaltyTier !== 'new' && loyaltyDiscount > 0) {
    const loyaltyNote = `${getLoyaltyBadge(loyaltyTier)} ${loyaltyTier.toUpperCase()} member: ${(loyaltyDiscount * 100).toFixed(0)}% loyalty discount applied ($${(priceBeforeDiscount - finalPrice).toFixed(2)} saved).`;
    reasoningArray.push(loyaltyNote);
  }

  // Calculate driver earnings (80% of final price after loyalty discount)
  const driverEarnings = finalPrice * 0.8;

  // Calculate competitor pricing (use original price for fair comparison)
  const competitorPricing = calculateCompetitorPrices(
    priceBeforeDiscount,
    city
  );

  return {
    basePrice: backendResponse.base_price,
    dynamicPrice: parseFloat(finalPrice.toFixed(2)),
    surgeMultiplier: backendResponse.surge_multiplier,
    driverEarnings: parseFloat(driverEarnings.toFixed(2)),
    reasoning: reasoningArray,
    confidence: backendResponse.confidence_score || 0.75,
    processingTime: processingTime,
    competitorPricing: competitorPricing,
    savedToDb: backendResponse.metadata?.saved_to_db || false,
    rideId: backendResponse.metadata?.ride_id,
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
  weatherType?: string,
  demandLevel?: string
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
    
    // Convert backend format to frontend format (with loyalty tier)
    const frontendResult = backendToFrontendResult(
      backendResponse,
      processingTime,
      ride.city,
      ride.loyaltyTier  // Pass loyalty tier for discount calculation
    );
    
    console.log('✅ Frontend result:', frontendResult);
    
    return frontendResult;
    
  } catch (error) {
    console.error('❌ Backend pricing failed, falling back to mock:', error);
    
    // Fallback to mock data if backend fails
    const { simulateAIPricing } = await import('./mockData');
    return simulateAIPricing(ride.id, ride, weatherType, demandLevel);
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

