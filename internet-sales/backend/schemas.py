"""Pydantic Schemas for API validation"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# ═══════════════════════════════════════════════════
# LEAD SCHEMAS
# ═══════════════════════════════════════════════════

class LeadCreate(BaseModel):
    source: str
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    interested_vehicle: Optional[str] = None
    stock_number: Optional[str] = None
    message: Optional[str] = None

class LeadResponse(BaseModel):
    id: int
    source: str
    customer_name: str
    customer_email: str
    customer_phone: Optional[str]
    interested_vehicle: Optional[str]
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ═══════════════════════════════════════════════════
# QUOTE SCHEMAS
# ═══════════════════════════════════════════════════

class QuoteRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    stock_number: str
    down_payment: float = 0
    trade_vin: Optional[str] = None
    trade_mileage: Optional[int] = None
    trade_condition: Optional[str] = "good"

class QuoteResponse(BaseModel):
    id: int
    lead_id: int
    stock_number: str
    vehicle_description: str
    selling_price: float
    trade_value: float
    down_payment: float
    amount_financed: float
    payment_options: List[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True

# ═══════════════════════════════════════════════════
# PAYMENT CALCULATOR
# ═══════════════════════════════════════════════════

class PaymentCalculation(BaseModel):
    amount_financed: float
    term_months: int
    apr: float

# ═══════════════════════════════════════════════════
# TRADE-IN
# ═══════════════════════════════════════════════════

class TradeInRequest(BaseModel):
    vin: str
    mileage: int
    condition: str = "good"
    photos: List[str] = []

# ═══════════════════════════════════════════════════
# APPOINTMENT
# ═══════════════════════════════════════════════════

class AppointmentCreate(BaseModel):
    lead_id: int
    appointment_type: str
    scheduled_time: datetime
    salesperson_id: Optional[int] = None
    notes: Optional[str] = None

# ═══════════════════════════════════════════════════
# CHAT
# ═══════════════════════════════════════════════════

class ChatMessage(BaseModel):
    lead_id: int
    message: str

# ═══════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
