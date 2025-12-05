/**
 * Custom React Hook for fetching real-time weather data
 */

import { useState, useEffect } from 'react';
import { fetchWeather, generateMockWeather, CityName, CITY_COORDINATES } from '@/lib/weatherService';

export interface WeatherData {
  temperature: number;
  feelsLike: number;
  condition: string;
  description: string;
  humidity: number;
  windSpeed: number;
  weatherType: 'clear' | 'rain' | 'storm' | 'snow' | 'fog' | 'clouds';
  weatherSeverity: 'none' | 'light' | 'moderate' | 'severe';
  icon: string;
  timestamp: number;
  location?: string;
  isRealData: boolean; // Indicates if this is real API data or mock data
}

export function useRealWeather(city: string) {
  const [weather, setWeather] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadWeather = async () => {
      setLoading(true);
      setError(null);

      try {
        // Validate city name
        if (!(city in CITY_COORDINATES)) {
          throw new Error(`Invalid city: ${city}`);
        }

        const cityName = city as CityName;
        const realWeather = await fetchWeather(cityName);

        if (realWeather) {
          // Real API data
          setWeather({
            ...realWeather,
            location: CITY_COORDINATES[cityName].location,
            isRealData: true
          });
        } else {
          // Fallback to mock data
          const mockWeather = generateMockWeather(cityName);
          setWeather({
            ...mockWeather,
            location: CITY_COORDINATES[cityName].location,
            isRealData: false
          });
        }
      } catch (err) {
        console.error('Error loading weather:', err);
        setError(err instanceof Error ? err.message : 'Failed to load weather');
        
        // Use mock data as final fallback
        if (city in CITY_COORDINATES) {
          const mockWeather = generateMockWeather(city as CityName);
          setWeather({
            ...mockWeather,
            location: CITY_COORDINATES[city as CityName].location,
            isRealData: false
          });
        }
      } finally {
        setLoading(false);
      }
    };

    loadWeather();
  }, [city]);

  return { weather, loading, error };
}

