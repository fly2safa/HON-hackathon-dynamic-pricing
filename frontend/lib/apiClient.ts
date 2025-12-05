/**
 * API Client for HoneyGo Backend
 * 
 * Handles HTTP communication with the FastAPI backend.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export interface BackendPricingRequest {
  pickup_location: string;
  dropoff_location: string;
  distance_km: number;  // Note: kilometers, not miles!
  customer_id: string;
  time_of_day: string;  // "morning", "afternoon", "evening", "night"
  weather_condition?: string;
}

export interface BackendPricingResponse {
  base_price: number;
  surge_multiplier: number;
  final_price: number;
  reasoning: string;
  confidence_score?: number;
  agent_trace_url?: string;
  metadata: Record<string, any>;
}

export interface BackendRideRequest extends BackendPricingRequest {
  // Same as PricingRequest for now
}

export interface BackendRideResponse {
  ride_id: string;
  pickup_location: string;
  dropoff_location: string;
  distance_km: number;
  customer_id: string;
  base_price: number;
  surge_multiplier: number;
  final_price: number;
  reasoning: string;
  confidence_score: number;
  created_at: string;
}

/**
 * Calculate pricing for a ride (quote only, no DB save)
 */
export async function calculatePricing(
  request: BackendPricingRequest
): Promise<BackendPricingResponse> {
  const response = await fetch(`${BACKEND_URL}/api/v1/pricing/calculate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Pricing API error (${response.status}): ${errorText}`);
  }

  return response.json();
}

/**
 * Create a ride with pricing (saves to MongoDB)
 */
export async function createRide(
  request: BackendRideRequest
): Promise<BackendRideResponse> {
  const response = await fetch(`${BACKEND_URL}/api/v1/rides/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Ride creation error (${response.status}): ${errorText}`);
  }

  return response.json();
}

/**
 * Get ride details by ID
 */
export async function getRide(rideId: string): Promise<BackendRideResponse> {
  const response = await fetch(`${BACKEND_URL}/api/v1/rides/${rideId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Get ride error (${response.status}): ${errorText}`);
  }

  return response.json();
}

/**
 * Get customer ride history
 */
export async function getCustomerRides(
  customerId: string,
  limit: number = 10,
  skip: number = 0
): Promise<any[]> {
  const response = await fetch(
    `${BACKEND_URL}/api/v1/rides/customer/${customerId}?limit=${limit}&skip=${skip}`,
    {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Get customer rides error (${response.status}): ${errorText}`);
  }

  return response.json();
}

/**
 * Get pricing factors
 */
export async function getPricingFactors(): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/api/v1/pricing/factors`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Get pricing factors error (${response.status}): ${errorText}`);
  }

  return response.json();
}

/**
 * Health check
 */
export async function healthCheck(): Promise<{ status: string }> {
  const response = await fetch(`${BACKEND_URL}/health`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Chat API - Natural Language Query Interface
 */
export interface ChatRequest {
  message: string;
  conversation_id?: string;
  context?: {
    current_city?: string;
    current_ride?: string;
    current_weather?: {
      temperature: number;
      conditions: string;
      weather_type: string;
      is_real_data: boolean;
    };
  };
}

export interface ChatResponse {
  response: string;
  data?: {
    type: string;
    count?: number;
    avg_price?: number;
    [key: string]: any;
  };
  suggestions?: string[];
  confidence: number;
}

/**
 * Send a chat message to the HoneyGo AI assistant
 */
export async function sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(`${BACKEND_URL}/api/v1/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Chat API error (${response.status}): ${errorText}`);
  }

  return response.json();
}

