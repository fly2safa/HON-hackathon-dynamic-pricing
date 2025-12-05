# Frontend Implementation Guide - HoneyGo Dynamic Pricing
## ✅ IMPLEMENTATION STARTED - DEC 1, 2025

**Created**: Nov 29, 2025  
**Updated**: December 1, 2025 (Implementation Day!)  
**For**: Frontend Developer (Jason - Primary, Safa - Backup/Alternative Implementation)  
**Purpose**: Quick reference guide for building frontend with mock data before backend is ready

**Current Status**: 🚀 **IMPLEMENTATION IN PROGRESS** - Safa building alternative frontend version while Jason is tied up with work

---

## 🎯 Why This Approach is Great

### 1. Frontend Development is Independent
You can build the entire UI with **mock data** and it will look identical to the final product. When the backend is ready, you just swap mock data for real API calls.

### 2. Parallel Development
While you build the frontend (Dec 1-2), your teammates can build:
- Backend API (FastAPI)
- LangChain agent
- Database connections
- n8n workflows

Everyone works simultaneously = **faster completion**.

### 3. Early Visual Feedback
Your team can see and critique the UI immediately:
- "Make that button bigger"
- "Change the color scheme"
- "Add a graph here"

No waiting for backend to see if the design works.

### 4. Judges See Progress
If you demo on Dec 5, having a polished UI ready early shows:
- Strong project management
- Professional development practices
- Clear vision of the final product

---

## 🚀 Step-by-Step Implementation (Dec 1 onwards)

### Step 0: Project Setup (12:01 AM - 12:30 AM)

**NOTE**: We already have a `frontend/` folder in the project root. Work within that folder!

```bash
# Navigate to frontend folder
cd frontend

# Create Next.js project in current directory
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --yes

# Install additional dependencies
npm install recharts  # For charts/graphs
npm install lucide-react  # For icons
npm install clsx tailwind-merge  # For styling utilities

# Run dev server
npm run dev
```

**Project Structure**: The frontend is at `Hackathon/frontend/` (not a separate repo)

---

## 📁 Folder Structure to Create

```
Hackathon/
├── frontend/                    # ← You are here!
│   ├── app/
│   │   ├── components/
│   │   │   ├── PricingDashboard.tsx
│   │   │   ├── ReasoningExplainer.tsx
│   │   │   ├── AnalyticsDashboard.tsx
│   │   │   ├── RideInputForm.tsx
│   │   │   ├── AgentStepsVisualization.tsx
│   │   │   └── VoiceFeatures.tsx      # NEW - Voice Input/Output (E1 & E2)
│   │   ├── mock-data/
│   │   │   ├── rides.ts
│   │   │   ├── pricing-decisions.ts
│   │   │   └── analytics.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── page.tsx
│   │   └── layout.tsx
│   ├── public/
│   │   └── honeygo-logo.png
│   └── package.json
├── backend/                     # Backend team (Dari)
├── workflows/                   # n8n/MCP team (Steve)
├── data/                        # MongoDB/ChromaDB data
├── docs/                        # Documentation (you're reading this!)
├── env.example                  # Environment variables template
├── docker-compose.yml           # Docker setup
└── README.md                    # Project overview
```

---

## 📊 Step 1: Create Mock Data Files (12:30 AM - 1:00 AM)

### File: `app/mock-data/rides.ts`

