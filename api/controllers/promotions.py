from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from ..models import promotions as model


def create(db: Session, request):
    new_promotion = model.Promotion(
        promotion_code=request.promotion_code,
        expiration_date=request.expiration_date
    )

    try:
        db.add(new_promotion)
        db.commit()
        db.refresh(new_promotion)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        if "UNIQUE constraint failed" in error and "promotion_code" in error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code must be unique")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_promotion


def read_all(db: Session):
    try:
        promotions = db.query(model.Promotion).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotions


def read_one(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion


def update(db: Session, promotion_id: int, request):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(promotion, key, value)

        db.commit()
        db.refresh(promotion)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        if "UNIQUE constraint failed" in error and "promotion_code" in error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Promotion code must be unique")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return promotion


def delete(db: Session, promotion_id: int):
    try:
        promotion = db.query(model.Promotion).filter(model.Promotion.id == promotion_id).first()
        if not promotion:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion not found")
        db.delete(promotion)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
