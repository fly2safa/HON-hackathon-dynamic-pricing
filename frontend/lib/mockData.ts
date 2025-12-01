// Mock data for HoneyGo frontend development
// This allows frontend development to proceed independently of backend

export interface RideRequest {
  id: string;
  pickupLocation: string;
  dropoffLocation: string;
  distance: number; // in miles
  estimatedDuration: number; // in minutes
  requestTime: string;
  passengerCount: number;
  isScheduled?: boolean;
  scheduledTime?: string;
}

export interface PricingResult {
  basePrice: number;
  dynamicPrice: number;
  surgeMultiplier: number;
  driverEarnings: number;
  reasoning: string[];
  confidence: number;
  processingTime: number;
}

export interface MarketConditions {
  currentDemand: 'low' | 'medium' | 'high' | 'surge';
  availableDrivers: number;
  activeRides: number;
  weatherCondition: string;
  weatherType: 'clear' | 'rain' | 'storm' | 'snow' | 'fog';
  weatherSeverity: 'none' | 'light' | 'moderate' | 'severe';
  trafficLevel: 'light' | 'moderate' | 'heavy';
}

// Sample ride requests
export const mockRideRequests: RideRequest[] = [
  {
    id: 'ride-001',
    pickupLocation: 'Phoenix Sky Harbor Airport',
    dropoffLocation: 'Arizona State University',
    distance: 8.5,
    estimatedDuration: 18,
    requestTime: new Date().toISOString(),
    passengerCount: 1,
  },
  {
    id: 'ride-002',
    pickupLocation: 'Scottsdale Fashion Square',
    dropoffLocation: 'Old Town Scottsdale',
    distance: 2.3,
    estimatedDuration: 8,
    requestTime: new Date().toISOString(),
    passengerCount: 2,
  },
  {
    id: 'ride-003',
    pickupLocation: 'Tempe Town Lake',
    dropoffLocation: 'Chase Field',
    distance: 5.7,
    estimatedDuration: 15,
    requestTime: new Date().toISOString(),
    passengerCount: 4,
  },
];

// Sample pricing results
export const mockPricingResults: Record<string, PricingResult> = {
  'ride-001': {
    basePrice: 18.50,
    dynamicPrice: 27.75,
    surgeMultiplier: 1.5,
    driverEarnings: 22.20,
    reasoning: [
      'High demand detected near airport area',
      'Limited driver availability (15 drivers within 2 miles)',
      'Peak travel time (5:30 PM)',
      'Weather conditions: Clear',
      'Historical data shows 1.5x surge typical for this route/time',
    ],
    confidence: 0.92,
    processingTime: 2.3,
  },
  'ride-002': {
    basePrice: 8.00,
    dynamicPrice: 8.00,
    surgeMultiplier: 1.0,
    driverEarnings: 6.40,
    reasoning: [
      'Normal demand in Scottsdale area',
      'Adequate driver availability (28 drivers within 2 miles)',
      'Short distance ride',
      'Off-peak hours',
      'No surge pricing applied',
    ],
    confidence: 0.88,
    processingTime: 1.8,
  },
  'ride-003': {
    basePrice: 14.00,
    dynamicPrice: 19.60,
    surgeMultiplier: 1.4,
    driverEarnings: 15.68,
    reasoning: [
      'Event detected: Baseball game at Chase Field',
      'Moderate driver availability (22 drivers within 2 miles)',
      'Multiple passenger ride (4 passengers)',
      'Increased demand due to event',
      'Driver incentive applied for event coverage',
    ],
    confidence: 0.85,
    processingTime: 2.7,
  },
};

