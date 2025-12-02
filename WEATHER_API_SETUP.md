# Real-Time Weather API Setup Guide

Get live weather data for exact locations using OpenWeatherMap API.

---

## 🌍 Location Coordinates

Weather data is fetched for these specific locations:

| City | Location | Coordinates |
|------|----------|-------------|
| 🌵 **Phoenix** | Phoenix Sky Harbor Airport | 33.4343°N, 112.0080°W |
| 🗽 **New York** | JFK Airport | 40.6413°N, 73.7781°W |
| 🌉 **San Francisco** | San Francisco City Hall | 37.7793°N, 122.4193°W |
| 🏙️ **Chicago** | Willis Tower | 41.8789°N, 87.6359°W |
| 🏰 **Orlando** | Orlando International Airport | 28.4312°N, 81.3081°W |

---

## 🔑 Step 1: Get OpenWeatherMap API Key (FREE)

### Sign Up
1. Go to https://openweathermap.org/
2. Click "Sign Up" (top right)
3. Create a free account (no credit card required)

### Get API Key
1. Go to https://home.openweathermap.org/api_keys
2. Copy your default API key (or create a new one)
3. **API key activation takes ~10 minutes** after creation

### Free Tier Limits
- ✅ **1,000 API calls/day**
- ✅ **60 calls/minute**
- ✅ Perfect for development and demos

---

## ⚙️ Step 2: Configure Frontend

### Create .env.local file

```bash
cd /home/jason/Python/AzNext_VibeCoding/HON-hackathon-dynamic-pricing/frontend
```

Create a file named `.env.local` with this content:

```bash
# OpenWeatherMap API Key
NEXT_PUBLIC_OPENWEATHER_API_KEY=your_actual_api_key_here

# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Replace `your_actual_api_key_here` with your actual API key!**

### Example:
```bash
NEXT_PUBLIC_OPENWEATHER_API_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 Step 3: Restart Frontend

After adding the API key:

```bash
# Stop the current frontend (Ctrl+C in the terminal running it)

# Start it again
cd frontend
npm run dev
```

The frontend will now fetch real-time weather data! 🎉

---

## 📊 How It Works

### With API Key (Real Weather):
1. App fetches weather every 5 minutes
2. Data cached to avoid excessive API calls
3. Shows real temperature, conditions, and weather icons
4. Pricing multipliers based on actual conditions

### Without API Key (Mock Data):
1. App uses realistic mock weather data
2. Still shows weather UI
3. Works offline
4. Good for testing without API limits

---

## 🔍 Verify It's Working

### Check Browser Console

Open your browser console (F12) and look for:

```
Fetched fresh weather for Phoenix: {...}
Using cached weather for Phoenix
```

### Weather Display

You should see live weather like:
- ☀️ Clear, 85°F (with green "🌐 Live" badge)
- 🌧️ Rain, 62°F (with location name below)
- ⛈️ Thunderstorm, 55°F

### Fallback Message

If no API key is set, you'll see:
```
No OpenWeatherMap API key found. Using mock weather data.
```

---

## ⚡ API Usage & Caching

### Cache Duration: 30 Minutes

Weather data is cached for **30 minutes** to minimize API calls:
- First visit: Fetches from API
- Next 30 minutes: Uses cached data
- After 30 minutes: Fetches fresh data

### Expected Usage

**4 Team Members, 8-hour workday:**
- Calls per person per city: ~16 (every 30 min for 8 hours)
- Maximum per day (5 cities × 4 people × 16): ~320 calls
- **Well within 1,000 calls/day limit! ✅**

**Conservative estimate:**
- 100-200 calls/day with typical usage
- Plenty of headroom for demos and testing

---

## 🛠️ Troubleshooting

### "Invalid API key" Error

**Cause:** API key not activated yet (takes ~10 min after creation)

**Solution:** Wait 10-15 minutes and refresh

### Weather Not Updating

**Cause:** Cache is working (updates every 5 minutes)

**Solution:** This is normal! Weather cached for performance

### Rate Limit Exceeded

**Cause:** More than 60 calls/minute

**Solution:** 
- Weather is cached for 5 minutes to prevent this
- If hit anyway, mock data will be used
- Upgrade to paid plan if needed

---

## 💡 Tips

### For Development:
- Use mock data to avoid API limits while coding
- Only enable real weather for demos/testing

### For Demo Day:
- Ensure API key is in .env.local
- Check weather is loading before presenting
- Have backup mock data ready

### For Production:
- Use environment variables on hosting platform
- Monitor API usage in OpenWeatherMap dashboard
- Consider upgrading if >1000 calls/day needed

---

## 🎯 Quick Commands

```bash
# Create .env.local
cd frontend
echo "NEXT_PUBLIC_OPENWEATHER_API_KEY=your_key" > .env.local

# Check if it's loaded
grep OPENWEATHER .env.local

# Restart frontend
npm run dev
```

---

## 📚 Resources

- **OpenWeatherMap Docs:** https://openweathermap.org/current
- **API Dashboard:** https://home.openweathermap.org/
- **Pricing Plans:** https://openweathermap.org/price

---

**Ready to see real weather? Add your API key and restart the frontend!** 🌤️

