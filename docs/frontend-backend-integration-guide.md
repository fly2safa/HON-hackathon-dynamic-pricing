# Frontend-Backend Integration Guide

**Created:** Dec 2, 2025  
**Author:** Safa (Role 2 & 4)  
**Purpose:** Guide for integrating the Next.js frontend with FastAPI backend

---

## Overview

This document outlines the differences between the current frontend mock data structure and the backend API structure, and provides a step-by-step guide for integration.

---

## Key Differences Between Frontend & Backend

### 1. **API Endpoint Structure**

**Backend Endpoints:**
- `POST /api/v1/pricing/calculate` - Calculate pricing (quote only, no DB save)
- `POST /api/v1/rides/` - Create ride with pricing (saves to MongoDB)
- `GET /api/v1/rides/{ride_id}` - Get ride details
- `GET /api/v1/rides/customer/{customer_id}` - Get customer ride history
- `GET /api/v1/pricing/factors` - Get current pricing factors

**Frontend Currently Uses:**
- Mock function `simulateAIPricing(rideId, ride)` in `frontend/lib/mockData.ts`

### 2. **Data Structure Differences**

#### Frontend RideRequest (mockData.ts)
```typescript
interface RideRequest {
  id: string;
  pickupLocation: string;
  dropoffLocation: string;
  city: string;
  distance: number;              // in MILES
  estimatedDuration: number;
  requestTime: string;
  passengerCount: number;
  isScheduled?: boolean;
  scheduledTime?: string;
  loyaltyTier?: LoyaltyTier;     // Frontend-specific
}
```

#### Backend PricingRequest (models/pricing.py)
```python
class PricingRequest(BaseModel):
    pickup_location: str
    dropoff_location: str
    distance_km: float             # in KILOMETERS (not miles!)
    customer_id: str
    time_of_day: str              # "morning", "afternoon", "evening", "night"
    weather_condition: Optional[str]
    
    # MISSING in backend:
    # - city
    # - passengerCount
    # - isScheduled/scheduledTime
    # - loyaltyTier
```

#### Frontend PricingResult (mockData.ts)
```typescript
interface PricingResult {
  basePrice: number;
  dynamicPrice: number;
  surgeMultiplier: number;
  driverEarnings: number;        // Frontend-specific
  reasoning: string[];           // Array of strings
  confidence: number;
  processingTime: number;
  competitorPricing?: {...};     // Frontend-specific
}
```

#### Backend PricingResponse (models/pricing.py)
```python
class PricingResponse(BaseModel):
    base_price: float
    surge_multiplier: float
    final_price: float
    reasoning: str                 # Single string (not array!)
    confidence_score: Optional[float]
    agent_trace_url: Optional[str]
    metadata: Dict[str, Any]
    
    # MISSING in backend:
    # - driverEarnings
    # - processingTime
    # - competitorPricing
```

---

## Integration Strategy

### Phase 1: Minimal Changes (Quick Integration)

**Goal:** Get frontend talking to backend with minimal changes to both sides.

#### Step 1: Create API Client Service

Create `frontend/lib/apiClient.ts`:

```typescript
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

export interface BackendPricingRequest {
  pickup_location: string;
  dropoff_location: string;
  distance_km: number;  // Convert from miles!
  customer_id: string;
  time_of_day: string;
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
    throw new Error(`Pricing API error: ${response.statusText}`);
  }

  return response.json();
}

export async function createRide(
  request: BackendPricingRequest
): Promise<any> {
  const response = await fetch(`${BACKEND_URL}/api/v1/rides/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`Ride creation error: ${response.statusText}`);
  }

  return response.json();
}
```

#### Step 2: Create Adapter Function

Create `frontend/lib/dataAdapter.ts`:

```typescript
import { RideRequest, PricingResult } from './mockData';
import { BackendPricingRequest, BackendPricingResponse, calculatePricing } from './apiClient';

