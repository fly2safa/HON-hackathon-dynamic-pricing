# API Usage Tips & Best Practices

Quick reference for managing OpenWeatherMap API usage during development.

---

## 📊 Current Configuration

- **Cache Duration:** 30 minutes
- **Free Tier Limit:** 1,000 calls/day
- **Expected Usage:** 100-400 calls/day (4 team members)
- **Safety Margin:** 600-900 calls remaining

---

## 🎯 Quick Actions

### Enable/Disable Real Weather

**To DISABLE real weather (use mock data):**
```bash
cd frontend
# Rename or remove .env.local temporarily
mv .env.local .env.local.backup
```

**To RE-ENABLE real weather:**
```bash
cd frontend
# Restore .env.local
mv .env.local.backup .env.local
```

### Check API Usage

1. Go to: https://home.openweathermap.org/
2. Log in
3. Click "API keys" in the menu
4. View usage statistics for your key

---

## 💡 Development Workflow

### For UI Development (No weather needed)
```bash
# Disable real weather
cd frontend
mv .env.local .env.local.backup
npm run dev
```
✅ Uses mock data  
✅ No API calls  
✅ Faster development  

### For Testing Weather Features
```bash
# Enable real weather
cd frontend
mv .env.local.backup .env.local
npm run dev
```
✅ Real-time data  
✅ Minimal API calls (30-min cache)  

### For Demos/Presentations
```bash
# Enable real weather
cd frontend
# Make sure .env.local exists
npm run dev
```
✅ Shows live data  
✅ "🌐 Live" badge visible  
✅ Impressive for judges!  

---

## 📈 API Call Estimator

### Individual Developer (8-hour day)

| Activity | Calls/Day |
|----------|-----------|
| Working on 1 city | ~16 |
| Testing 3 cities | ~48 |
| Testing all 5 cities | ~80 |

### Team of 4 (8-hour day)

| Scenario | Calls/Day | % of Limit |
|----------|-----------|------------|
| Normal development | 100-200 | 10-20% |
| Active testing | 200-400 | 20-40% |
| Maximum (all cities) | 320 | 32% |

**All scenarios well within 1,000 limit! ✅**

---

## 🛡️ Safety Features

### Built-in Protections

1. **30-Minute Cache**
   - Prevents excessive calls
   - Shared across all tabs

2. **Automatic Fallback**
   - If API limit hit → uses mock data
   - App never breaks

3. **Smart Fetching**
   - Only fetches on city change
   - No polling or continuous calls

4. **Browser Tab Handling**
   - Inactive tabs don't make calls
   - Cache persists across refreshes

---

## 🚨 If You Hit the Limit

**Symptoms:**
- Console shows: "Rate limit exceeded"
- Weather shows mock data instead

**Solutions:**

### Immediate (Same Day):
1. App automatically uses mock data
2. Everything still works!
3. Wait until midnight UTC for reset

### Temporary:
```bash
# Disable real weather, use mock data
cd frontend
mv .env.local .env.local.backup
# Restart frontend
```

### Long-term:
- Review who needs real weather access
- Consider creating separate API keys per person
- Upgrade to paid tier if needed (unlikely)

---

## 👥 Team Coordination

### Best Practices

1. **During Development:**
   - Most team members use mock data
   - Only 1-2 people test real weather

2. **Before Demo:**
   - Enable real weather
   - Test all cities once
   - Close unused browser tabs

3. **During Demo:**
   - Use real weather (impressive!)
   - Only presenter's browser open
   - Share screen instead of multiple viewers

4. **After Hours:**
   - Close all browser tabs
   - Stops any background fetching

---

## 📊 Monitoring Dashboard

Visit your OpenWeatherMap dashboard to track usage:

**URL:** https://home.openweathermap.org/api_keys

**What to Check:**
- Calls in last hour
- Calls today
- Percentage of daily limit used
- Historical usage patterns

**When to Check:**
- End of each day
- Before important demos
- If you suspect issues

---

## 🎓 Pro Tips

### Minimize API Calls

1. **Use Mock Data by Default**
   - Only enable real weather when testing weather features
   - Mock data is realistic and works great

2. **Close Unused Tabs**
   - Each open tab might cache weather
   - Close tabs when switching tasks

3. **Test Intentionally**
   - Don't randomly switch cities
   - Test specific scenarios

4. **Share During Demos**
   - One person shares screen
   - Others watch, don't open own browsers

### Maximize Effectiveness

1. **Enable for Demos**
   - Shows judges you have real integration
   - "🌐 Live" badge proves it's real

2. **Test All Cities Once**
   - Verify all 5 locations work
   - Then rely on cache for 30 minutes

3. **Monitor Before Big Events**
   - Check usage day before demo
   - Ensure plenty of quota remaining

---

## 📞 Quick Reference

| Need | Command |
|------|---------|
| Disable weather | `mv .env.local .env.local.backup` |
| Enable weather | `mv .env.local.backup .env.local` |
| Check usage | Visit https://home.openweathermap.org/api_keys |
| Test API key | `node frontend/test-weather-api.js` |
| View cache logs | Check browser console (F12) |

---

## ✅ Daily Checklist

**Morning:**
- [ ] Check API usage from yesterday
- [ ] Decide if you need real weather today
- [ ] Enable/disable accordingly

**During Work:**
- [ ] Use mock data for UI work
- [ ] Enable real weather only for weather features
- [ ] Close tabs when switching tasks

**End of Day:**
- [ ] Close all browser tabs
- [ ] Check daily API usage
- [ ] Review if approaching limit (unlikely)

---

**Remember:** The app works perfectly with mock data! Only use real weather when you specifically need to test weather features or impress during demos. 🎯

