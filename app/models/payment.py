from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from app.core.database import Base
from datetime import datetime


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)
    paid_at = Column(DateTime, default=datetime.utcnow)