```typescript
export interface Ride {
  ride_id: string;
  pickup_location: string;
  dropoff_location: string;
  distance: number;
  base_price: number;
  calculated_price: number;
  surge_multiplier: number;
  timestamp: string;
  status: 'completed' | 'in_progress' | 'pending';
}

export const mockRides: Ride[] = [
  {
    ride_id: "ride_001",
    pickup_location: "Downtown Phoenix",
    dropoff_location: "Sky Harbor Airport",
    distance: 5.2,
    base_price: 38.50,
    calculated_price: 46.20,
    surge_multiplier: 1.2,
    timestamp: "2025-12-01T14:30:00Z",
    status: "completed"
  },
  {
    ride_id: "ride_002",
    pickup_location: "Tempe ASU Campus",
    dropoff_location: "Scottsdale Fashion Square",
    distance: 8.7,
    base_price: 52.00,
    calculated_price: 52.00,
    surge_multiplier: 1.0,
    timestamp: "2025-12-01T15:45:00Z",
    status: "completed"
  },
  {
    ride_id: "ride_003",
    pickup_location: "Old Town Scottsdale",
    dropoff_location: "Phoenix Convention Center",
    distance: 12.3,
    base_price: 68.00,
    calculated_price: 102.00,
    surge_multiplier: 1.5,
    timestamp: "2025-12-01T19:20:00Z",
    status: "in_progress"
  },
  {
    ride_id: "ride_004",
    pickup_location: "Glendale Arena",
    dropoff_location: "Westgate Entertainment",
    distance: 2.1,
    base_price: 18.00,
    calculated_price: 16.20,
    surge_multiplier: 0.9,
    timestamp: "2025-12-01T22:15:00Z",
    status: "pending"
  },
  {
    ride_id: "ride_005",
    pickup_location: "Mesa Downtown",
    dropoff_location: "Chandler Mall",
    distance: 6.8,
    base_price: 42.00,
    calculated_price: 50.40,
    surge_multiplier: 1.2,
    timestamp: "2025-12-01T16:00:00Z",
    status: "completed"
  }
];
```

### File: `app/mock-data/pricing-decisions.ts`

```typescript
export interface AgentStep {
  step: number;
  tool: string;
  duration: string;
  result: string;
  details?: string;
}

export interface PricingDecision {
  ride_id: string;
  calculated_price: number;
  base_price: number;
  surge_multiplier: number;
  confidence: number;
  reasoning: string;
  factors_considered: string[];
  agent_steps: AgentStep[];
  total_time: string;
  driver_earnings: number;
  driver_percentage: number;
  timestamp: string;
}

export const mockPricingDecision: PricingDecision = {
  ride_id: "ride_001",
  calculated_price: 46.20,
  base_price: 38.50,
  surge_multiplier: 1.2,
  confidence: 0.94,
  reasoning: "High demand detected (2:1 ratio) combined with rain (70% chance) and nearby concert (15k attendees at Footprint Center). Applied 20% surge pricing to balance supply and demand. Driver earnings optimized at $33.26 (72% of fare) to ensure retention and service quality during challenging conditions.",
  factors_considered: [
    "Historical data: 234 similar rides in downtown area, average $38.50",
    "Weather: Rain 70% probability, temperature 68°F, wind 12 mph",
    "Events: Concert at Footprint Center (15k attendees), game at Chase Field (8k attendees)",
    "Demand ratio: 2.0 (high demand - 46 requests vs 23 available drivers)",
    "Driver availability: 23 drivers nearby within 0.5 mile radius",
    "Time of day: Evening rush hour (5:30 PM)",
    "Customer tier: Gold member (5% loyalty discount applied)",
    "Traffic conditions: Moderate congestion on I-10"
  ],
  agent_steps: [
    { 
      step: 1, 
      tool: "query_database", 
      duration: "120ms", 
      result: "Found 234 similar rides",
      details: "Queried MongoDB for historical rides in downtown Phoenix area with similar distance (5-6 miles)"
    },
    { 
      step: 2, 
      tool: "get_external_data", 
      duration: "450ms", 
      result: "Rain + Concert detected",
      details: "Retrieved weather data from OpenWeatherMap API and event data from Ticketmaster API"
    },
    { 
      step: 3, 
      tool: "calculate_demand_ratio", 
      duration: "95ms", 
      result: "Demand ratio: 2.0 (high)",
      details: "Calculated ratio of pending ride requests to available drivers in the area"
    },
    { 
      step: 4, 
      tool: "calculate_profitability", 
      duration: "80ms", 
      result: "28% margin achieved",
      details: "Calculated profitability considering operational costs, driver compensation, and platform fees"
    },
    { 
      step: 5, 
      tool: "optimize_driver_earnings", 
      duration: "65ms", 
      result: "$33.26 (72%)",
      details: "Optimized driver compensation to ensure retention while maintaining platform profitability"
    },
    { 
      step: 6, 
      tool: "retrieve_semantic_context", 
      duration: "340ms", 
      result: "5 similar cases, 91% success",
      details: "Retrieved semantically similar pricing scenarios from ChromaDB vector database"
    },
    { 
      step: 7, 
      tool: "validate_business_rules", 
      duration: "45ms", 
      result: "All rules passed",
      details: "Validated pricing against business rules (max surge 2.0x, min driver 70%, customer tier discounts)"
    }
  ],
  total_time: "1.19s",
  driver_earnings: 33.26,
  driver_percentage: 72,
  timestamp: "2025-12-01T14:30:00Z"
};

// Multiple scenarios for testing different UI states
export const mockPricingScenarios = {
  highSurge: {
    ...mockPricingDecision,
    calculated_price: 65.00,
    surge_multiplier: 1.5,
    confidence: 0.89,
    reasoning: "Very high demand (3:1 ratio) during severe weather and multiple major events. Applied 50% surge pricing."
  },
  normalPricing: {
    ...mockPricingDecision,
    calculated_price: 38.50,
    surge_multiplier: 1.0,
    confidence: 0.97,
    reasoning: "Normal conditions with balanced supply and demand. No surge pricing applied."
  },
  lowDemand: {
    ...mockPricingDecision,
    calculated_price: 32.00,
    surge_multiplier: 0.9,
    confidence: 0.92,
    reasoning: "Low demand period with excess driver supply. Applied 10% discount to stimulate demand while maintaining driver incentives."
  }
};
```

