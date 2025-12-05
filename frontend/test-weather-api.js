/**
 * Quick test script to verify OpenWeatherMap API key
 * Run: node test-weather-api.js
 */

const fs = require('fs');
const path = require('path');

// Load .env.local file
const envPath = path.join(__dirname, '.env.local');
let apiKey = null;

if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const match = envContent.match(/NEXT_PUBLIC_OPENWEATHER_API_KEY=(.+)/);
  if (match) {
    apiKey = match[1].trim();
  }
}

if (!apiKey || apiKey === 'your_actual_api_key_here') {
  console.log('❌ No valid API key found in .env.local');
  console.log('');
  console.log('Please create frontend/.env.local with:');
  console.log('NEXT_PUBLIC_OPENWEATHER_API_KEY=your_actual_api_key');
  console.log('');
  console.log('Get a free key from: https://home.openweathermap.org/api_keys');
  process.exit(1);
}

console.log('🔑 API Key found:', apiKey.substring(0, 8) + '...' + apiKey.substring(apiKey.length - 4));
console.log('📍 Testing Phoenix Sky Harbor Airport...');
console.log('');

// Test API call
const testLocation = {
  name: 'Phoenix',
  lat: 33.4343,
  lon: -112.0080
};

const url = `https://api.openweathermap.org/data/2.5/weather?lat=${testLocation.lat}&lon=${testLocation.lon}&appid=${apiKey}&units=imperial`;

fetch(url)
  .then(response => {
    if (!response.ok) {
      if (response.status === 401) {
        throw new Error('Invalid API key or not activated yet (wait 10-15 minutes after creation)');
      } else if (response.status === 429) {
        throw new Error('Rate limit exceeded (60 calls/minute or 1000 calls/day)');
      } else {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
    }
    return response.json();
  })
  .then(data => {
    console.log('✅ SUCCESS! Real weather data received:');
    console.log('');
    console.log('📊 Weather Data:');
    console.log('  Location:', data.name);
    console.log('  Temperature:', Math.round(data.main.temp) + '°F');
    console.log('  Feels Like:', Math.round(data.main.feels_like) + '°F');
    console.log('  Condition:', data.weather[0].main);
    console.log('  Description:', data.weather[0].description);
    console.log('  Humidity:', data.main.humidity + '%');
    console.log('  Wind Speed:', Math.round(data.wind.speed) + ' mph');
    console.log('');
    console.log('🎉 Your API key is working correctly!');
    console.log('💡 Refresh your browser to see live weather in the app');
  })
  .catch(error => {
    console.log('❌ ERROR:', error.message);
    console.log('');
    if (error.message.includes('not activated')) {
      console.log('⏰ Wait 10-15 minutes after creating your API key');
      console.log('   New API keys take time to activate');
    } else if (error.message.includes('Invalid API key')) {
      console.log('🔑 Check your API key at: https://home.openweathermap.org/api_keys');
      console.log('   Make sure it\'s copied correctly in .env.local');
    }
    process.exit(1);
  });

