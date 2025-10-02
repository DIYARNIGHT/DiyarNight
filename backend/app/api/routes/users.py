from fastapi import APIRouter, HTTPException
from app.database.connection import (
    users_collection, plans_collection, usage_collection, addresses_collection
)
from app.models.schemas import *
from typing import List
import random
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get user information"""
    try:
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/usage", response_model=UsageResponse)
async def get_user_usage(user_id: str):
    """Get user's quota usage information"""
    try:
        # Get user info
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current plan
        plan = await plans_collection.find_one({"plan_id": user["current_plan_id"]})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Get usage data
        usage_cursor = usage_collection.find({"user_id": user_id}).sort("date", -1)
        usage_data = await usage_cursor.to_list(length=30)  # Last 30 days
        
        # Calculate total usage
        total_used_gb = sum(usage["used_gb"] for usage in usage_data)
        quota_gb = plan["quota_gb"]
        usage_percentage = (total_used_gb / quota_gb) * 100
        
        # Generate recommendations
        recommendations = []
        if usage_percentage > 80:
            recommendations.append("Kotanız %80'in üzerinde! Ek kota paketlerimizi inceleyin.")
        
        if usage_percentage > 95:
            recommendations.append("Kotanız bitmek üzere! Hemen ek kota alın.")
            
        return UsageResponse(
            total_used_gb=total_used_gb,
            quota_gb=quota_gb,
            usage_percentage=usage_percentage,
            daily_usage=usage_data,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/dashboard", response_model=DashboardResponse)
async def get_user_dashboard(user_id: str):
    """Get complete dashboard information for user"""
    try:
        # Get user info
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current plan
        plan = await plans_collection.find_one({"plan_id": user["current_plan_id"]})
        
        # Get address info
        address = await addresses_collection.find_one({"address_id": user["address_id"]})
        
        # Get usage info
        usage_response = await get_user_usage(user_id)
        
        # Generate general recommendations
        recommendations = []
        if usage_response.usage_percentage < 50:
            recommendations.append("Düşük kullanım oranınız var. Daha ekonomik paketleri inceleyin.")
        
        # Check if user can upgrade
        if address and plan:
            higher_plans_cursor = plans_collection.find({
                "speed_mbps": {"$gt": plan["speed_mbps"], "$lte": address["max_speed_mbps"]}
            }).sort("speed_mbps", 1)
            higher_plans = await higher_plans_cursor.to_list(length=3)
            
            if higher_plans:
                recommendations.append(f"Daha hızlı internet için {higher_plans[0]['name']} paketini inceleyin.")
        
        return DashboardResponse(
            user=user,
            current_plan=plan,
            usage_info=usage_response,
            address_info=address,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/change-plan")
async def change_user_plan(user_id: str, request: PlanChangeRequest):
    """Change user's plan"""
    try:
        # Verify plan exists
        plan = await plans_collection.find_one({"plan_id": request.new_plan_id})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Update user's plan
        result = await users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"current_plan_id": request.new_plan_id}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"status": "success", "message": f"Plan başarıyla {plan['name']} olarak değiştirildi."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/speed-test", response_model=SpeedTestResponse)
async def mock_speed_test(user_id: str):
    """Mock speed test"""
    try:
        # Get user's plan for realistic speed simulation
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        plan = await plans_collection.find_one({"plan_id": user["current_plan_id"]})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        
        # Simulate realistic speeds (85-95% of plan speed)
        max_speed = plan["speed_mbps"]
        download_speed = round(max_speed * random.uniform(0.85, 0.95), 2)
        upload_speed = round(download_speed * random.uniform(0.1, 0.2), 2)  # Upload is typically 10-20% of download
        ping = round(random.uniform(8, 25), 1)
        
        return SpeedTestResponse(
            download_speed=download_speed,
            upload_speed=upload_speed,
            ping=ping,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))