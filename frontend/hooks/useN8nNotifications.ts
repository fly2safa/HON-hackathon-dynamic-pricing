'use client';

import { useState, useCallback, useEffect } from 'react';
import { N8nNotificationData } from '@/components/N8nNotification';

export function useN8nNotifications() {
  const [notifications, setNotifications] = useState<N8nNotificationData[]>([]);

  const addNotification = useCallback((notification: N8nNotificationData) => {
    const id = notification.id || `n8n-${Date.now()}-${Math.random()}`;
    const newNotification = { ...notification, id };
    setNotifications(prev => [...prev, newNotification]);
    return id;
  }, []);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  // Listen for n8n notification events from backend
  useEffect(() => {
    const checkN8nNotifications = async () => {
      try {
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
        const response = await fetch(`${backendUrl}/api/v1/n8n/notifications`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.notifications && Array.isArray(data.notifications)) {
            data.notifications.forEach((notif: N8nNotificationData) => {
              addNotification(notif);
            });
          }
        }
      } catch (error) {
        // Silently fail - n8n notifications are optional
        console.debug('N8n notification check failed:', error);
      }
    };

    // Check every 5 seconds for new notifications
    const interval = setInterval(checkN8nNotifications, 5000);
    checkN8nNotifications(); // Initial check

    return () => clearInterval(interval);
  }, [addNotification]);

  return {
    notifications,
    addNotification,
    removeNotification,
  };
}

