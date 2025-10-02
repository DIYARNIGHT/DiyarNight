from fastapi import APIRouter, HTTPException
from app.database.connection import addresses_collection, plans_collection
from app.models.schemas import CoverageResponse, Address
from typing import List, Optional, Optional

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("/{address_id}/coverage", response_model=CoverageResponse)
async def get_address_coverage(address_id: str):
    """Get coverage information for an address"""
    try:
        address = await addresses_collection.find_one({"address_id": address_id})
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        
        # Get recommended plans based on coverage
        max_speed = address["max_speed_mbps"]
        plans_cursor = plans_collection.find({"speed_mbps": {"$lte": max_speed}}).sort("speed_mbps", -1)
        recommended_plans = await plans_cursor.to_list(length=5)
        
        return CoverageResponse(
            address_id=address["address_id"],
            city=address["city"],
            district=address["district"],
            fiber_available=bool(address["fiber"]),
            vdsl_available=bool(address["vdsl"]),
            adsl_available=bool(address["adsl"]),
            max_speed_mbps=address["max_speed_mbps"],
            recommended_plans=recommended_plans
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Address])
async def get_all_addresses():
    """Get all addresses"""
    try:
        addresses = await addresses_collection.find({}).to_list(length=100)
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[Address])
async def search_addresses(city: Optional[str] = None, district: Optional[str] = None):
    """Search addresses by city and/or district"""
    try:
        query = {}
        if city:
            query["city"] = {"$regex": city, "$options": "i"}
        if district:
            query["district"] = {"$regex": district, "$options": "i"}
        
        addresses = await addresses_collection.find(query).to_list(length=50)
        return addresses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cities")
async def get_cities():
    """Get all available cities"""
    try:
        cities = await addresses_collection.distinct("city")
        return {"cities": cities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/districts/{city}")
async def get_districts_by_city(city: str):
    """Get all districts for a specific city"""
    try:
        districts = await addresses_collection.distinct("district", {"city": city})
        return {"districts": districts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))