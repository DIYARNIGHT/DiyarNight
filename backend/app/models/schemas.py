from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class User(BaseModel):
    user_id: str
    name: str
    address_id: str
    current_plan_id: str
    modem_mac: str

class Address(BaseModel):
    address_id: str
    city: str
    district: str
    fiber: int
    vdsl: int
    adsl: int
    max_speed_mbps: int

class Plan(BaseModel):
    plan_id: str
    name: str
    quota_gb: int
    speed_mbps: int
    monthly_price: float

class Usage(BaseModel):
    user_id: str
    date: str
    used_gb: float

class Addon(BaseModel):
    addon_id: str
    name: str
    extra_gb: int
    price: float

class Ticket(BaseModel):
    ticket_id: str
    user_id: str
    created_at: str
    issue: str
    status: str

# Response Models
class UsageResponse(BaseModel):
    total_used_gb: float
    quota_gb: int
    usage_percentage: float
    daily_usage: List[Usage]
    recommendations: List[str]

class CoverageResponse(BaseModel):
    address_id: str
    city: str
    district: str
    fiber_available: bool
    vdsl_available: bool
    adsl_available: bool
    max_speed_mbps: int
    recommended_plans: List[Plan]

class DashboardResponse(BaseModel):
    user: User
    current_plan: Plan
    usage_info: UsageResponse
    address_info: Address
    recommendations: List[str]

class PlanChangeRequest(BaseModel):
    new_plan_id: str

class AddonPurchaseRequest(BaseModel):
    addon_id: str

class TicketCreateRequest(BaseModel):
    issue: str
    description: Optional[str] = ""

class ModemResetResponse(BaseModel):
    status: str
    message: str

class TicketCreateResponse(BaseModel):
    ticket_id: str
    status: str
    message: str

class SpeedTestResponse(BaseModel):
    download_speed: float
    upload_speed: float
    ping: float
    timestamp: str