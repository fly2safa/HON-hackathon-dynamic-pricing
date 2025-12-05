"""
Knowledge Base Seeding

Seeds ChromaDB with Honeywell domain knowledge and pricing reasoning examples.
"""

from typing import List, Dict, Any
import logging
from .chromadb_client import ChromaDBClient

logger = logging.getLogger(__name__)


def seed_hon_knowledge(client: ChromaDBClient, clear_existing: bool = False) -> int:
    """
    Seed Honeywell domain knowledge into ChromaDB
    
    Args:
        client: ChromaDB client instance
        clear_existing: Whether to clear existing knowledge first
        
    Returns:
        Number of items added
    """
    if clear_existing:
        logger.info("Clearing existing HON knowledge...")
        client.clear_collection("hon_knowledge")
    
    # Honeywell domain knowledge (public information + ride-sharing best practices)
    hon_knowledge = [
        {
            "text": "Honeywell's approach to pricing emphasizes value-based strategies that consider customer relationships, market conditions, and long-term partnerships. Fair pricing during high-demand periods maintains customer trust and reduces churn.",
            "metadata": {
                "category": "pricing_philosophy",
                "source": "Honeywell best practices",
                "relevance": "high"
            }
        },
        {
            "text": "Dynamic pricing should balance profitability with partner retention. During surge periods, ensure driver compensation remains attractive (typically 70-80% of fare) to maintain supply and service quality.",
            "metadata": {
                "category": "partner_retention",
                "source": "Ride-sharing industry standards",
                "relevance": "high"
            }
        },
        {
            "text": "Weather conditions significantly impact ride demand and pricing. Rain increases demand by 20-30%, snow by 40-50%, and severe weather by 60%+. Adjust pricing accordingly while maintaining transparency with customers.",
            "metadata": {
                "category": "weather_impact",
                "source": "Market analysis",
                "relevance": "high"
            }
        },
        {
            "text": "Customer loyalty tiers should provide meaningful benefits. Bronze (0-10 rides): standard pricing. Silver (11-50): 5% discount. Gold (51-100): 10% discount. Platinum (100+): 15% discount plus priority matching.",
            "metadata": {
                "category": "loyalty_program",
                "source": "Customer retention strategy",
                "relevance": "high"
            }
        },
        {
            "text": "Geographic pricing factors: Urban areas have higher base rates due to traffic and demand density. Suburban areas: -10% adjustment. Rural areas: -20% but with minimum fare guarantees to ensure driver participation.",
            "metadata": {
                "category": "geographic_pricing",
                "source": "Market segmentation",
                "relevance": "high"
            }
        },
        {
            "text": "Time-of-day surge pricing: Morning rush (6-9 AM): 1.2-1.5x. Evening rush (4-7 PM): 1.3-1.6x. Late night (11 PM-3 AM): 1.4-1.8x. Weekend nights: 1.5-2.0x. Always communicate surge clearly to customers.",
            "metadata": {
                "category": "time_based_pricing",
                "source": "Demand patterns",
                "relevance": "high"
            }
        },
        {
            "text": "Event-based pricing: Concerts/sports events increase demand within 2-mile radius by 50-100%. Airports have consistent demand but price sensitivity. Convention centers show predictable patterns based on event schedules.",
            "metadata": {
                "category": "event_impact",
                "source": "Historical data analysis",
                "relevance": "medium"
            }
        },
        {
            "text": "Competitor pricing intelligence: Monitor Uber, Lyft, and local competitors. Price within 5-10% of market leaders to remain competitive. Highlight unique value propositions (AI transparency, loyalty benefits) when pricing higher.",
            "metadata": {
                "category": "competitive_analysis",
                "source": "Market positioning",
                "relevance": "high"
            }
        },
        {
            "text": "Regulatory compliance: Phoenix requires transparent surge pricing disclosure. New York has taxi medallion regulations affecting ride-share pricing. San Francisco has strict driver compensation rules (minimum 80% of fare).",
            "metadata": {
                "category": "regulations",
                "source": "Legal compliance",
                "relevance": "high"
            }
        },
        {
            "text": "Customer communication: Always explain pricing factors. Show base rate, distance, time, surge multiplier, and discounts separately. Transparency builds trust and reduces complaints by 40%.",
            "metadata": {
                "category": "customer_communication",
                "source": "UX best practices",
                "relevance": "high"
            }
        },
        {
            "text": "Minimum fare policies: Set minimum fares to ensure driver profitability on short trips. Urban: $8-10. Suburban: $10-12. Rural: $12-15. Adjust based on local cost of living and fuel prices.",
            "metadata": {
                "category": "minimum_pricing",
                "source": "Driver economics",
                "relevance": "medium"
            }
        },
        {
            "text": "Maximum surge caps: Implement surge caps to prevent price gouging during emergencies. Standard cap: 3x base rate. Emergency situations (natural disasters): 1.5x cap with clear communication.",
            "metadata": {
                "category": "surge_limits",
                "source": "Ethical pricing",
                "relevance": "high"
            }
        },
        {
            "text": "Distance-based pricing: $2.50-3.00 per mile in urban areas. $2.00-2.50 in suburban. $1.75-2.25 in rural. Include time component: $0.30-0.50 per minute for traffic delays.",
            "metadata": {
                "category": "distance_pricing",
                "source": "Cost structure",
                "relevance": "high"
            }
        },
        {
            "text": "Passenger count adjustments: 1-2 passengers: standard rate. 3-4 passengers: +10% (larger vehicle needed). 5+ passengers: +20% (premium vehicle required). Ensure vehicle availability matches demand.",
            "metadata": {
                "category": "passenger_pricing",
                "source": "Vehicle economics",
                "relevance": "medium"
            }
        },
        {
            "text": "Scheduled rides: Allow 10% price lock for rides scheduled 2+ hours in advance. Include disclaimer that actual price may vary if conditions change significantly (weather, traffic, events).",
            "metadata": {
                "category": "scheduled_pricing",
                "source": "Booking policies",
                "relevance": "medium"
            }
        },
        {
            "text": "Cancellation policies: Free cancellation within 5 minutes. After 5 minutes: $5 fee. No-show: $10 fee. Waive fees for legitimate emergencies to maintain customer goodwill.",
            "metadata": {
                "category": "cancellation_policy",
                "source": "Operations",
                "relevance": "low"
            }
        },
        {
            "text": "Driver incentives during surge: Offer driver bonuses during high-demand periods to increase supply. Example: +$5 per ride during 2x+ surge. This improves service availability and customer satisfaction.",
            "metadata": {
                "category": "driver_incentives",
                "source": "Supply management",
                "relevance": "medium"
            }
        },
        {
            "text": "Airport pricing: Airports have unique dynamics - consistent demand but price-sensitive business travelers. Consider flat-rate options for common airport routes. Factor in airport fees (typically $2-5 per pickup).",
            "metadata": {
                "category": "airport_pricing",
                "source": "Special locations",
                "relevance": "medium"
            }
        },
        {
            "text": "Corporate accounts: Offer volume discounts for corporate clients. 10-50 rides/month: 5% discount. 51-200: 10% discount. 200+: 15% discount plus dedicated support. Ensure pricing remains profitable.",
            "metadata": {
                "category": "corporate_pricing",
                "source": "B2B strategy",
                "relevance": "low"
            }
        },
        {
            "text": "AI pricing confidence: When AI confidence score is below 85%, flag for human review. Confidence factors: data quality, scenario similarity to training data, external factor reliability, regulatory compliance.",
            "metadata": {
                "category": "ai_confidence",
                "source": "AI governance",
                "relevance": "high"
            }
        },
        {
            "text": "Seasonal adjustments: Summer (June-Aug): +5% in tourist cities. Winter (Dec-Feb): +10% in cold climates due to increased demand and driver costs. Holiday periods (Thanksgiving, Christmas, New Year): +15-20%.",
            "metadata": {
                "category": "seasonal_pricing",
                "source": "Demand forecasting",
                "relevance": "medium"
            }
        },
        {
            "text": "Traffic impact: Heavy traffic increases time component significantly. Use real-time traffic APIs to adjust pricing. Communicate estimated time clearly. Consider offering fixed-price options during known congestion periods.",
            "metadata": {
                "category": "traffic_pricing",
                "source": "Real-time optimization",
                "relevance": "high"
            }
        },
        {
            "text": "Customer complaint resolution: If pricing dispute arises, review AI reasoning trace. If error found, issue partial refund (20-50% depending on severity). Use disputes as training data to improve AI accuracy.",
            "metadata": {
                "category": "dispute_resolution",
                "source": "Customer service",
                "relevance": "medium"
            }
        },
        {
            "text": "Data privacy: Never use personally identifiable information in pricing decisions. Use aggregated patterns only. Comply with GDPR, CCPA, and local privacy regulations. Maintain transparent data usage policies.",
            "metadata": {
                "category": "data_privacy",
                "source": "Legal compliance",
                "relevance": "high"
            }
        },
        {
            "text": "Pricing experimentation: A/B test pricing strategies on small user segments (5-10%) before full rollout. Monitor key metrics: conversion rate, customer satisfaction, driver acceptance, profitability. Iterate based on data.",
            "metadata": {
                "category": "experimentation",
                "source": "Product development",
                "relevance": "low"
            }
        }
    ]
    
    # Add knowledge to ChromaDB
    ids = client.add_bulk_knowledge(hon_knowledge, collection_name="hon_knowledge")
    logger.info(f"Seeded {len(ids)} HON knowledge items")
    
    return len(ids)


