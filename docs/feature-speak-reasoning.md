# Feature: Speak AI Reasoning 🔊

## Overview

Add a speaker button (🔊) next to the AI Reasoning section that reads the bullet points aloud using the browser's built-in text-to-speech (Web Speech API).

**Owner:** Jason  
**Priority:** Medium (Nice Demo Enhancement)  
**Estimated Effort:** 30 minutes

---

## User Story

```
As a user,
I want to click a speaker button to hear the AI reasoning read aloud,
So that I can understand the pricing decision hands-free or for accessibility.
```

---

## User Experience

### Before (Current)
```
┌─────────────────────────────────────────────┐
│ 🤖 AI Reasoning                             │
│ • NYC market: Higher base rates             │
│ • Surge demand detected in Manhattan        │
│ • Weather impact: Rain increases demand     │
│ • 🥈 SILVER member: 10% loyalty discount    │
└─────────────────────────────────────────────┘
```

### After (With Speaker)
```
┌─────────────────────────────────────────────┐
│ 🤖 AI Reasoning                        [🔊] │
│ • NYC market: Higher base rates             │
│ • Surge demand detected in Manhattan        │
│ • Weather impact: Rain increases demand     │
│ • 🥈 SILVER member: 10% loyalty discount    │
└─────────────────────────────────────────────┘

*User clicks [🔊]*

🔊 "NYC market: Higher base rates. 
    Surge demand detected in Manhattan. 
    Weather impact: Rain increases demand.
    Silver member: 10% loyalty discount applied."
```

---

## Technical Implementation

### Option 1: Simple Component (Recommended)

**File:** `frontend/components/SpeakButton.tsx`

```typescript
'use client';

import { useState } from 'react';
import { Volume2, VolumeX, Loader2 } from 'lucide-react';

interface SpeakButtonProps {
  text: string | string[];  // Can be single string or array of bullet points
  className?: string;
}

export default function SpeakButton({ text, className = '' }: SpeakButtonProps) {
  const [isSpeaking, setIsSpeaking] = useState(false);

  const speak = () => {
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    if (isSpeaking) {
      setIsSpeaking(false);
      return;
    }

    // Convert array to single string if needed
    const textToSpeak = Array.isArray(text) 
      ? text.join('. ') 
      : text;

    // Clean up text (remove emojis, special chars)
    const cleanText = textToSpeak
      .replace(/[🎯🤖💡🥇🥈🥉⚡🌧️☀️❄️]/g, '')  // Remove emojis
      .replace(/\s+/g, ' ')  // Normalize whitespace
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = 0.9;   // Slightly slower for clarity
    utterance.pitch = 1;
    utterance.volume = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  // Check if speech synthesis is supported
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
    return null;  // Don't render if not supported
  }

  return (
    <button
      onClick={speak}
      className={`p-2 rounded-lg transition-colors ${
        isSpeaking 
          ? 'bg-[#FF6A13] text-white' 
          : 'bg-gray-700 hover:bg-gray-600 text-gray-300'
      } ${className}`}
      title={isSpeaking ? 'Stop speaking' : 'Read aloud'}
      aria-label={isSpeaking ? 'Stop speaking' : 'Read aloud'}
    >
      {isSpeaking ? <VolumeX size={18} /> : <Volume2 size={18} />}
    </button>
  );
}
```

---

### Option 2: Add to PricingDisplay.tsx

**In existing file:** `frontend/components/PricingDisplay.tsx`

Find the AI Reasoning section and add:

```typescript
import SpeakButton from './SpeakButton';

// In the AI Reasoning section:
<div className="mt-4">
  <div className="flex items-center justify-between mb-2">
    <h4 className="text-sm font-semibold text-gray-400 flex items-center gap-2">
      <span>🤖</span> AI Reasoning
    </h4>
    <SpeakButton text={result.reasoning} />
  </div>
  <ul className="space-y-1">
    {result.reasoning.map((reason, index) => (
      <li key={index} className="text-sm text-gray-300 flex items-start gap-2">
        <span className="text-[#FF6A13]">•</span>
        <span>{reason}</span>
      </li>
    ))}
  </ul>
</div>
```

---

## Browser Support

The Web Speech API is supported in:
- ✅ Chrome (desktop & mobile)
- ✅ Safari (desktop & mobile)
- ✅ Edge
- ⚠️ Firefox (partial)

**Fallback:** Button simply doesn't render if not supported.

---

## Demo Script

**For Dari's Presentation:**

> "For accessibility and convenience, users can click the speaker icon to have the AI reasoning read aloud."
> 
> *Click 🔊 button*
> 
> *Browser speaks the reasoning*
> 
> "This uses the browser's built-in text-to-speech - no external APIs needed."

---

## Success Criteria

- [ ] Speaker button appears next to AI Reasoning header
- [ ] Clicking plays the reasoning aloud
- [ ] Clicking again stops playback
- [ ] Button changes appearance when speaking
- [ ] Works in Chrome and Safari
- [ ] Gracefully hidden if browser doesn't support

---

## Timeline

| Task | Owner | Time |
|------|-------|------|
| Create SpeakButton component | Jason | 15 min |
| Add to PricingDisplay | Jason | 10 min |
| Test in Chrome/Safari | Jason | 5 min |
| **Total** | | **30 min** |

---

## Notes

- This is a quick win for the demo
- Shows attention to UX/accessibility
- No external APIs or costs
- Can be expanded later for other sections

---

## Future Enhancements (If Time Permits)

### 🎤 Voice Input (Microphone)
**Status:** Planned for future / stretch goal

If time permits, we could add voice input using the Web Speech API's `SpeechRecognition`:

```typescript
// Future: Voice input for queries
const startVoiceInput = () => {
  const recognition = new (window as any).webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  
  recognition.onresult = (event: any) => {
    const transcript = event.results[0][0].transcript;
    // Send to chat bot or search
    sendMessage(transcript);
  };
  
  recognition.start();
};
```

**Use Cases:**
- 🎤 "Find all Urban rides" → Bot responds
- 🎤 "What's the price for Gold customers?" → Bot responds
- 🎤 Hands-free demo interaction

**Talking Point for Presentation:**
> "Currently we have text-to-speech for the AI reasoning. As a future enhancement, we plan to add voice input using the microphone, allowing fully hands-free interaction with the system."

---

**Document for:** Jason  
**Created:** Dec 3, 2025  
**Related:** [feature-natural-language-bot.md](./feature-natural-language-bot.md) (separate feature)

