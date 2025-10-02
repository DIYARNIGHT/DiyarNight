from fastapi import APIRouter, HTTPException
from app.database.connection import tickets_collection, users_collection
from app.models.schemas import ModemResetResponse, TicketCreateRequest, TicketCreateResponse, Ticket
from typing import List
import random
from datetime import datetime

router = APIRouter(prefix="/support", tags=["support"])

@router.post("/reset-modem", response_model=ModemResetResponse)
async def reset_modem(request: dict):
    """Reset user's modem"""
    try:
        user_id = request.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Mock modem reset process
        return ModemResetResponse(
            status="ok",
            message="Modem reset komutu gönderildi. 2-3 dakika içinde modem yeniden başlayacak."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tickets", response_model=TicketCreateResponse)
async def create_support_ticket(request: dict):
    """Create support ticket"""
    try:
        user_id = request.get("user_id")
        subject = request.get("subject", "Genel Destek")
        description = request.get("description", "")
        priority = request.get("priority", "medium")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id is required")
        
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate ticket ID
        ticket_id = f"T-{random.randint(10000, 99999)}"
        
        # Create ticket
        ticket_data = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "subject": subject,
            "description": description,
            "priority": priority,
            "status": "open",
            "created_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        await tickets_collection.insert_one(ticket_data)
        
        return TicketCreateResponse(
            ticket_id=ticket_id,
            status="created",
            message=f"Destek talebiniz oluşturuldu. Ticket ID: {ticket_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
        await tickets_collection.insert_one(ticket_data)
        
        return TicketCreateResponse(
            ticket_id=ticket_id,
            status="created",
            message=f"Destek talebi oluşturuldu. Takip numarası: {ticket_id}"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tickets/{user_id}", response_model=List[Ticket])
async def get_user_tickets(user_id: str):
    """Get all tickets for a user"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        tickets = await tickets_collection.find(
            {"user_id": user_id}
        ).sort("created_at", -1).to_list(length=50)
        
        return tickets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ticket/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: str):
    """Get specific ticket details"""
    try:
        ticket = await tickets_collection.find_one({"ticket_id": ticket_id})
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/ticket/{ticket_id}/status")
async def update_ticket_status(ticket_id: str, new_status: str):
    """Update ticket status"""
    try:
        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if new_status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        result = await tickets_collection.update_one(
            {"ticket_id": ticket_id},
            {"$set": {"status": new_status, "updated_at": datetime.now().isoformat()}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Ticket not found")
        
        return {"status": "success", "message": f"Ticket status updated to {new_status}"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tickets/status/{status}")
async def get_tickets_by_status(status: str):
    """Get all tickets with specific status"""
    try:
        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
        
        tickets = await tickets_collection.find(
            {"status": status}
        ).sort("created_at", -1).to_list(length=100)
        
        return tickets
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_support_statistics():
    """Get support statistics"""
    try:
        # Count tickets by status
        open_count = await tickets_collection.count_documents({"status": "open"})
        in_progress_count = await tickets_collection.count_documents({"status": "in_progress"})
        resolved_count = await tickets_collection.count_documents({"status": "resolved"})
        closed_count = await tickets_collection.count_documents({"status": "closed"})
        
        # Get recent tickets (last 7 days)
        from datetime import datetime, timedelta
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        recent_tickets = await tickets_collection.count_documents({
            "created_at": {"$gte": week_ago}
        })
        
        return {
            "total_tickets": open_count + in_progress_count + resolved_count + closed_count,
            "open_tickets": open_count,
            "in_progress_tickets": in_progress_count,
            "resolved_tickets": resolved_count,
            "closed_tickets": closed_count,
            "recent_tickets_7_days": recent_tickets
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))