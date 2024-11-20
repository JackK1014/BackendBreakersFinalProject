from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import customers as model


def create(db: Session, request):
    new_customer = model.Customer(
        name=request.name,
        email=request.email,
        phone_number=request.phone_number,
        address=request.address
    )

    try:
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        if "UNIQUE constraint failed" in error and "email" in error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be unique")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_customer


def read_all(db: Session):
    try:
        customers = db.query(model.Customer).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customers


def read_one(db: Session, customer_id: int):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer


def update(db: Session, customer_id: int, request):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        if "UNIQUE constraint failed" in error and "email" in error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must be unique")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return customer


def delete(db: Session, customer_id: int):
    try:
        customer = db.query(model.Customer).filter(model.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        db.delete(customer)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
