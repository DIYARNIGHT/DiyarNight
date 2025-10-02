from fastapi import APIRouter, HTTPException, Query
from app.database.connection import usage_collection, users_collection, plans_collection
from app.models.schemas import Usage
from typing import List, Optional
from datetime import datetime, timedelta
import calendar

router = APIRouter(prefix="/usage", tags=["usage"])

@router.get("/{user_id}/daily", response_model=List[Usage])
async def get_daily_usage(user_id: str, days: int = 30):
    """Get daily usage for user (last N days)"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        usage_data = await usage_collection.find(
            {"user_id": user_id}
        ).sort("date", -1).limit(days).to_list(length=days)
        
        return usage_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/monthly")
async def get_monthly_usage(user_id: str):
    """Get monthly usage summary for October 2025"""
    try:
        # Get all usage for the user
        usage_data = await usage_collection.find(
            {"user_id": user_id}
        ).to_list(length=365)
        
        # Filter for October 2025 and clean data
        october_data = []
        total_usage = 0
        
        for usage in usage_data:
            if usage.get("date", "").startswith("2025-10"):
                # Clean the data - remove ObjectId and convert to simple dict
                clean_usage = {
                    "user_id": usage.get("user_id"),
                    "date": usage.get("date"),
                    "used_gb": float(usage.get("used_gb", 0))
                }
                october_data.append(clean_usage)
                total_usage += clean_usage["used_gb"]
        
        return {
            "user_id": user_id,
            "month": "October 2025",
            "total_usage_gb": round(total_usage, 2),
            "days_count": len(october_data),
            "data": october_data
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "user_id": user_id
        }

@router.get("/{user_id}/statistics")
async def get_usage_statistics(user_id: str):
    """Get comprehensive usage statistics"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all usage data
        all_usage = await usage_collection.find(
            {"user_id": user_id}
        ).sort("date", 1).to_list(length=365)
        
        if not all_usage:
            raise HTTPException(status_code=404, detail="No usage data found")
        
        # Calculate statistics
        total_usage = sum(usage["used_gb"] for usage in all_usage)
        avg_daily = total_usage / len(all_usage)
        max_daily = max(usage["used_gb"] for usage in all_usage)
        min_daily = min(usage["used_gb"] for usage in all_usage)
        
        # Get recent trend (last 7 days vs previous 7 days)
        recent_7_days = all_usage[-7:] if len(all_usage) >= 7 else all_usage
        previous_7_days = all_usage[-14:-7] if len(all_usage) >= 14 else []
        
        recent_avg = sum(usage["used_gb"] for usage in recent_7_days) / len(recent_7_days) if recent_7_days else 0
        previous_avg = sum(usage["used_gb"] for usage in previous_7_days) / len(previous_7_days) if previous_7_days else 0
        
        trend = "increasing" if recent_avg > previous_avg else "decreasing" if recent_avg < previous_avg else "stable"
        trend_percentage = ((recent_avg - previous_avg) / previous_avg * 100) if previous_avg > 0 else 0
        
        return {
            "user_id": user_id,
            "total_usage_gb": round(total_usage, 2),
            "avg_daily_usage_gb": round(avg_daily, 2),
            "max_daily_usage_gb": round(max_daily, 2),
            "min_daily_usage_gb": round(min_daily, 2),
            "days_of_data": len(all_usage),
            "recent_trend": trend,
            "trend_percentage": round(trend_percentage, 2),
            "recent_7_days_avg": round(recent_avg, 2),
            "previous_7_days_avg": round(previous_avg, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/predictions")
async def get_usage_predictions(user_id: str):
    """Get usage predictions for current month"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get current month usage
        current_date = datetime.now()
        current_month_start = current_date.replace(day=1).date().isoformat()
        
        current_month_usage = await usage_collection.find({
            "user_id": user_id,
            "date": {"$gte": current_month_start}
        }).sort("date", 1).to_list(length=31)
        
        if not current_month_usage:
            raise HTTPException(status_code=404, detail="No current month usage data found")
        
        # Calculate predictions
        days_passed = len(current_month_usage)
        total_usage_so_far = sum(usage["used_gb"] for usage in current_month_usage)
        avg_daily_usage = total_usage_so_far / days_passed
        
        # Days remaining in month
        days_in_month = calendar.monthrange(current_date.year, current_date.month)[1]
        days_remaining = days_in_month - days_passed
        
        # Predicted total usage
        predicted_total = total_usage_so_far + (avg_daily_usage * days_remaining)
        
        # Get user's quota
        plan = await plans_collection.find_one({"plan_id": user["current_plan_id"]})
        quota_gb = plan["quota_gb"] if plan else 0
        
        predicted_percentage = (predicted_total / quota_gb * 100) if quota_gb > 0 else 0
        
        # Risk assessment
        risk_level = "low"
        if predicted_percentage > 100:
            risk_level = "high"
        elif predicted_percentage > 85:
            risk_level = "medium"
        
        return {
            "user_id": user_id,
            "current_month": f"{current_date.year}-{current_date.month:02d}",
            "days_passed": days_passed,
            "days_remaining": days_remaining,
            "usage_so_far_gb": round(total_usage_so_far, 2),
            "avg_daily_usage_gb": round(avg_daily_usage, 2),
            "predicted_total_gb": round(predicted_total, 2),
            "quota_gb": quota_gb,
            "predicted_percentage": round(predicted_percentage, 2),
            "risk_level": risk_level,
            "recommendations": [
                "Kullanımınızı azaltın" if risk_level == "high" else 
                "Kullanımınızı takip edin" if risk_level == "medium" else 
                "Normal kullanım devam edebilir"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/add-usage")
async def add_usage_record(user_id: str, date: str, used_gb: float):
    """Add new usage record (for testing/admin purposes)"""
    try:
        # Verify user exists
        user = await users_collection.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate date format
        try:
            datetime.fromisoformat(date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Check if record already exists
        existing = await usage_collection.find_one({"user_id": user_id, "date": date})
        if existing:
            # Update existing record
            await usage_collection.update_one(
                {"user_id": user_id, "date": date},
                {"$set": {"used_gb": used_gb}}
            )
            return {"status": "updated", "message": "Usage record updated"}
        else:
            # Insert new record
            usage_record = {
                "user_id": user_id,
                "date": date,
                "used_gb": used_gb
            }
            await usage_collection.insert_one(usage_record)
            return {"status": "created", "message": "Usage record created"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