// Generate random weather conditions
const generateWeatherConditions = (forScheduled: boolean = false) => {
  const weatherOptions = [
    { type: 'clear' as const, severity: 'none' as const, display: 'Clear, 72°F', multiplier: 1.0 },
    { type: 'rain' as const, severity: 'light' as const, display: 'Light Rain, 65°F', multiplier: 1.1 },
    { type: 'rain' as const, severity: 'moderate' as const, display: 'Heavy Rain, 58°F', multiplier: 1.25 },
    { type: 'storm' as const, severity: 'severe' as const, display: 'Thunderstorm, 55°F', multiplier: 1.5 },
    { type: 'snow' as const, severity: 'moderate' as const, display: 'Snow, 28°F', multiplier: 1.4 },
    { type: 'fog' as const, severity: 'moderate' as const, display: 'Dense Fog, 50°F', multiplier: 1.2 },
  ];
  
  // For scheduled rides: 50/50 chance of weather changes
  // For current weather: 70% clear, 30% other (more stable)
  const clearThreshold = forScheduled ? 0.5 : 0.7;
  const random = Math.random();
  
  if (random < clearThreshold) {
    return weatherOptions[0]; // Clear
  } else {
    return weatherOptions[Math.floor(Math.random() * (weatherOptions.length - 1)) + 1];
  }
};

// Sample market conditions (regenerate on each page load for variety)
const currentWeather = generateWeatherConditions();
export const mockMarketConditions: MarketConditions = {
  currentDemand: 'high',
  availableDrivers: 42,
  activeRides: 87,
  weatherCondition: currentWeather.display,
  weatherType: currentWeather.type,
  weatherSeverity: currentWeather.severity,
  trafficLevel: 'moderate',
};

// Export weather multiplier for pricing
export const getWeatherMultiplier = () => {
  const weatherOptions = [
    { type: 'clear', multiplier: 1.0 },
    { type: 'rain', multiplier: mockMarketConditions.weatherSeverity === 'light' ? 1.1 : 1.25 },
    { type: 'storm', multiplier: 1.5 },
    { type: 'snow', multiplier: 1.4 },
    { type: 'fog', multiplier: 1.2 },
  ];
  
  return weatherOptions.find(w => w.type === mockMarketConditions.weatherType)?.multiplier || 1.0;
};