### File: `app/mock-data/analytics.ts`

```typescript
export interface AnalyticsData {
  totalRides: number;
  totalRevenue: number;
  averagePrice: number;
  averageSurge: number;
  driverRetention: number;
  customerSatisfaction: number;
  pricesByHour: { hour: string; price: number }[];
  surgeDistribution: { surge: string; count: number }[];
  topRoutes: { route: string; count: number; avgPrice: number }[];
}

export const mockAnalytics: AnalyticsData = {
  totalRides: 1247,
  totalRevenue: 54832.50,
  averagePrice: 43.95,
  averageSurge: 1.15,
  driverRetention: 94,
  customerSatisfaction: 4.6,
  pricesByHour: [
    { hour: "00:00", price: 32.50 },
    { hour: "03:00", price: 28.00 },
    { hour: "06:00", price: 38.50 },
    { hour: "09:00", price: 45.20 },
    { hour: "12:00", price: 42.00 },
    { hour: "15:00", price: 48.50 },
    { hour: "18:00", price: 56.80 },
    { hour: "21:00", price: 62.30 },
  ],
  surgeDistribution: [
    { surge: "0.8-0.9x", count: 145 },
    { surge: "1.0x", count: 687 },
    { surge: "1.1-1.2x", count: 312 },
    { surge: "1.3-1.5x", count: 89 },
    { surge: "1.5x+", count: 14 },
  ],
  topRoutes: [
    { route: "Downtown → Airport", count: 234, avgPrice: 42.50 },
    { route: "ASU → Scottsdale", count: 189, avgPrice: 48.20 },
    { route: "Airport → Downtown", count: 178, avgPrice: 41.80 },
    { route: "Tempe → Phoenix", count: 156, avgPrice: 38.90 },
    { route: "Scottsdale → Mesa", count: 134, avgPrice: 52.30 },
  ]
};
```

---

## 🔌 Step 2: Create API Service with Mock Toggle (1:00 AM - 1:30 AM)

### File: `app/services/api.ts`

```typescript
import { mockRides } from '@/app/mock-data/rides';
import { mockPricingDecision, mockPricingScenarios } from '@/app/mock-data/pricing-decisions';
import { mockAnalytics } from '@/app/mock-data/analytics';

// Toggle this when backend is ready
const USE_MOCK_DATA = true;
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Simulate API delay for realism
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export async function calculatePrice(rideData: any) {
  if (USE_MOCK_DATA) {
    await delay(1200); // Simulate agent thinking time
    return mockPricingDecision;
  } else {
    const response = await fetch(`${API_BASE_URL}/api/calculate-price`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(rideData)
    });
    return response.json();
  }
}

export async function getRides() {
  if (USE_MOCK_DATA) {
    await delay(500);
    return mockRides;
  } else {
    const response = await fetch(`${API_BASE_URL}/api/rides`);
    return response.json();
  }
}

export async function getAnalytics() {
  if (USE_MOCK_DATA) {
    await delay(800);
    return mockAnalytics;
  } else {
    const response = await fetch(`${API_BASE_URL}/api/analytics`);
    return response.json();
  }
}

export async function getPricingDecision(rideId: string) {
  if (USE_MOCK_DATA) {
    await delay(400);
    return mockPricingDecision;
  } else {
    const response = await fetch(`${API_BASE_URL}/api/pricing-decision/${rideId}`);
    return response.json();
  }
}
```

