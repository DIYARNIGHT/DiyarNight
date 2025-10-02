from fastapi import APIRouter, HTTPException
from app.database.connection import addons_collection, users_collection
from app.models.schemas import Addon, AddonPurchaseRequest
from typing import List

router = APIRouter(prefix="/addons", tags=["addons"])

@router.get("/", response_model=List[Addon])
async def get_all_addons():
    """Get all available addon packages"""
    try:
        addons = await addons_collection.find({}).sort("price", 1).to_list(length=100)
        return addons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{addon_id}", response_model=Addon)
async def get_addon(addon_id: str):
    """Get specific addon details"""
    try:
        addon = await addons_collection.find_one({"addon_id": addon_id})
        if not addon:
            raise HTTPException(status_code=404, detail="Addon not found")
        return addon
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/purchase/{user_id}")
async def purchase_addon(user_id: str, request: AddonPurchaseRequest):
    """Purchase addon package for user"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify addon exists
        addon = await addons_collection.find_one({"addon_id": request.addon_id})
        if not addon:
            raise HTTPException(status_code=404, detail="Addon not found")
        
        # Mock addon purchase process
        # In real implementation, this would integrate with payment system
        purchase_data = {
            "user_id": user_id,
            "addon_id": request.addon_id,
            "addon_name": addon["name"],
            "extra_gb": addon["extra_gb"],
            "price": addon["price"],
            "purchase_date": "2025-10-02T10:00:00Z",
            "status": "completed"
        }
        
        return {
            "status": "success", 
            "message": f"{addon['name']} ek paketi başarıyla satın alındı.",
            "purchase": purchase_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations/{user_id}")
async def get_addon_recommendations(user_id: str, usage_percentage: float = 0):
    """Get addon recommendations based on user's usage"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        recommendations = []
        
        if usage_percentage > 90:
            # Critical - recommend immediate addon
            urgent_addons = await addons_collection.find({
                "extra_gb": {"$gte": 10, "$lte": 25}
            }).sort("price", 1).to_list(length=2)
            recommendations.extend(urgent_addons)
            
        elif usage_percentage > 75:
            # High usage - recommend medium addons
            medium_addons = await addons_collection.find({
                "extra_gb": {"$gte": 20, "$lte": 50}
            }).sort("extra_gb", 1).to_list(length=3)
            recommendations.extend(medium_addons)
            
        elif usage_percentage > 60:
            # Moderate usage - recommend small addons
            small_addons = await addons_collection.find({
                "extra_gb": {"$lte": 30}
            }).sort("price", 1).to_list(length=2)
            recommendations.extend(small_addons)
        
        return {
            "user_id": user_id,
            "usage_percentage": usage_percentage,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/filter/by-size")
async def filter_addons_by_size(min_gb: int = None, max_gb: int = None, max_price: float = None):
    """Filter addons by size and price"""
    try:
        query = {}
        
        if min_gb is not None or max_gb is not None:
            size_query = {}
            if min_gb is not None:
                size_query["$gte"] = min_gb
            if max_gb is not None:
                size_query["$lte"] = max_gb
            query["extra_gb"] = size_query
        
        if max_price is not None:
            query["price"] = {"$lte": max_price}
        
        addons = await addons_collection.find(query).sort("extra_gb", 1).to_list(length=50)
        return addons
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))