def seed_pricing_reasoning(client: ChromaDBClient, clear_existing: bool = False) -> int:
    """
    Seed example pricing reasoning into ChromaDB
    
    Args:
        client: ChromaDB client instance
        clear_existing: Whether to clear existing reasoning first
        
    Returns:
        Number of items added
    """
    if clear_existing:
        logger.info("Clearing existing pricing reasoning...")
        client.clear_collection("pricing_reasoning")
    
    # Example pricing decisions with reasoning
    pricing_examples = [
        {
            "text": "Urban ride, 8.5 miles, evening rush hour, rainy weather, Gold customer. Base: $21.25 (8.5 × $2.50). Evening surge: 1.4x. Rain impact: 1.2x. Combined multiplier: 1.68x. Subtotal: $35.70. Gold discount: 10%. Final: $32.13. Reasoning: High demand period with adverse weather justifies surge. Gold loyalty discount rewards repeat customer. Price competitive with market (Uber: $34.50, Lyft: $33.20).",
            "metadata": {
                "scenario": "urban_evening_rain",
                "distance_miles": 8.5,
                "time_of_day": "evening_rush",
                "weather": "rain",
                "customer_tier": "gold",
                "final_price": 32.13,
                "outcome": "successful"
            }
        },
        {
            "text": "Suburban ride, 12 miles, morning, clear weather, Bronze customer. Base: $30.00 (12 × $2.50). Suburban adjustment: 0.9x. Morning surge: 1.2x. Combined: 1.08x. Final: $32.40. Reasoning: Moderate morning demand in suburban area. No weather impact. Standard pricing for Bronze customer. Competitive with alternatives (Uber: $33.00).",
            "metadata": {
                "scenario": "suburban_morning_clear",
                "distance_miles": 12,
                "time_of_day": "morning_rush",
                "weather": "clear",
                "customer_tier": "bronze",
                "final_price": 32.40,
                "outcome": "successful"
            }
        },
        {
            "text": "Urban ride, 5 miles, late night, clear weather, Platinum customer, near concert venue. Base: $12.50 (5 × $2.50). Late night: 1.6x. Event proximity: 1.3x. Combined: 2.08x. Subtotal: $26.00. Platinum discount: 15%. Final: $22.10. Reasoning: High demand from concert ending. Late night premium justified. Platinum customer receives significant discount. Still profitable and competitive.",
            "metadata": {
                "scenario": "urban_latenight_event",
                "distance_miles": 5,
                "time_of_day": "late_night",
                "weather": "clear",
                "customer_tier": "platinum",
                "event_nearby": True,
                "final_price": 22.10,
                "outcome": "successful"
            }
        },
        {
            "text": "Urban ride, 15 miles, midday, snowing, Silver customer. Base: $37.50 (15 × $2.50). Snow impact: 1.5x. Midday (low demand): 1.0x. Combined: 1.5x. Subtotal: $56.25. Silver discount: 5%. Final: $53.44. Reasoning: Severe weather significantly increases demand and driver costs. No time surge during midday. Silver discount applied. Price higher than normal but justified by conditions.",
            "metadata": {
                "scenario": "urban_midday_snow",
                "distance_miles": 15,
                "time_of_day": "midday",
                "weather": "snow",
                "customer_tier": "silver",
                "final_price": 53.44,
                "outcome": "successful"
            }
        },
        {
            "text": "Airport ride, 18 miles, early morning, clear weather, Gold customer. Base: $45.00 (18 × $2.50). Airport fee: $3.50. Early morning: 1.1x. Subtotal: $53.00. Gold discount: 10%. Final: $47.70. Reasoning: Airport pickups have additional fees. Early morning has moderate demand. Gold customer loyalty rewarded. Competitive with airport taxi rates ($50-55).",
            "metadata": {
                "scenario": "airport_early_clear",
                "distance_miles": 18,
                "time_of_day": "early_morning",
                "weather": "clear",
                "customer_tier": "gold",
                "location_type": "airport",
                "final_price": 47.70,
                "outcome": "successful"
            }
        },
        {
            "text": "Short urban ride, 2 miles, evening rush, clear weather, Bronze customer. Distance price: $5.00 (2 × $2.50). Below minimum fare. Applied minimum: $10.00. Evening surge: 1.3x. Final: $13.00. Reasoning: Short trips require minimum fare to ensure driver profitability. Evening surge applied to minimum fare. Transparent communication about minimum fare policy prevents disputes.",
            "metadata": {
                "scenario": "short_urban_evening",
                "distance_miles": 2,
                "time_of_day": "evening_rush",
                "weather": "clear",
                "customer_tier": "bronze",
                "minimum_fare_applied": True,
                "final_price": 13.00,
                "outcome": "successful"
            }
        },
        {
            "text": "Scheduled ride, 10 miles, future booking (4 hours ahead), predicted clear weather, Silver customer. Base: $25.00 (10 × $2.50). Scheduled ride lock: 0.9x (10% discount for advance booking). Silver discount: 5%. Final: $21.38. Reasoning: Advance booking allows better driver matching and route optimization. Price locked with disclaimer about condition changes. Customer benefits from planning ahead.",
            "metadata": {
                "scenario": "scheduled_advance",
                "distance_miles": 10,
                "booking_type": "scheduled",
                "weather": "predicted_clear",
                "customer_tier": "silver",
                "final_price": 21.38,
                "outcome": "successful"
            }
        },
        {
            "text": "Multi-passenger ride, 8 miles, afternoon, clear weather, 5 passengers, Bronze customer. Base: $20.00 (8 × $2.50). Large group surcharge: 1.2x (premium vehicle needed). Afternoon: 1.0x. Final: $24.00. Reasoning: 5 passengers require larger vehicle (SUV/minivan). Additional cost justified by vehicle type. No time surge during afternoon. Competitive with alternatives for group rides.",
            "metadata": {
                "scenario": "multi_passenger",
                "distance_miles": 8,
                "time_of_day": "afternoon",
                "weather": "clear",
                "passenger_count": 5,
                "customer_tier": "bronze",
                "final_price": 24.00,
                "outcome": "successful"
            }
        },
        {
            "text": "Rural ride, 20 miles, evening, clear weather, Bronze customer. Base: $50.00 (20 × $2.50). Rural adjustment: 0.8x. Evening: 1.2x. Combined: 0.96x. Calculated: $48.00. Below rural minimum ($50). Applied minimum: $50.00. Reasoning: Rural rides have higher minimums due to driver return costs. Lower base rate offset by minimum fare. Ensures driver participation in rural areas.",
            "metadata": {
                "scenario": "rural_evening",
                "distance_miles": 20,
                "time_of_day": "evening",
                "weather": "clear",
                "location_type": "rural",
                "customer_tier": "bronze",
                "minimum_fare_applied": True,
                "final_price": 50.00,
                "outcome": "successful"
            }
        },
        {
            "text": "Urban ride, 6 miles, weekend night, clear weather, near entertainment district, Bronze customer. Base: $15.00 (6 × $2.50). Weekend night: 1.8x. Entertainment district: 1.2x. Combined: 2.16x. Final: $32.40. Reasoning: High demand on weekend nights in entertainment areas. Multiple surge factors compound. Price high but expected for this scenario. Customers in entertainment districts are less price-sensitive.",
            "metadata": {
                "scenario": "weekend_entertainment",
                "distance_miles": 6,
                "time_of_day": "weekend_night",
                "weather": "clear",
                "location_type": "entertainment_district",
                "customer_tier": "bronze",
                "final_price": 32.40,
                "outcome": "successful"
            }
        }
    ]
    
    # Add pricing reasoning to ChromaDB
    ids = client.add_bulk_knowledge(pricing_examples, collection_name="pricing_reasoning")
    logger.info(f"Seeded {len(ids)} pricing reasoning examples")
    
    return len(ids)


def seed_all(client: ChromaDBClient, clear_existing: bool = False) -> Dict[str, int]:
    """
    Seed all knowledge bases
    
    Args:
        client: ChromaDB client instance
        clear_existing: Whether to clear existing data first
        
    Returns:
        Dict with counts for each collection
    """
    logger.info("Starting knowledge base seeding...")
    
    results = {
        "hon_knowledge": seed_hon_knowledge(client, clear_existing),
        "pricing_reasoning": seed_pricing_reasoning(client, clear_existing)
    }
    
    logger.info(f"Seeding complete: {results}")
    return results