// Simulate AI processing with realistic delays
// NOTE: When backend is ready, this will call:
// - FastAPI endpoint: POST /api/pricing/calculate
// - Backend will fetch real weather from OpenWeatherMap API
// - For scheduled rides, backend will use weather forecast API
// - MongoDB will store historical pricing decisions
// - ChromaDB will provide similar context for better AI reasoning
export const simulateAIPricing = async (rideId: string, ride?: RideRequest): Promise<PricingResult> => {
  // Record actual start time
  const startTime = Date.now();
  
  // Simulate processing time (2-4 seconds)
  const processingTime = 2000 + Math.random() * 2000;
  await new Promise(resolve => setTimeout(resolve, processingTime));
  
  // Calculate actual elapsed time
  const actualProcessingTime = (Date.now() - startTime) / 1000;
  
  // If we have a predefined result, use it but update processing time
  if (mockPricingResults[rideId]) {
    return {
      ...mockPricingResults[rideId],
      processingTime: parseFloat(actualProcessingTime.toFixed(1)), // Use actual time
    };
  }
  
  // Otherwise, generate dynamic pricing based on ride characteristics
  if (ride) {
    const basePrice = 5 + (ride.distance * 2.5) + (ride.passengerCount * 1.5);
    
    // Random surge multiplier based on "market conditions"
    const baseSurge = 1.0 + (Math.random() * 0.5); // 1.0x to 1.5x
    
    // Determine weather for this specific ride
    let rideWeather;
    if (ride.isScheduled) {
      // Scheduled rides: predict future weather (50% chance of change)
      rideWeather = generateWeatherConditions(true);
    } else {
      // Immediate rides: use current weather
      rideWeather = {
        type: mockMarketConditions.weatherType,
        severity: mockMarketConditions.weatherSeverity,
        display: mockMarketConditions.weatherCondition,
        multiplier: getWeatherMultiplier()
      };
    }
    
    const weatherMultiplier = rideWeather.multiplier;
    const surgeMultiplier = baseSurge * weatherMultiplier;
    
    const dynamicPrice = basePrice * surgeMultiplier;
    
    // Driver gets 80% of dynamic price
    const driverEarnings = dynamicPrice * 0.8;
    
    // Generate realistic reasoning
    const demandLevel = surgeMultiplier > 1.4 ? 'High' : surgeMultiplier > 1.2 ? 'Moderate' : 'Normal';
    const timeOfDay = new Date().getHours();
    const isPeakHour = (timeOfDay >= 7 && timeOfDay <= 9) || (timeOfDay >= 16 && timeOfDay <= 19);
    
    const weatherPrefix = ride.isScheduled ? 'Predicted weather: ' : 'Current weather: ';
    const weatherImpact = 
      rideWeather.type === 'storm' ? weatherPrefix + 'Severe thunderstorm - significant price increase for driver safety' :
      rideWeather.type === 'snow' ? weatherPrefix + 'Snow conditions - higher pricing due to hazardous driving' :
      rideWeather.type === 'rain' && rideWeather.severity === 'moderate' ? weatherPrefix + 'Heavy rain - increased pricing for difficult driving conditions' :
      rideWeather.type === 'rain' && rideWeather.severity === 'light' ? weatherPrefix + 'Light rain - slight price adjustment' :
      rideWeather.type === 'fog' ? weatherPrefix + 'Dense fog - reduced visibility increases risk' :
      weatherPrefix + 'Clear conditions - standard pricing';
    
    const reasoning = [
      `${demandLevel} demand detected in the area`,
      `Distance: ${ride.distance} miles requires ${ride.estimatedDuration} minutes`,
      `${ride.passengerCount} passenger${ride.passengerCount > 1 ? 's' : ''} - ${ride.passengerCount > 2 ? 'larger vehicle needed' : 'standard vehicle'}`,
      weatherImpact,
      isPeakHour ? 'Peak travel hours detected' : 'Off-peak hours - moderate demand',
      surgeMultiplier > 1.3 ? `Total surge: ${surgeMultiplier.toFixed(2)}x (includes weather adjustment)` : 'Minimal surge - stable conditions',
    ];
    
    return {
      basePrice: parseFloat(basePrice.toFixed(2)),
      dynamicPrice: parseFloat(dynamicPrice.toFixed(2)),
      surgeMultiplier: parseFloat(surgeMultiplier.toFixed(2)),
      driverEarnings: parseFloat(driverEarnings.toFixed(2)),
      reasoning,
      confidence: 0.82 + (Math.random() * 0.15), // 82-97% confidence
      processingTime: parseFloat(actualProcessingTime.toFixed(1)), // Use actual elapsed time
    };
  }
  
  // Fallback to ride-001 if no ride data provided
  return mockPricingResults['ride-001'];
};

// Generate random ride request
export const generateRandomRide = (scheduled: boolean = false): RideRequest => {
  const locations = [
    { pickup: 'Downtown Phoenix', dropoff: 'Camelback Mountain' },
    { pickup: 'Mesa Riverview', dropoff: 'Tempe Marketplace' },
    { pickup: 'Glendale Arena', dropoff: 'Westgate Entertainment' },
    { pickup: 'Chandler Fashion Center', dropoff: 'Intel Campus' },
  ];
  
  const location = locations[Math.floor(Math.random() * locations.length)];
  const distance = 3 + Math.random() * 15;
  const duration = Math.ceil(distance * 2.5);
  
  const ride: RideRequest = {
    id: `ride-${Date.now()}`,
    pickupLocation: location.pickup,
    dropoffLocation: location.dropoff,
    distance: parseFloat(distance.toFixed(1)),
    estimatedDuration: duration,
    requestTime: new Date().toISOString(),
    passengerCount: Math.floor(Math.random() * 4) + 1,
  };
  
  // If scheduled, add a future time (1-6 hours from now)
  if (scheduled) {
    const hoursAhead = 1 + Math.floor(Math.random() * 5);
    const scheduledDate = new Date();
    scheduledDate.setHours(scheduledDate.getHours() + hoursAhead);
    ride.isScheduled = true;
    ride.scheduledTime = scheduledDate.toISOString();
  }
  
  return ride;
};