---

## 🎨 Step 3: Build UI Components (1:30 AM - 4:00 AM or Monday morning)

### File: `app/components/PricingDashboard.tsx`

```typescript
'use client';

import { useState } from 'react';
import { calculatePrice } from '@/app/services/api';
import { Calculator, TrendingUp, DollarSign } from 'lucide-react';

export default function PricingDashboard() {
  const [pricing, setPricing] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    pickup: 'Downtown Phoenix',
    dropoff: 'Sky Harbor Airport',
    distance: 5.2
  });

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const result = await calculatePrice(formData);
      setPricing(result);
    } catch (error) {
      console.error('Error calculating price:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-teal-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            HoneyGo Dynamic Pricing
          </h1>
          <p className="text-gray-600">
            AI-powered intelligent pricing for optimal profitability and driver retention
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
            <Calculator className="w-6 h-6 text-blue-600" />
            Calculate Ride Price
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Pickup Location
              </label>
              <input
                type="text"
                value={formData.pickup}
                onChange={(e) => setFormData({...formData, pickup: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dropoff Location
              </label>
              <input
                type="text"
                value={formData.dropoff}
                onChange={(e) => setFormData({...formData, dropoff: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Distance (miles)
              </label>
              <input
                type="number"
                value={formData.distance}
                onChange={(e) => setFormData({...formData, distance: parseFloat(e.target.value)})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <button
            onClick={handleCalculate}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                Calculating...
              </>
            ) : (
              <>
                <TrendingUp className="w-5 h-5" />
                Calculate Dynamic Price
              </>
            )}
          </button>
        </div>

        {/* Results */}
        {pricing && (
          <div className="bg-white rounded-xl shadow-lg p-6">
            {/* Price Display */}
            <div className="border-b pb-6 mb-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Calculated Price</p>
                  <h2 className="text-5xl font-bold text-green-600">
                    ${pricing.calculated_price.toFixed(2)}
                  </h2>
                </div>
                <div className="text-right">
                  <p className="text-sm text-gray-600 mb-1">Base Price</p>
                  <p className="text-2xl font-semibold text-gray-700">
                    ${pricing.base_price.toFixed(2)}
                  </p>
                  <p className="text-sm text-blue-600 font-medium mt-1">
                    Surge: {pricing.surge_multiplier}x
                  </p>
                </div>
              </div>
              
              <div className="mt-4 flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-600">
                    Confidence: {(pricing.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <DollarSign className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-gray-600">
                    Driver Earnings: ${pricing.driver_earnings.toFixed(2)} ({pricing.driver_percentage}%)
                  </span>
                </div>
              </div>
            </div>

            {/* Agent Reasoning */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-gray-900">
                AI Agent Reasoning
              </h3>
              <p className="text-gray-700 leading-relaxed bg-blue-50 p-4 rounded-lg">
                {pricing.reasoning}
              </p>
            </div>

            {/* Factors Considered */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-3 text-gray-900">
                Factors Considered
              </h3>
              <ul className="space-y-2">
                {pricing.factors_considered.map((factor: string, idx: number) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-blue-600 mt-1">•</span>
                    <span className="text-gray-700 text-sm">{factor}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Agent Steps */}
            <div>
              <h3 className="text-lg font-semibold mb-3 text-gray-900">
                Agent Execution Steps
              </h3>
              <div className="space-y-3">
                {pricing.agent_steps.map((step: any) => (
                  <div key={step.step} className="bg-gray-50 p-4 rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-gray-900">
                        Step {step.step}: {step.tool}
                      </span>
                      <span className="text-sm text-gray-500">{step.duration}</span>
                    </div>
                    <p className="text-sm text-gray-700">{step.result}</p>
                    {step.details && (
                      <p className="text-xs text-gray-500 mt-1">{step.details}</p>
                    )}
                  </div>
                ))}
              </div>
              <div className="mt-4 text-right">
                <span className="text-sm text-gray-600">
                  Total execution time: <span className="font-semibold">{pricing.total_time}</span>
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

---

## 🔄 Step 4: Integration with Backend (Dec 2-3)

When backend is ready, simply change one line:

```typescript
// In app/services/api.ts
const USE_MOCK_DATA = false; // Change from true to false
```

That's it! Your entire UI will now use real backend data.

---

## 💡 Pro Tips

### 1. Test Different Scenarios
Use the `mockPricingScenarios` to test how UI looks with different data:

```typescript
// In your component
const result = mockPricingScenarios.highSurge; // Test high surge UI
const result = mockPricingScenarios.normalPricing; // Test normal UI
const result = mockPricingScenarios.lowDemand; // Test low demand UI
```

### 2. Add Loading States
Always show loading spinners - makes the app feel professional:

```typescript
{loading && (
  <div className="flex items-center justify-center">
    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
  </div>
)}
```

### 3. Error Handling
Add error states for when things go wrong:

```typescript
const [error, setError] = useState<string | null>(null);

