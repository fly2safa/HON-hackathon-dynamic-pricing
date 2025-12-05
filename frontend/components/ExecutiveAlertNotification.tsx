'use client';

import React, { useState, useEffect, useImperativeHandle, forwardRef } from 'react';

interface AlertData {
  alertType: 'success' | 'warning' | 'info';
  title: string;
  message: string;
  detail?: string;
  priority: 'low' | 'medium' | 'high';
  timestamp?: string;
}

export interface ExecutiveAlertNotificationRef {
  triggerAlert: (alertData?: AlertData) => void;
}

// Main Executive Alert Component
const ExecutiveAlertNotification = forwardRef<ExecutiveAlertNotificationRef>((props, ref) => {
  const [alert, setAlert] = useState<AlertData | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const [alertIndex, setAlertIndex] = useState(0);

  // Demo alerts that rotate - first one shows on first click
  const demoAlerts: AlertData[] = [
    {
      alertType: 'success',
      title: 'Q4 Target Achieved',
      message: 'Revenue target of $2,500,000 exceeded by 1.9%',
      detail: 'Actual: $2,547,832 | Dynamic pricing contributed 23% uplift',
      priority: 'high',
      timestamp: new Date().toISOString()
    },
    {
      alertType: 'warning',
      title: 'Surge Pricing Active',
      message: 'High demand detected in Phoenix metropolitan area',
      detail: '2.1x multiplier applied | 847 ride requests in queue',
      priority: 'high',
      timestamp: new Date().toISOString()
    },
    {
      alertType: 'success',
      title: 'New Market Milestone',
      message: 'Phoenix coverage expanded to 95% of metro area',
      detail: '12 new zones added | Expected +$180K monthly revenue',
      priority: 'medium',
      timestamp: new Date().toISOString()
    },
    {
      alertType: 'info',
      title: 'Driver Performance Report',
      message: 'Top 10% of drivers earned average $285 today',
      detail: 'Fleet utilization at 89% | Customer satisfaction 4.8★',
      priority: 'medium',
      timestamp: new Date().toISOString()
    }
  ];

  // Simulated alert for demo - rotates through different messages
  const triggerDemoAlert = (customAlert?: AlertData) => {
    const demoAlert: AlertData = customAlert || {
      ...demoAlerts[alertIndex],
      timestamp: new Date().toISOString()
    };
    
    setAlert(demoAlert);
    setIsVisible(true);
    // Rotate to next alert for next click
    setAlertIndex((prev) => (prev + 1) % demoAlerts.length);
  };

  // Expose trigger function via ref
  useImperativeHandle(ref, () => ({
    triggerAlert: triggerDemoAlert
  }));

  // Auto-dismiss after 10 seconds
  useEffect(() => {
    if (isVisible) {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 10000);
      return () => clearTimeout(timer);
    }
  }, [isVisible]);

  const dismissAlert = () => {
    setIsVisible(false);
  };

  const alertStyles = {
    success: {
      bg: 'bg-white',
      border: 'border-l-4 border-l-emerald-600',
      iconBg: 'bg-emerald-50',
      iconColor: 'text-emerald-600',
      accentColor: 'text-emerald-600',
      titleColor: 'text-gray-900'
    },
    warning: {
      bg: 'bg-white',
      border: 'border-l-4 border-l-amber-600',
      iconBg: 'bg-amber-50',
      iconColor: 'text-amber-600',
      accentColor: 'text-amber-600',
      titleColor: 'text-gray-900'
    },
    info: {
      bg: 'bg-white',
      border: 'border-l-4 border-l-blue-600',
      iconBg: 'bg-blue-50',
      iconColor: 'text-blue-600',
      accentColor: 'text-blue-600',
      titleColor: 'text-gray-900'
    }
  };

  const style = alert ? alertStyles[alert.alertType] || alertStyles.info : alertStyles.info;

  return (
    <>
      {/* Alert Notification */}
      <div
        className={`fixed top-6 right-6 z-50 transition-all duration-300 ease-out ${
          isVisible 
            ? 'opacity-100 translate-x-0' 
            : 'opacity-0 translate-x-full pointer-events-none'
        }`}
      >
        {alert && (
          <div className={`${style.bg} ${style.border} border-t border-r border-b border-gray-200 rounded-lg shadow-xl p-6 min-w-[420px] max-w-lg`}>
            {/* Header */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-start gap-4">
                <div className={`${style.iconBg} w-12 h-12 rounded-lg flex items-center justify-center shrink-0`}>
                  {alert.alertType === 'success' && (
                    <svg className={`w-6 h-6 ${style.iconColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                  {alert.alertType === 'warning' && (
                    <svg className={`w-6 h-6 ${style.iconColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                  )}
                  {alert.alertType === 'info' && (
                    <svg className={`w-6 h-6 ${style.iconColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                </div>
                <div className="flex-1">
                  <h3 className={`${style.titleColor} font-semibold text-lg leading-tight mb-1`}>{alert.title}</h3>
                  <p className="text-gray-500 text-xs font-medium">n8n Automation • {new Date(alert.timestamp || Date.now()).toLocaleTimeString()}</p>
                </div>
              </div>
              <button 
                onClick={dismissAlert}
                className="text-gray-400 hover:text-gray-600 transition-colors text-xl leading-none ml-2"
                aria-label="Dismiss alert"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Message */}
            <div className="mb-4">
              <p className="text-gray-800 font-medium text-base mb-2 leading-relaxed">{alert.message}</p>
              {alert.detail && (
                <p className="text-gray-600 text-sm leading-relaxed">{alert.detail}</p>
              )}
            </div>

            {/* Metric Visualization */}
            <div className="bg-gray-50 rounded-lg p-4 mb-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-600 text-xs font-medium uppercase tracking-wide">Target Achievement</span>
                <span className={`${style.accentColor} font-semibold text-sm`}>101.9%</span>
              </div>
              <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                <div 
                  className={`h-full ${style.accentColor.replace('text-', 'bg-')} rounded-full transition-all duration-1000`}
                  style={{ width: '101.9%', maxWidth: '100%' }}
                />
              </div>
            </div>

            {/* Footer */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200">
              <span className="text-gray-500 text-xs font-medium">HoneyGo AI Platform</span>
              <button 
                onClick={dismissAlert}
                className="text-gray-600 hover:text-gray-900 text-sm font-medium transition-colors"
              >
                Dismiss
              </button>
            </div>
          </div>
        )}
      </div>
    </>
  );
});

ExecutiveAlertNotification.displayName = 'ExecutiveAlertNotification';

export default ExecutiveAlertNotification;

