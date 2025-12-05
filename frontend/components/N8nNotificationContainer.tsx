'use client';

import { useN8nNotifications } from '@/hooks/useN8nNotifications';
import N8nNotification from './N8nNotification';

export default function N8nNotificationContainer() {
  const { notifications, removeNotification } = useN8nNotifications();

  return (
    <div className="fixed top-4 right-4 z-[100] space-y-3 pointer-events-none">
      {notifications.map((notification, index) => (
        <div
          key={notification.id || index}
          className="pointer-events-auto"
          style={{
            transform: `translateY(${index * 10}px)`,
          }}
        >
          <N8nNotification
            notification={notification}
            onClose={() => notification.id && removeNotification(notification.id)}
          />
        </div>
      ))}
    </div>
  );
}

