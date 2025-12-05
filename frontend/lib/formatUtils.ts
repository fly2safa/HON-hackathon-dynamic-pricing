/**
 * Formatting Utilities
 * 
 * Helper functions for formatting data for display.
 */

/**
 * Convert miles to kilometers
 */
export function milesToKm(miles: number): number {
  return miles * 1.60934;
}

/**
 * Format distance with both miles and kilometers for international users
 * 
 * @param miles - Distance in miles
 * @returns Formatted string like "8.5 mi (13.7 km)"
 */
export function formatDistance(miles: number): string {
  const km = milesToKm(miles);
  return `${miles.toFixed(1)} mi (${km.toFixed(1)} km)`;
}

/**
 * Format distance - short version (for tight spaces)
 * 
 * @param miles - Distance in miles
 * @returns Formatted string like "8.5mi/13.7km"
 */
export function formatDistanceShort(miles: number): string {
  const km = milesToKm(miles);
  return `${miles.toFixed(1)}mi / ${km.toFixed(1)}km`;
}

/**
 * Format price as currency
 * 
 * @param amount - Price amount
 * @returns Formatted string like "$27.75"
 */
export function formatPrice(amount: number): string {
  return `$${amount.toFixed(2)}`;
}

/**
 * Format percentage
 * 
 * @param value - Percentage value (e.g., 15.5)
 * @returns Formatted string like "15.5%"
 */
export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`;
}

