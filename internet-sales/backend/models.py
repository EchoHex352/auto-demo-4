"""Database Models for Internet Sales Platform"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ═══════════════════════════════════════════════════
# LEADS
# ═══════════════════════════════════════════════════

class Lead(Base):
    """Customer leads from website/phone/email"""
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Source tracking
    source = Column(String(50), index=True)  # website, email, phone, chat, referral
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Customer information
    customer_name = Column(String(255))
    customer_email = Column(String(255), index=True)
    customer_phone = Column(String(20))
    
    # Interest information
    interested_vehicle = Column(String(255))  # "2024 Honda Accord Sport"
    stock_number = Column(String(50))
    message = Column(Text)  # Customer's inquiry message
    
    # Status tracking
    status = Column(String(50), default="new", index=True)  # new, contacted, quoted, appointment_set, sold, lost
    last_contact = Column(DateTime)
    assigned_to = Column(String(100))  # Salesperson name
    
    # Relationships
    quotes = relationship("Quote", back_populates="lead")
    conversations = relationship("Conversation", back_populates="lead")
    appointments = relationship("Appointment", back_populates="lead")
    trade_ins = relationship("TradeIn", back_populates="lead")


# ═══════════════════════════════════════════════════
# QUOTES
# ═══════════════════════════════════════════════════

class Quote(Base):
    """Vehicle price quotes sent to customers"""
    __tablename__ = "quotes"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    # Vehicle details
    stock_number = Column(String(50))
    vin = Column(String(17))
    vehicle_description = Column(String(255))  # "2024 Honda Accord Sport"
    
    # Pricing
    selling_price = Column(Float)
    trade_value = Column(Float, default=0)
    down_payment = Column(Float, default=0)
    amount_financed = Column(Float)
    
    # Payment options (stored as JSON)
    payment_options = Column(JSON)  # Array of payment calculations
    
    # Tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    viewed_at = Column(DateTime)  # When customer opened email
    quote_pdf_url = Column(String(500))  # URL to PDF quote
    
    status = Column(String(50), default="draft")  # draft, sent, viewed, expired, accepted
    expires_at = Column(DateTime)
    
    # Relationships
    lead = relationship("Lead", back_populates="quotes")


# ═══════════════════════════════════════════════════
# TRADE-INS
# ═══════════════════════════════════════════════════

class TradeIn(Base):
    """Customer trade-in vehicles"""
    __tablename__ = "trade_ins"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    # Vehicle information
    vin = Column(String(17))
    year = Column(Integer)
    make = Column(String(100))
    model = Column(String(100))
    trim = Column(String(100))
    mileage = Column(Integer)
    
    # Condition
    condition = Column(String(50))  # excellent, good, fair, poor
    exterior_condition = Column(String(50))
    interior_condition = Column(String(50))
    mechanical_condition = Column(String(50))
    
    # Valuation
    estimated_value = Column(Float)
    kbb_value = Column(Float)
    nada_value = Column(Float)
    actual_offer = Column(Float)
    
    # Photos
    photos = Column(JSON)  # Array of photo URLs
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="trade_ins")


# ═══════════════════════════════════════════════════
# CONVERSATIONS
# ═══════════════════════════════════════════════════

class Conversation(Base):
    """Chat/email conversation history"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    message = Column(Text)
    sender = Column(String(50))  # customer, ai, human (salesperson)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Message metadata
    channel = Column(String(50))  # chat, email, sms
    read = Column(Boolean, default=False)
    
    # Relationships
    lead = relationship("Lead", back_populates="conversations")


# ═══════════════════════════════════════════════════
# APPOINTMENTS
# ═══════════════════════════════════════════════════

class Appointment(Base):
    """Test drives and delivery appointments"""
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    appointment_type = Column(String(50))  # test_drive, delivery, trade_appraisal
    scheduled_time = Column(DateTime, index=True)
    
    # Assignment
    salesperson_id = Column(Integer)
    salesperson_name = Column(String(255))
    
    # Status
    status = Column(String(50), default="scheduled")  # scheduled, confirmed, completed, no_show, cancelled
    
    # Notes
    notes = Column(Text)
    customer_notes = Column(Text)
    
    # Confirmation tracking
    confirmation_sent = Column(Boolean, default=False)
    reminder_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    lead = relationship("Lead", back_populates="appointments")


# ═══════════════════════════════════════════════════
# ACTIVITY LOG
# ═══════════════════════════════════════════════════

class Activity(Base):
    """Activity tracking for analytics"""
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    
    action = Column(String(100), index=True)  # lead_created, quoted, email_sent, etc.
    description = Column(Text)
    metadata = Column(JSON)
    
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


# ═══════════════════════════════════════════════════
# USERS (for admin access)
# ═══════════════════════════════════════════════════

class User(Base):
    """System users (managers, salespeople)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # admin, manager, salesperson
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
