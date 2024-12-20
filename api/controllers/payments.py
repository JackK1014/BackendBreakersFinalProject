from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import payments as model
from ..models.orders import Order
from sqlalchemy.sql import func


def create(db: Session, request):
    new_payment = model.Payment(
        order_id=request.order_id,
        card_information=request.card_information,
        transaction_status=request.transaction_status,
        payment_type=request.payment_type
    )

    try:
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_payment


def read_all(db: Session):
    try:
        payments = db.query(model.Payment).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payments


def read_one(db: Session, payment_id: int):
    try:
        payment = db.query(model.Payment).filter(
            model.Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payment


def update(db: Session, payment_id: int, request):
    try:
        payment = db.query(model.Payment).filter(
            model.Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)

        db.commit()
        db.refresh(payment)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return payment


def delete(db: Session, payment_id: int):
    try:
        payment = db.query(model.Payment).filter(
            model.Payment.id == payment_id).first()
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
        db.delete(payment)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def get_total_payments(db: Session) -> float:
    """
    Calculate the sum of all payments.
    """
    total = db.query(func.sum(model.Payment.amount)).scalar()
    return total if total else 0.0