try {
  const result = await calculatePrice(formData);
  setPricing(result);
  setError(null);
} catch (err) {
  setError('Failed to calculate price. Please try again.');
}
```

### 4. Environment Variables
Create `.env.local` file:

```bash
NEXT_PUBLIC_USE_MOCK_DATA=true
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then use in code:

```typescript
const USE_MOCK_DATA = process.env.NEXT_PUBLIC_USE_MOCK_DATA === 'true';
```

---

## 📅 Timeline

**⚠️ NOTE**: All times are **suggestions only**. Team members are distributed across the country with different schedules. Work when you're available - the important thing is completing tasks by the phase deadlines, not the exact times listed.

### ✅ Monday Dec 1 (TODAY - IN PROGRESS)
- **12:01 AM - 12:30 AM**: ✅ Create Next.js project, install dependencies
- **12:30 AM - 1:00 AM**: Create mock data files
- **1:00 AM - 4:00 AM**: Build first components (or sleep and start in morning!)
- **9:00 AM - 12:00 PM**: Continue building components
- **12:00 PM - 2:00 PM**: Show team working UI with mock data
- **2:00 PM - 6:00 PM**: Polish UI, add more components
- **Evening**: Coordinate with backend team (Dari) for API contracts

### Tuesday Dec 2
- **Morning**: Backend team completes APIs
- **Afternoon**: Integration - change `USE_MOCK_DATA = false`
- **Evening**: Test integrated system, Docker setup begins

### Wednesday Dec 3
- **Morning**: Bug fixes, polish, optimization
- **Afternoon**: Add voice features (E1 & E2) if time permits
- **Evening**: Final integration testing

### Thursday Dec 4 (Midday Deadline)
- **Morning**: Final testing, screenshots for slides, demo preparation
- **Midday**: Submit to GitHub, presentation deck, demo video
- **Afternoon**: Rehearse presentation

### Friday Dec 5 (Presentation Day)
- **Live Demo**: Show off HoneyGo to judges! 🎉

---

## ✅ Benefits Recap

| Benefit | Impact |
|---------|--------|
| **Parallel Development** | Team works simultaneously, faster completion |
| **Early Feedback** | Team sees UI immediately, can suggest changes |
| **No Backend Dependency** | You're not blocked waiting for APIs |
| **Easy Integration** | Just flip `USE_MOCK_DATA` flag when ready |
| **Professional Demo** | Even if backend has issues, UI still looks great |
| **Reduced Risk** | If backend is delayed, you still have something to show |

---

## 🎯 Success Criteria

By end of Monday Dec 1, you should have:
- ✅ Working Next.js app running on localhost
- ✅ Beautiful UI with HoneyGo branding
- ✅ Pricing dashboard showing mock results
- ✅ Agent reasoning visualization
- ✅ Smooth animations and loading states
- ✅ Team can see and interact with the UI

---

## 🎤 Extra Features: Voice Input & Output (E1 & E2)

**When to implement**: Dec 3 afternoon/evening (ONLY if core features are stable)

### Voice Output (E2) - Priority 1 🔊
**Easiest and highest impact - do this first!**

