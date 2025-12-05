# backend/routers/notifications.py
# FastAPI endpoint for n8n executive alerts

from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import asyncio

router = APIRouter(prefix="/api/v1/n8n", tags=["notifications"])

# In-memory store for alerts (use Redis in production)
alert_store: List[dict] = []
alert_subscribers: List[asyncio.Queue] = []


class ExecutiveAlert(BaseModel):
    alertType: str  # "success", "warning", "info"
    title: str
    message: str
    detail: Optional[str] = None
    priority: str = "medium"  # "low", "medium", "high"
    timestamp: Optional[str] = None


class AlertResponse(BaseModel):
    status: str
    alertId: str
    broadcastCount: int


@router.post("/executive-alert", response_model=AlertResponse)
async def receive_executive_alert(
    alert: ExecutiveAlert,
    x_alert_source: Optional[str] = Header(None)
):
    """
    Receive executive alert from n8n automation.
    Broadcasts to all connected frontend clients via SSE.
    """
    # Validate source (optional security)
    if x_alert_source != "n8n-automation":
        # Log but don't reject - allows manual testing
        print(f"Alert received from non-n8n source: {x_alert_source}")
    
    # Add timestamp if not provided
    if not alert.timestamp:
        alert.timestamp = datetime.utcnow().isoformat()
    
    # Generate alert ID
    alert_id = f"alert_{int(datetime.utcnow().timestamp() * 1000)}"
    
    # Store alert
    alert_data = {
        "id": alert_id,
        **alert.dict()
    }
    alert_store.append(alert_data)
    
    # Keep only last 50 alerts
    if len(alert_store) > 50:
        alert_store.pop(0)
    
    # Broadcast to all SSE subscribers
    broadcast_count = 0
    for queue in alert_subscribers:
        try:
            await queue.put(alert_data)
            broadcast_count += 1
        except:
            pass
    
    print(f"📢 Executive Alert broadcast to {broadcast_count} clients: {alert.title}")
    
    return AlertResponse(
        status="success",
        alertId=alert_id,
        broadcastCount=broadcast_count
    )


@router.get("/stream")
async def stream_alerts():
    """
    Server-Sent Events (SSE) endpoint for real-time alerts.
    Frontend connects here to receive push notifications.
    """
    from fastapi.responses import StreamingResponse
    
    queue = asyncio.Queue()
    alert_subscribers.append(queue)
    
    async def event_generator():
        try:
            # Send initial connection message
            yield f"data: {{'type': 'connected', 'message': 'Listening for executive alerts'}}\n\n"
            
            while True:
                # Wait for new alert
                alert = await queue.get()
                yield f"data: {alert}\n\n"
        except asyncio.CancelledError:
            pass
        finally:
            alert_subscribers.remove(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/recent")
async def get_recent_alerts(limit: int = 10):
    """Get recent alerts (for clients that missed SSE broadcasts)."""
    return alert_store[-limit:]


@router.get("/notifications")
async def get_notifications(limit: int = 10):
    """Get notifications in format expected by frontend hook."""
    return {"notifications": alert_store[-limit:]}


@router.post("/test")
async def trigger_test_alert():
    """Manual test endpoint - triggers a sample executive alert."""
    test_alert = ExecutiveAlert(
        alertType="success",
        title="Q4 Target Achieved",
        message="Revenue target of $2,500,000 exceeded by 1.9%",
        detail="Actual: $2,547,832 | Dynamic pricing contributed 23% uplift",
        priority="high"
    )
    return await receive_executive_alert(test_alert, x_alert_source="test")


# ============================================
# USAGE INSTRUCTIONS
# ============================================
#
# 1. Add to your FastAPI app:
#    from routers.notifications import router as notifications_router
#    app.include_router(notifications_router)
#
# 2. n8n will POST to: http://localhost:8000/api/notifications/executive-alert
#
# 3. Frontend connects to SSE: http://localhost:8000/api/notifications/stream
#
# 4. Test manually: POST http://localhost:8000/api/notifications/test
#
# ============================================

