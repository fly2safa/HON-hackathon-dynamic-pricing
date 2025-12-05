'use client';

import { useState, useEffect } from 'react';

export interface N8nNotificationData {
  id?: string;
  title: string;
  message: string;
  type?: 'success' | 'info' | 'warning' | 'error';
  duration?: number;
  action?: {
    label: string;
    url?: string;
    onClick?: () => void;
  };
}

interface N8nNotificationProps {
  notification: N8nNotificationData;
  onClose: () => void;
}

export default function N8nNotification({ notification, onClose }: N8nNotificationProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    // Trigger entrance animation
    setTimeout(() => setIsVisible(true), 10);

    // Auto-close after duration
    const duration = notification.duration || 5000;
    const timer = setTimeout(() => {
      handleClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [notification.duration]);

  const handleClose = () => {
    setIsExiting(true);
    setTimeout(() => {
      onClose();
    }, 300); // Match animation duration
  };

  const handleAction = () => {
    if (notification.action?.onClick) {
      notification.action.onClick();
    } else if (notification.action?.url) {
      window.open(notification.action.url, '_blank');
    }
    handleClose();
  };

  const typeStyles = {
    success: 'bg-green-500 border-green-600',
    info: 'bg-blue-500 border-blue-600',
    warning: 'bg-orange-500 border-orange-600',
    error: 'bg-red-500 border-red-600',
  };

  const iconStyles = {
    success: '✓',
    info: 'ℹ',
    warning: '⚠',
    error: '✕',
  };

  const type = notification.type || 'info';
  const style = typeStyles[type];
  const icon = iconStyles[type];

  return (
    <div
      className={`
        fixed top-4 right-4 z-[100] 
        min-w-[320px] max-w-[420px]
        bg-white rounded-lg shadow-2xl border-2 ${style}
        transform transition-all duration-300 ease-out
        ${isVisible && !isExiting ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
      `}
      style={{
        animation: isVisible && !isExiting ? 'slideInRight 0.3s ease-out' : undefined,
      }}
    >
      <div className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <div className={`w-8 h-8 rounded-full ${style} flex items-center justify-center text-white font-bold text-sm`}>
              {icon}
            </div>
            <h3 className="font-bold text-gray-900 text-sm">{notification.title}</h3>
          </div>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close notification"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        {/* Message */}
        <p className="text-gray-700 text-sm mb-3">{notification.message}</p>

        {/* Action Button */}
        {notification.action && (
          <button
            onClick={handleAction}
            className={`
              w-full px-4 py-2 rounded-md font-semibold text-sm
              transition-all duration-200
              ${style} text-white hover:opacity-90
              transform hover:scale-[1.02] active:scale-[0.98]
            `}
          >
            {notification.action.label}
          </button>
        )}
      </div>

      {/* Progress Bar */}
      {notification.duration && (
        <div className="h-1 bg-gray-200 rounded-b-lg overflow-hidden">
          <div
            className={`h-full ${style.replace('bg-', 'bg-').replace('border-', 'bg-')}`}
            style={{
              animation: `shrink ${notification.duration}ms linear forwards`,
            }}
          />
        </div>
      )}

      <style jsx>{`
        @keyframes slideInRight {
          from {
            transform: translateX(100%);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }

        @keyframes shrink {
          from {
            width: 100%;
          }
          to {
            width: 0%;
          }
        }
      `}</style>
    </div>
  );
}