```typescript
// app/components/VoiceOutput.tsx
'use client';

import { useState } from 'react';
import { Volume2, VolumeX } from 'lucide-react';

export function VoiceOutput({ text }: { text: string }) {
  const [speaking, setSpeaking] = useState(false);

  const speak = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9; // Slightly slower for clarity
      utterance.pitch = 1.0;
      utterance.onstart = () => setSpeaking(true);
      utterance.onend = () => setSpeaking(false);
      window.speechSynthesis.speak(utterance);
    }
  };

  const stop = () => {
    window.speechSynthesis.cancel();
    setSpeaking(false);
  };

  return (
    <button
      onClick={speaking ? stop : speak}
      className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
    >
      {speaking ? (
        <>
          <VolumeX className="w-5 h-5" />
          Stop Speaking
        </>
      ) : (
        <>
          <Volume2 className="w-5 h-5" />
          Read Aloud
        </>
      )}
    </button>
  );
}
```

**Usage**: Add to pricing results to read AI reasoning aloud!

### Voice Input (E1) - Priority 2 🎤
**More complex, but very impressive**

```typescript
// app/components/VoiceInput.tsx
'use client';

import { useState, useEffect } from 'react';
import { Mic, MicOff } from 'lucide-react';

export function VoiceInput({ onTranscript }: { onTranscript: (text: string) => void }) {
  const [listening, setListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = false;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        onTranscript(transcript);
        setListening(false);
      };

      recognitionInstance.onerror = () => {
        setListening(false);
      };

      recognitionInstance.onend = () => {
        setListening(false);
      };

      setRecognition(recognitionInstance);
    }
  }, [onTranscript]);

  const toggleListening = () => {
    if (!recognition) return;

    if (listening) {
      recognition.stop();
      setListening(false);
    } else {
      recognition.start();
      setListening(true);
    }
  };

  if (!recognition) {
    return null; // Browser doesn't support speech recognition
  }

  return (
    <button
      onClick={toggleListening}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
        listening 
          ? 'bg-red-600 hover:bg-red-700 text-white animate-pulse' 
          : 'bg-gray-600 hover:bg-gray-700 text-white'
      }`}
    >
      {listening ? (
        <>
          <MicOff className="w-5 h-5" />
          Listening...
        </>
      ) : (
        <>
          <Mic className="w-5 h-5" />
          Speak
        </>
      )}
    </button>
  );
}
```

**Usage**: Add to input form to allow speaking pickup/dropoff locations!

### Testing Voice Features
```typescript
// Test in browser console
window.speechSynthesis.speak(new SpeechSynthesisUtterance("Hello HoneyGo!"));
```

**Browser Compatibility**: Works in Chrome, Edge, Safari (not Firefox)

---

## 🐳 Docker Integration

When Docker setup is complete (Dec 2-3), frontend will run in a container:

```bash
# Run frontend in Docker
docker-compose up frontend

# Frontend will be available at http://localhost:3000
```

See `docker-compose.yml` and `Dockerfile.frontend` for configuration.

---

## 🚨 Current Status (Dec 1, 2025)

**Implementation Started**: ✅ YES - We're live!

**Team Status**:
- **Jason** (Primary Frontend): Tied up with work till about 3:30 PM AZ time. In the meantime, Safa will work on the Frontend.
- **Safa** (Backup Frontend): Building initial implementation NOW on branch `frontend/initial-implementation-safa`
- **Strategy**: 
  - Safa builds working version first
  - When Jason is available, he can either:
    - **Option A** (Most likely): Continue building on Safa's version (collaborate on same branch)
    - **Option B**: Create his own branch `frontend/initial-implementation-jason` and build independently
  - Team reviews and chooses best approach (or hybrid)

**Branch Strategy**:
- Current branch: `frontend/initial-implementation-safa`
- Jason's branch (if needed): `frontend/initial-implementation-jason` (create from `dev`)
- Final merged: `frontend/integrated` (cherry-pick best from both)

**Note to Jason**: When you're ready, check out Safa's branch first! If you like it, just continue building on it. If you want to try your own approach, create a new branch from `dev`. Either way is fine! 👍

**Next Steps**:
1. Initialize Next.js project in `frontend/` folder
2. Create mock data files
3. Build core components (PricingDashboard, ReasoningExplainer)
4. Show team progress by end of day
5. Coordinate with Dari (Backend) for API contracts

---

**Good luck and let's build an amazing frontend! 🚀**

