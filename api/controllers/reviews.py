from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from sqlalchemy.exc import SQLAlchemyError
from ..models import reviews as model


def create(db: Session, request):
    new_review = model.Review(
        customer_id=request.customer_id,
        sandwich_id=request.sandwich_id,
        review_text=request.review_text,
        score=request.score
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review


def read_all(db: Session):
    try:
        reviews = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return reviews


def read_one(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


def update(db: Session, review_id: int, request):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

        update_data = request.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(review, key, value)

        db.commit()
        db.refresh(review)
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return review


def delete(db: Session, review_id: int):
    try:
        review = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
        db.delete(review)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        error = str(e.__dict__.get('orig', e)) or str(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
