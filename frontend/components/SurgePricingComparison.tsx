'use client';

import React, { useState } from 'react';

export default function SurgePricingComparison() {
  const [activeScenario, setActiveScenario] = useState<'baseline' | 'peak' | 'weather' | 'goldMember'>('peak');

  const scenarios = {
    baseline: {
      name: 'Baseline',
      time: 'Tuesday 2:00 PM',
      weather: 'Clear',
      event: 'None',
      demand: 'Normal',
      supply: 'Normal',
      factors: [
        { name: 'Base Rate', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Time of Day', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Weather', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Events', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Demand/Supply', value: 1.0, impact: 0, color: '#6B7280' },
      ],
      finalSurge: 1.0,
      reasoning: 'Normal conditions. No surge factors present.',
    },
    peak: {
      name: 'Peak Demand',
      time: 'Friday 6:00 PM',
      weather: 'Light Rain',
      event: 'Suns Game Ending',
      demand: 'Very High',
      supply: 'Low',
      factors: [
        { name: 'Base Rate', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Time of Day', value: 1.2, impact: 0.2, color: '#F59E0B' },
        { name: 'Weather', value: 1.15, impact: 0.15, color: '#3B82F6' },
        { name: 'Events', value: 1.25, impact: 0.25, color: '#8B5CF6' },
        { name: 'Demand/Supply', value: 1.15, impact: 0.15, color: '#EF4444' },
      ],
      finalSurge: 1.75,
      reasoning: 'Multiple surge factors: Rush hour (+20%), rain increases requests (+15%), stadium event ending (+25%), driver shortage (+15%). Capped at jurisdiction max.',
    },
    weather: {
      name: 'Weather Event',
      time: 'Saturday 3:00 PM',
      weather: 'Heavy Rain',
      event: 'None',
      demand: 'High',
      supply: 'Normal',
      factors: [
        { name: 'Base Rate', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Time of Day', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Weather', value: 1.35, impact: 0.35, color: '#3B82F6' },
        { name: 'Events', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Demand/Supply', value: 1.1, impact: 0.1, color: '#EF4444' },
      ],
      finalSurge: 1.45,
      reasoning: 'Heavy rain drives demand spike (+35%). Moderate supply pressure (+10%). No time or event factors.',
    },
    goldMember: {
      name: 'Gold Member',
      time: 'Friday 6:00 PM',
      weather: 'Light Rain',
      event: 'Suns Game Ending',
      demand: 'Very High',
      supply: 'Low',
      factors: [
        { name: 'Base Rate', value: 1.0, impact: 0, color: '#6B7280' },
        { name: 'Time of Day', value: 1.2, impact: 0.2, color: '#F59E0B' },
        { name: 'Weather', value: 1.15, impact: 0.15, color: '#3B82F6' },
        { name: 'Events', value: 1.25, impact: 0.25, color: '#8B5CF6' },
        { name: 'Loyalty Discount', value: 0.85, impact: -0.15, color: '#10B981' },
      ],
      finalSurge: 1.49,
      reasoning: 'Same peak conditions, but Gold member loyalty discount (-15%) reduces final surge. Tier benefits preserved even during high demand.',
    },
  };

  const current = scenarios[activeScenario];
  const baseline = scenarios.baseline;

  return (
    <div className="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6 font-sans">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-white mb-1">HoneyGo Surge Pricing</h1>
          <p className="text-slate-400">See exactly <span className="text-amber-400 font-semibold">why</span> prices change</p>
        </div>
        <div className="flex justify-center gap-2 mb-6 flex-wrap">
          {Object.entries(scenarios).map(([key, scenario]) => (
            <button
              key={key}
              onClick={() => setActiveScenario(key as 'baseline' | 'peak' | 'weather' | 'goldMember')}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                activeScenario === key
                  ? 'bg-red-600 text-white shadow-lg'
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {scenario.name}
            </button>
          ))}
        </div>
        <div className="grid md:grid-cols-2 gap-4 mb-6">
          <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-semibold text-slate-300">Baseline</h2>
              <span className="text-2xl font-bold text-slate-400">1.0x</span>
            </div>
            <div className="space-y-1 text-sm text-slate-400">
              <div className="flex justify-between"><span>📅 Time:</span><span>{baseline.time}</span></div>
              <div className="flex justify-between"><span>🌤️ Weather:</span><span>{baseline.weather}</span></div>
              <div className="flex justify-between"><span>🎭 Event:</span><span>{baseline.event}</span></div>
              <div className="flex justify-between"><span>📊 Demand:</span><span>{baseline.demand}</span></div>
            </div>
          </div>
          <div className="bg-slate-800/50 rounded-xl p-4 border border-red-600/50 shadow-lg shadow-red-600/10">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-lg font-semibold text-white">{current.name}</h2>
              <span className={`text-2xl font-bold ${current.finalSurge > 1.5 ? 'text-red-400' : current.finalSurge > 1.2 ? 'text-amber-400' : 'text-green-400'}`}>
                {current.finalSurge.toFixed(2)}x
              </span>
            </div>
            <div className="space-y-1 text-sm text-slate-300">
              <div className="flex justify-between"><span>📅 Time:</span><span className={current.time !== baseline.time ? 'text-amber-400' : ''}>{current.time}</span></div>
              <div className="flex justify-between"><span>🌤️ Weather:</span><span className={current.weather !== baseline.weather ? 'text-blue-400' : ''}>{current.weather}</span></div>
              <div className="flex justify-between"><span>🎭 Event:</span><span className={current.event !== baseline.event ? 'text-purple-400' : ''}>{current.event}</span></div>
              <div className="flex justify-between"><span>📊 Demand:</span><span className={current.demand !== baseline.demand ? 'text-red-400' : ''}>{current.demand}</span></div>
            </div>
          </div>
        </div>
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700 mb-6">
          <h3 className="text-md font-semibold text-white mb-3">Factor Breakdown</h3>
          <div className="space-y-2">
            {current.factors.map((factor, index) => (
              <div key={index} className="flex items-center gap-3">
                <div className="w-28 text-xs text-slate-400">{factor.name}</div>
                <div className="flex-1 h-6 bg-slate-700 rounded overflow-hidden relative">
                  <div 
                    className="h-full rounded transition-all duration-500 flex items-center justify-end pr-2"
                    style={{ width: `${(factor.value / 1.5) * 100}%`, backgroundColor: factor.color }}
                  >
                    <span className="text-xs font-bold text-white">{factor.value.toFixed(2)}x</span>
                  </div>
                  <div className="absolute top-0 bottom-0 left-[66.67%] w-px bg-white/30"></div>
                </div>
                <div className={`w-14 text-right text-xs font-medium ${
                  factor.impact > 0 ? 'text-red-400' : factor.impact < 0 ? 'text-green-400' : 'text-slate-500'
                }`}>
                  {factor.impact > 0 ? '+' : ''}{(factor.impact * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="bg-gradient-to-r from-slate-800 to-slate-800/50 rounded-xl p-4 border border-amber-600/30">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-amber-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <span className="text-lg">🤖</span>
            </div>
            <div>
              <h3 className="text-md font-semibold text-amber-400 mb-1">Agent Reasoning</h3>
              <p className="text-slate-300 text-sm leading-relaxed">{current.reasoning}</p>
            </div>
          </div>
        </div>
        <div className="mt-4 flex justify-center gap-4 flex-wrap text-xs text-slate-400">
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-amber-500"></div><span>Time</span></div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-blue-500"></div><span>Weather</span></div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-purple-500"></div><span>Event</span></div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-red-500"></div><span>Demand</span></div>
          <div className="flex items-center gap-1"><div className="w-2 h-2 rounded bg-green-500"></div><span>Loyalty</span></div>
        </div>
      </div>
    </div>
  );
}

