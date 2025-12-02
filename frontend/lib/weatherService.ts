/**
 * Real-time Weather Service using OpenWeatherMap API
 * 
 * Free tier: 1,000 calls/day, 60 calls/minute
 * Provides current weather data for specific locations
 */

// City coordinates for precise weather data
export const CITY_COORDINATES = {
  'Phoenix': {
    name: 'Phoenix',
    location: 'Phoenix Sky Harbor Airport',
    lat: 33.4343,
    lon: -112.0080,
    emoji: '🌵'
  },
  'New York': {
    name: 'New York',
    location: 'JFK Airport',
    lat: 40.6413,
    lon: -73.7781,
    emoji: '🗽'
  },
  'San Francisco': {
    name: 'San Francisco',
    location: 'San Francisco City Hall',
    lat: 37.7793,
    lon: -122.4193,
    emoji: '🌉'
  },
  'Chicago': {
    name: 'Chicago',
    location: 'Willis Tower',
    lat: 41.8789,
    lon: -87.6359,
    emoji: '🏙️'
  },
  'Orlando': {
    name: 'Orlando',
    location: 'Orlando International Airport',
    lat: 28.4312,
    lon: -81.3081,
    emoji: '🏰'
  }
} as const;

export type CityName = keyof typeof CITY_COORDINATES;

interface WeatherData {
  temperature: number; // Fahrenheit
  feelsLike: number;
  condition: string;
  description: string;
  humidity: number;
  windSpeed: number;
  weatherType: 'clear' | 'rain' | 'storm' | 'snow' | 'fog' | 'clouds';
  weatherSeverity: 'none' | 'light' | 'moderate' | 'severe';
  icon: string;
  timestamp: number;
}

// Cache weather data to avoid excessive API calls (30 minute cache)
const weatherCache: Map<string, { data: WeatherData; expiry: number }> = new Map();
const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes

/**
 * Determine weather type and severity from OpenWeatherMap data
 */
function determineWeatherType(weatherMain: string, weatherId: number, description: string): {
  type: WeatherData['weatherType'];
  severity: WeatherData['weatherSeverity'];
} {
  // Weather ID ranges:
  // 2xx = Thunderstorm
  // 3xx = Drizzle
  // 5xx = Rain
  // 6xx = Snow
  // 7xx = Atmosphere (fog, mist, etc.)
  // 800 = Clear
  // 80x = Clouds

  if (weatherId >= 200 && weatherId < 300) {
    return { type: 'storm', severity: 'severe' };
  } else if (weatherId >= 300 && weatherId < 400) {
    return { type: 'rain', severity: 'light' };
  } else if (weatherId >= 500 && weatherId < 600) {
    const severity = weatherId >= 502 ? 'moderate' : 'light';
    return { type: 'rain', severity };
  } else if (weatherId >= 600 && weatherId < 700) {
    const severity = weatherId >= 602 ? 'moderate' : 'light';
    return { type: 'snow', severity };
  } else if (weatherId >= 700 && weatherId < 800) {
    return { type: 'fog', severity: 'moderate' };
  } else if (weatherId === 800) {
    return { type: 'clear', severity: 'none' };
  } else {
    // Clouds
    return { type: 'clouds', severity: 'none' };
  }
}

/**
 * Fetch real-time weather data from OpenWeatherMap API
 */
export async function fetchWeather(city: CityName): Promise<WeatherData | null> {
  const apiKey = process.env.NEXT_PUBLIC_OPENWEATHER_API_KEY;
  
  // If no API key, return null (will fall back to mock data)
  if (!apiKey) {
    console.warn('No OpenWeatherMap API key found. Using mock weather data.');
    return null;
  }

  const coords = CITY_COORDINATES[city];
  const cacheKey = `${city}-${coords.lat}-${coords.lon}`;
  
  // Check cache first
  const cached = weatherCache.get(cacheKey);
  if (cached && cached.expiry > Date.now()) {
    console.log(`Using cached weather for ${city}`);
    return cached.data;
  }

  try {
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${coords.lat}&lon=${coords.lon}&appid=${apiKey}&units=imperial`;
    
    const response = await fetch(url, {
      next: { revalidate: 1800 } // Revalidate every 30 minutes (1800 seconds)
    });

    if (!response.ok) {
      throw new Error(`Weather API error: ${response.status}`);
    }

    const data = await response.json();
    
    const { type, severity } = determineWeatherType(
      data.weather[0].main,
      data.weather[0].id,
      data.weather[0].description
    );

    const weatherData: WeatherData = {
      temperature: Math.round(data.main.temp),
      feelsLike: Math.round(data.main.feels_like),
      condition: data.weather[0].main,
      description: data.weather[0].description,
      humidity: data.main.humidity,
      windSpeed: Math.round(data.wind.speed),
      weatherType: type,
      weatherSeverity: severity,
      icon: data.weather[0].icon,
      timestamp: Date.now()
    };

    // Cache the result
    weatherCache.set(cacheKey, {
      data: weatherData,
      expiry: Date.now() + CACHE_DURATION
    });

    console.log(`Fetched fresh weather for ${city}:`, weatherData);
    return weatherData;

  } catch (error) {
    console.error(`Error fetching weather for ${city}:`, error);
    return null;
  }
}

/**
 * Get formatted weather display string
 */
export function formatWeatherDisplay(weather: WeatherData): string {
  const emoji = getWeatherEmoji(weather.weatherType);
  return `${emoji} ${weather.condition}, ${weather.temperature}°F`;
}

/**
 * Get weather emoji based on type
 */
export function getWeatherEmoji(type: WeatherData['weatherType']): string {
  const emojiMap = {
    clear: '☀️',
    rain: '🌧️',
    storm: '⛈️',
    snow: '❄️',
    fog: '🌫️',
    clouds: '☁️'
  };
  return emojiMap[type] || '🌤️';
}

/**
 * Get weather multiplier for pricing calculations
 */
export function getWeatherMultiplier(weather: WeatherData): number {
  const multipliers = {
    clear: 1.0,
    clouds: 1.0,
    rain: weather.weatherSeverity === 'light' ? 1.1 : 1.25,
    storm: 1.5,
    snow: weather.weatherSeverity === 'moderate' ? 1.4 : 1.5,
    fog: 1.2
  };
  
  return multipliers[weather.weatherType] || 1.0;
}

/**
 * Generate fallback mock weather if API fails or no API key
 */
export function generateMockWeather(city: CityName): WeatherData {
  const cityDefaults: Record<CityName, Partial<WeatherData>> = {
    'Phoenix': { temperature: 85, condition: 'Clear', weatherType: 'clear' },
    'New York': { temperature: 65, condition: 'Partly Cloudy', weatherType: 'clouds' },
    'San Francisco': { temperature: 62, condition: 'Foggy', weatherType: 'fog' },
    'Chicago': { temperature: 58, condition: 'Cloudy', weatherType: 'clouds' },
    'Orlando': { temperature: 78, condition: 'Partly Cloudy', weatherType: 'clouds' }
  };

  const defaults = cityDefaults[city];
  
  return {
    temperature: defaults.temperature || 72,
    feelsLike: (defaults.temperature || 72) - 2,
    condition: defaults.condition || 'Clear',
    description: defaults.condition?.toLowerCase() || 'clear sky',
    humidity: 45,
    windSpeed: 8,
    weatherType: defaults.weatherType || 'clear',
    weatherSeverity: 'none',
    icon: '01d',
    timestamp: Date.now()
  };
}

