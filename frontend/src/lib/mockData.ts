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

// Sample market conditions
export const mockMarketConditions: MarketConditions = {
  currentDemand: 'high',
  availableDrivers: 42,
  activeRides: 87,
  weatherCondition: 'Clear, 72°F',
  trafficLevel: 'moderate',
};

// Simulate AI processing with realistic delays
export const simulateAIPricing = async (rideId: string): Promise<PricingResult> => {
  // Simulate processing time (2-4 seconds)
  const processingTime = 2000 + Math.random() * 2000;
  await new Promise(resolve => setTimeout(resolve, processingTime));
  
  return mockPricingResults[rideId] || mockPricingResults['ride-001'];
};

// Generate random ride request
export const generateRandomRide = (): RideRequest => {
  const locations = [
    { pickup: 'Downtown Phoenix', dropoff: 'Camelback Mountain' },
    { pickup: 'Mesa Riverview', dropoff: 'Tempe Marketplace' },
    { pickup: 'Glendale Arena', dropoff: 'Westgate Entertainment' },
    { pickup: 'Chandler Fashion Center', dropoff: 'Intel Campus' },
  ];
  
  const location = locations[Math.floor(Math.random() * locations.length)];
  const distance = 3 + Math.random() * 15;
  const duration = Math.ceil(distance * 2.5);
  
  return {
    id: `ride-${Date.now()}`,
    pickupLocation: location.pickup,
    dropoffLocation: location.dropoff,
    distance: parseFloat(distance.toFixed(1)),
    estimatedDuration: duration,
    requestTime: new Date().toISOString(),
    passengerCount: Math.floor(Math.random() * 4) + 1,
  };
};