// Convert miles to kilometers
function milesToKm(miles: number): number {
  return miles * 1.60934;
}

// Determine time of day from current time or scheduled time
function getTimeOfDay(date: Date = new Date()): string {
  const hour = date.getHours();
  
  if (hour >= 7 && hour < 12) return 'morning';
  if (hour >= 12 && hour < 17) return 'afternoon';
  if (hour >= 17 && hour < 21) return 'evening';
  return 'night';
}

// Convert frontend RideRequest to backend PricingRequest
export function frontendToBackendRequest(
  ride: RideRequest,
  weatherCondition?: string
): BackendPricingRequest {
  return {
    pickup_location: ride.pickupLocation,
    dropoff_location: ride.dropoffLocation,
    distance_km: milesToKm(ride.distance),
    customer_id: `CUST_${ride.id}`, // Generate customer ID from ride ID
    time_of_day: getTimeOfDay(
      ride.isScheduled && ride.scheduledTime 
        ? new Date(ride.scheduledTime) 
        : new Date()
    ),
    weather_condition: weatherCondition,
  };
}

// Convert backend PricingResponse to frontend PricingResult
export function backendToFrontendResult(
  backendResponse: BackendPricingResponse,
  processingTime: number,
  city: string
): PricingResult {
  // Split reasoning string into array (if it contains periods)
  const reasoningArray = backendResponse.reasoning
    .split('. ')
    .filter(r => r.trim().length > 0)
    .map(r => r.trim().endsWith('.') ? r.trim() : r.trim() + '.');

  // Calculate driver earnings (80% of final price)
  const driverEarnings = backendResponse.final_price * 0.8;

  // Calculate competitor pricing (mock for now)
  const competitorPricing = calculateCompetitorPrices(
    backendResponse.final_price,
    city
  );

  return {
    basePrice: backendResponse.base_price,
    dynamicPrice: backendResponse.final_price,
    surgeMultiplier: backendResponse.surge_multiplier,
    driverEarnings: driverEarnings,
    reasoning: reasoningArray,
    confidence: backendResponse.confidence_score || 0.75,
    processingTime: processingTime,
    competitorPricing: competitorPricing,
  };
}

