# 🔔 n8n Executive Alert Integration Guide

> **Purpose:** Deliver Emotional Beat #4 — Transform "reactive firefighting" → "proactive monitoring"  
> **Demo Impact:** High — this is the "wow" moment that makes leadership care

---

## 🎯 Transformation Goal

| Before | After |
|--------|-------|
| "We find out about problems in weekly reports" | "We know instantly when thresholds are crossed" |
| "Firefighting after margin leakage" | "Catching anomalies before they cost money" |
| "AI runs in the background somewhere" | "AI actively notifies the right people" |

---

## 🎬 Demo Script (Transformation Version)

During Safa's demo, after showing hierarchy enforcement:

> **SAFA:** "Fourth—can you actually monitor this at scale?
>
> We integrated n8n workflow automation. Watch what happens when a key metric threshold is crossed."
>
> *[Triggers the n8n workflow]*
>
> *[Notification slides in with confetti]*
>
> **SAFA:** "Q4 revenue target achieved. The n8n workflow detected the threshold, formatted the alert, and pushed it to the executive dashboard—instantly.
>
> Not in tomorrow's report. Not in next week's review. **Now.**
>
> This same pattern works for margin alerts, hierarchy violations, competitor signals, anomaly detection.
>
> **Transformation:** You're not firefighting after the fact. You're monitoring in real-time."

---

## 🔗 Honeywell Connection (Say This)

> "This same automation pattern applies to Honeywell:
> - **Margin Alert:** 'Catalog price on SKU-7842 dropped below 15% margin'
> - **Hierarchy Violation:** 'Attempted to price UFR above New Spare — blocked'
> - **Competitor Signal:** 'PMA pricing detected 12% below catalog'
> - **Target Achievement:** 'Q4 Aerospace revenue target exceeded'
>
> The n8n workflow can trigger from any data source — ERP, CRM, external APIs — and push real-time alerts to the right people."

---

## 📦 Files Included

| File | Purpose |
|------|---------|
| `n8n_executive_alert_workflow.json` | Import into n8n |
| `ExecutiveAlertNotification.tsx` | React notification component |
| `notifications.py` | FastAPI backend endpoint |

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Import n8n Workflow

1. Open n8n (http://localhost:5678)
2. Click **"..."** → **Import from File**
3. Select `n8n_executive_alert_workflow.json`
4. Click **Activate** toggle (top right)
5. Note the webhook URL: `http://localhost:5678/webhook/trigger-executive-alert`

### Step 2: Add Backend Endpoint

Add to your FastAPI `main.py`:

```python
from routers.notifications import router as notifications_router
app.include_router(notifications_router)
```

### Step 3: Add Frontend Component

Add to your Next.js layout or page:

```tsx
import ExecutiveAlertNotification from '@/components/ExecutiveAlertNotification';

export default function DemoLayout({ children }) {
  return (
    <>
      {children}
      <ExecutiveAlertNotification />
    </>
  );
}
```

### Step 4: Test It

```bash
# Option A: Trigger via n8n webhook
curl -X POST http://localhost:5678/webhook/trigger-executive-alert

# Option B: Trigger via FastAPI test endpoint
curl -X POST http://localhost:8000/api/notifications/test

# Option C: Click the red "Trigger Executive Alert" button in the UI
```

---

## 🔄 How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   n8n Trigger   │────▶│  FastAPI POST   │────▶│  React SSE      │
│   (Webhook)     │     │  /executive-    │     │  Notification   │
│                 │     │  alert          │     │  + Confetti!    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
   Manual click            Broadcasts to           Slides in from
   or scheduled            all connected           right, auto-
   automation              clients via SSE          dismisses
```

---

## 🎯 Demo Triggers

### Option A: Manual Button (Easiest)
The React component includes a red **"Trigger Executive Alert"** button in the bottom-right corner. Just click it during the demo.

### Option B: n8n Webhook (Shows Automation)
1. Keep n8n open in a browser tab
2. During demo, click **"Execute Workflow"** in n8n
3. Notification appears in HoneyGo frontend

### Option C: Keyboard Shortcut (Slick)
Add this to your frontend:

```tsx
useEffect(() => {
  const handleKeyPress = (e) => {
    if (e.ctrlKey && e.key === 'n') {
      triggerDemoAlert();
    }
  };
  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, []);
```

Then press **Ctrl+N** during demo.

---

## 🎨 Customization

### Change Alert Content

Edit the `Set Metric Data` node in n8n:

```json
{
  "metricName": "Q4 Revenue Target",
  "targetValue": 2500000,
  "actualValue": 2547832,
  "achievementPct": 101.9
}
```

### Change Alert Style

In `ExecutiveAlertNotification.tsx`, modify `alertStyles`:

```tsx
const alertStyles = {
  success: {
    bg: 'bg-gradient-to-r from-emerald-600 to-emerald-700',
    border: 'border-emerald-400',
    icon: '✓',
    iconBg: 'bg-emerald-500'
  },
  // Add custom styles...
};
```

### Disable Confetti

Set `showConfetti: false` in the n8n workflow or alert data.

---

## 🔗 HON Connection

During the demo, connect this to Honeywell:

> "This same automation pattern applies to Honeywell scenarios:
> - **Alert when catalog price breaches margin threshold**
> - **Notify when competitor pricing detected**
> - **Flag when hierarchy violation attempted**
> - **Celebrate when quarterly targets hit**
>
> The n8n workflow can trigger from any data source — ERP, CRM, external APIs — and push real-time alerts to executives."

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| n8n webhook not triggering | Make sure workflow is **Activated** (toggle top-right) |
| CORS error | Add frontend origin to FastAPI CORS middleware |
| SSE not connecting | Check browser console, verify `/api/notifications/stream` endpoint |
| Notification not showing | Check React component is mounted in layout |
| Confetti not animating | Ensure Tailwind JIT is processing the component |

---

## ✅ Pre-Demo Checklist

- [ ] n8n workflow imported and activated
- [ ] FastAPI notifications endpoint added
- [ ] React component added to layout
- [ ] Test trigger works (button or webhook)
- [ ] Confetti animation looks good
- [ ] Know which trigger method you'll use (button/n8n/keyboard)

---

**Good luck with the demo! 🐝**

