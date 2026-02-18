from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime
from app.models.order import Order
from app.models.payment import Payment
from app.models.customer import Customer


def get_revenue_summary(
    db: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    query = db.query(
        func.sum(Payment.amount).label("total_revenue"),
        func.count(Order.id).label("orders_count"),
    ).join(Order, Payment.order_id == Order.id)

    if start_date:
        query = query.filter(Order.created_at >= start_date)

    if end_date:
        query = query.filter(Order.created_at <= end_date)

    result = query.first()

    return {
        "total_revenue": float(result.total_revenue or 0),
        "orders_count": result.orders_count or 0,
    }


def get_revenue_by_day(
    db: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    query = db.query(
        func.date(Order.created_at).label("date"),
        func.sum(Payment.amount).label("revenue"),
    ).join(Order, Payment.order_id == Order.id)

    if start_date:
        query = query.filter(Order.created_at >= start_date)

    if end_date:
        query = query.filter(Order.created_at <= end_date)

    query = query.group_by(func.date(Order.created_at)).order_by(
        func.date(Order.created_at)
    )

    results = query.all()

    return [
        {"date": str(row.date), "revenue": float(row.revenue or 0)}
        for row in results
    ]


def get_revenue_by_order_status(
    db: Session,
):
    query = (
        db.query(
            Order.status.label("status"),
            func.sum(Payment.amount).label("revenue"),
            func.count(Order.id).label("orders_count"),
        )
        .join(Payment, Payment.order_id == Order.id)
        .group_by(Order.status)
        .order_by(func.sum(Payment.amount).desc())
    )

    results = query.all()

    return [
        {
            "status": row.status,
            "revenue": round(row.revenue, 2),
            "orders_count": row.orders_count,
        }
        for row in results
    ]


def get_revenue_by_status_per_day(
    db: Session,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    query = db.query(
        func.date(Order.created_at).label("date"),
        Order.status.label("status"),
        func.sum(Payment.amount).label("revenue"),
        func.count(Order.id).label("orders_count"),
    ).join(Payment, Payment.order_id == Order.id)

    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    query = query.group_by(func.date(Order.created_at), Order.status)

    results = query.all()

    return [
        {
            "date": str(row.date),
            "status": row.status,
            "revenue": float(row.revenue or 0),
            "orders_count": row.orders_count,
        }
        for row in results
    ]


def get_payment_failure_rate(db: Session):
    total_payments = db.query(func.count(Payment.id)).scalar()
    failed_payments = (
        db.query(func.count(Payment.id))
        .filter(Payment.status == "failed")
        .scalar()
    )
    total_payments = total_payments or 0
    failed_payments = failed_payments or 0

    failure_rate = (
        (failed_payments / total_payments) * 100 if total_payments > 0 else 0
    )

    return {
        "total_payments": total_payments,
        "failed_payments": failed_payments,
        "failure_rate": round(failure_rate, 2),
    }


def get_top_customers(db: Session, limit: int = 5):
    query = (
        db.query(
            Customer.id.label("customer_id"),
            Customer.name.label("name"),
            func.sum(Payment.amount).label("total_spent"),
            func.count(Order.id).label("orders_count"),
        )
        .join(Order, Order.customer_id == Customer.id)
        .join(Payment, Payment.order_id == Order.id)
        .group_by(Customer.id, Customer.name)
        .order_by(desc("total_spent"))
        .limit(limit)
    )

    results = query.all()
    return [
        {
            "customer_id": row.customer_id,
            "name": row.name,
            "total_spent": float(row.total_spent or 0),
            "orders_count": row.orders_count,
        }
        for row in results
    ]