// Helper function to calculate competitor prices (same as mockData.ts)
function calculateCompetitorPrices(ourPrice: number, city: string) {
  const uberPrice = ourPrice * (1.05 + Math.random() * 0.1);
  const lyftPrice = ourPrice * (1.03 + Math.random() * 0.08);
  
  const hasWaymo = city === 'Phoenix' || city === 'San Francisco';
  const waymoPrice = hasWaymo ? ourPrice * (1.08 + Math.random() * 0.12) : undefined;
  
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

// Main integration function - replaces simulateAIPricing
export async function calculatePricingWithBackend(
  ride: RideRequest,
  weatherCondition?: string
): Promise<PricingResult> {
  const startTime = Date.now();
  
  try {
    // Convert frontend format to backend format
    const backendRequest = frontendToBackendRequest(ride, weatherCondition);
    
    // Call backend API
    const backendResponse = await calculatePricing(backendRequest);
    
    // Calculate processing time
    const processingTime = (Date.now() - startTime) / 1000;
    
    // Convert backend format to frontend format
    const frontendResult = backendToFrontendResult(
      backendResponse,
      processingTime,
      ride.city
    );
    
    return frontendResult;
    
  } catch (error) {
    console.error('Backend pricing failed, falling back to mock:', error);
    
    // Fallback to mock data if backend fails
    const { simulateAIPricing } = await import('./mockData');
    return simulateAIPricing(ride.id, ride);
  }
}
```

#### Step 3: Update Frontend to Use Backend

In `frontend/app/page.tsx`, replace the mock function call:

```typescript
// OLD (Mock):
import { simulateAIPricing } from '@/lib/mockData';
const result = await simulateAIPricing(ride.id, ride);

// NEW (Backend):
import { calculatePricingWithBackend } from '@/lib/dataAdapter';
const result = await calculatePricingWithBackend(ride, marketConditions.weatherType);
```

#### Step 4: Add Environment Variable

In `frontend/.env.local`:
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

### Phase 2: Backend Enhancements (Optional)

To fully support frontend features, the backend would need these enhancements:

#### 1. Add Missing Fields to PricingRequest

```python
class PricingRequest(BaseModel):
    # ... existing fields ...
    city: Optional[str] = None
    passenger_count: Optional[int] = 1
    is_scheduled: Optional[bool] = False
    scheduled_time: Optional[datetime] = None
    loyalty_tier: Optional[str] = None  # "new", "bronze", "silver", "gold", "platinum"
```

#### 2. Add Missing Fields to PricingResponse

```python
class PricingResponse(BaseModel):
    # ... existing fields ...
    driver_earnings: Optional[float] = None
    processing_time: Optional[float] = None
    competitor_pricing: Optional[Dict[str, Any]] = None
```

#### 3. Update Pricing Logic

In `backend/routers/pricing.py`, update `calculate_pricing()` to:
- Consider `passenger_count` (larger vehicles for 3+ passengers)
- Consider `loyalty_tier` (apply discounts)
- Consider `city` (different base rates per market)
- Calculate `driver_earnings` (80% of final price)
- Return `competitor_pricing` (mock comparison)

---

## Testing Strategy

### 1. Test Backend Independently

```bash
# Start backend
cd backend
uvicorn main:app --reload

# Test with curl
curl -X POST http://localhost:8000/api/v1/pricing/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_location": "Phoenix Sky Harbor Airport",
    "dropoff_location": "Arizona State University",
    "distance_km": 13.68,
    "customer_id": "CUST_001",
    "time_of_day": "evening",
    "weather_condition": "clear"
  }'
```

### 2. Test Frontend with Backend

```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Open browser: http://localhost:3000
# Click "Calculate AI Price" and check browser console for API calls
```

### 3. Test Fallback to Mock

```bash
# Stop backend
# Frontend should automatically fall back to mock data
```

---

## Current Status & Next Steps

### ✅ Completed
- Backend API structure (Dari)
- Frontend UI with mock data (Safa)
- MongoDB integration (Jason)

### 🔄 In Progress
- LangChain agent implementation (Safa - Dec 3)
- ChromaDB RAG implementation (Safa - Dec 3)

### 📋 TODO for Integration
1. **Create `apiClient.ts`** - API communication layer
2. **Create `dataAdapter.ts`** - Data format conversion
3. **Update `page.tsx`** - Switch from mock to backend
4. **Add `.env.local`** - Backend URL configuration
5. **Test integration** - Verify end-to-end flow
6. **(Optional) Enhance backend** - Add missing fields for full feature parity

---

## Timeline

- **Dec 2 (Today):** Create integration layer (`apiClient.ts`, `dataAdapter.ts`)
- **Dec 2 (Today):** Test basic integration with current backend
- **Dec 3:** Integrate LangChain agent with backend
- **Dec 3:** Add ChromaDB RAG to backend
- **Dec 4:** Full end-to-end testing with all features

---

## Notes

### Why Dari Said "Not Straightforward"

1. **Unit Mismatch:** Frontend uses miles, backend uses kilometers
2. **Data Structure:** Different field names (camelCase vs snake_case)
3. **Missing Fields:** Backend doesn't support all frontend features yet
4. **Reasoning Format:** Backend returns string, frontend expects array
5. **No Competitor Pricing:** Backend doesn't calculate competitor comparison
6. **No Loyalty Tiers:** Backend doesn't have loyalty discount logic yet

### Solution

The adapter pattern (`dataAdapter.ts`) handles all these differences transparently, allowing both frontend and backend to maintain their current structures while still working together.

---

## Questions?

Contact Safa or Dari for clarification on integration details.

