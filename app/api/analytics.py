from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import SessionLocal
from app.services.analytics_service import (
    get_revenue_summary,
    get_revenue_by_day,
    get_revenue_by_order_status,
    get_revenue_by_status_per_day,
    get_payment_failure_rate,
    get_top_customers,
)

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/revenue")
def revenue_summary(
    start_date: datetime | None = (Query(None)),
    end_date: datetime | None = (Query(None)),
    db: Session = (Depends(get_db)),
):
    return get_revenue_summary(db, start_date, end_date)


@router.get("/revenue-by-day")
def revenue_by_day(
    start_date: datetime | None = (Query(None)),
    end_date: datetime | None = (Query(None)),
    db: Session = (Depends(get_db)),
):
    return get_revenue_by_day(db, start_date, end_date)


@router.get("/revenue-by-order-status")
def revenue_by_status(db: Session = Depends(get_db)):
    return get_revenue_by_order_status(db)


@router.get("/revenue-by-status-per-day")
def revenue_by_status_per_day(
    db: Session = Depends(get_db),
    start_date: datetime | None = (Query(None)),
    end_date: datetime | None = (Query(None)),
):
    return get_revenue_by_status_per_day(db, start_date, end_date)


@router.get("/payment-failure-rate")
def payment_failure_rate(db: Session = Depends(get_db)):
    return get_payment_failure_rate(db)


@router.get("/top-customers")
def top_customers(
    limit: int = Query(5, ge=1),
    db: Session = Depends(get_db),
):
    return get_top_customers(db, limit)
