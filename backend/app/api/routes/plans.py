from fastapi import APIRouter, HTTPException, Query
from app.database.connection import plans_collection, users_collection
from app.models.schemas import Plan
from typing import List, Optional

router = APIRouter(prefix="/plans", tags=["plans"])

@router.get("/", response_model=List[Plan])
async def get_all_plans():
    """Get all available plans"""
    try:
        plans = await plans_collection.find({}).sort("speed_mbps", 1).to_list(length=100)
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{plan_id}", response_model=Plan)
async def get_plan(plan_id: str):
    """Get specific plan details"""
    try:
        plan = await plans_collection.find_one({"plan_id": plan_id})
        if not plan:
            raise HTTPException(status_code=404, detail="Plan not found")
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/speed/{max_speed}")
async def get_plans_by_speed(max_speed: int):
    """Get plans available for specific maximum speed"""
    try:
        plans = await plans_collection.find({
            "speed_mbps": {"$lte": max_speed}
        }).sort("speed_mbps", -1).to_list(length=50)
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-criteria")
async def filter_plans(
    min_speed: Optional[int] = None,
    max_speed: Optional[int] = None,
    min_quota: Optional[int] = None,
    max_quota: Optional[int] = None,
    max_price: Optional[float] = None
):
    """Filter plans by various criteria"""
    try:
        query = {}
        
        if min_speed is not None or max_speed is not None:
            speed_query = {}
            if min_speed is not None:
                speed_query["$gte"] = min_speed
            if max_speed is not None:
                speed_query["$lte"] = max_speed
            query["speed_mbps"] = speed_query
        
        if min_quota is not None or max_quota is not None:
            quota_query = {}
            if min_quota is not None:
                quota_query["$gte"] = min_quota
            if max_quota is not None:
                quota_query["$lte"] = max_quota
            query["quota_gb"] = quota_query
        
        if max_price is not None:
            query["monthly_price"] = {"$lte": max_price}
        
        plans = await plans_collection.find(query).sort("speed_mbps", 1).to_list(length=50)
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{user_id}")
async def get_plan_recommendations(user_id: str):
    """Get plan recommendations for user"""
    try:
        # Get user
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current plan
        current_plan = await plans_collection.find_one({"plan_id": user["current_plan_id"]})
        if not current_plan:
            raise HTTPException(status_code=404, detail="Current plan not found")
        
        # Get all other plans
        all_plans = await plans_collection.find({
            "plan_id": {"$ne": user["current_plan_id"]}
        }).to_list(length=20)
        
        # Clean and prepare recommendations
        recommendations = []
        for plan in all_plans[:3]:  # Take first 3
            clean_plan = {
                "plan_id": plan["plan_id"],
                "name": plan["name"],
                "quota_gb": plan["quota_gb"],
                "speed_mbps": plan["speed_mbps"],
                "monthly_price": plan["monthly_price"]
            }
            recommendations.append(clean_plan)
        
        return {
            "user_id": user_id,
            "current_plan": {
                "plan_id": current_plan["plan_id"],
                "name": current_plan["name"],
                "quota_gb": current_plan["quota_gb"],
                "speed_mbps": current_plan["speed_mbps"],
                "monthly_price": current_plan["monthly_price"]
            },
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")