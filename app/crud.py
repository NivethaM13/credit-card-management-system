from sqlalchemy.orm import Session
from app import models
from app import schemas
import uuid

from app.auth import hash_password


# ================= CREATE USER =================

def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ================= LOGIN USER =================

def login_user(db: Session, email: str):

    return db.query(models.User).filter(
        models.User.email == email
    ).first()


# ================= CREATE CARD =================

def create_card(db: Session, card: schemas.CardCreate):

    masked_number = "XXXX-XXXX-XXXX-" + card.card_number[-4:]

    new_card = models.Card(
        user_id=card.user_id,
        card_holder=card.card_holder,
        card_number=masked_number,
        expiry=card.expiry,
        balance=50000
    )

    db.add(new_card)

    db.commit()

    db.refresh(new_card)

    return new_card


# ================= GET CARDS =================

def get_cards(db: Session):

    return db.query(models.Card).all()


# ================= DELETE CARD =================

def delete_card(db: Session, card_id: int):

    card = db.query(models.Card).filter(
        models.Card.id == card_id
    ).first()

    if card:

        db.delete(card)

        db.commit()

        return {
            "message": "Card Deleted"
        }

    return {
        "message": "Card Not Found"
    }


# ================= CREATE PAYMENT =================

def create_payment(
    db: Session,
    payment: schemas.PaymentCreate
):

    card = db.query(models.Card).filter(
        models.Card.id == payment.card_id
    ).first()

    if not card:

        return {
            "message": "Card Not Found"
        }

    if card.balance < payment.amount:

        return {
            "message": "Insufficient Balance"
        }

    card.balance -= payment.amount

    transaction = str(uuid.uuid4())

    new_payment = models.Payment(
        user_id=payment.user_id,
        card_id=payment.card_id,
        amount=payment.amount,
        status="SUCCESS",
        transaction_id=transaction
    )

    db.add(new_payment)

    db.commit()

    db.refresh(new_payment)

    return {
        "message": "Payment Successful",
        "remaining_balance": card.balance,
        "payment": new_payment
    }


# ================= PAYMENT HISTORY =================

def get_payments(db: Session):

    return db.query(models.Payment).all()


# ================= GET TRANSACTIONS =================

def get_transactions(db: Session):

    return db.query(models.Payment).all()


# ================= DELETE TRANSACTION =================

def delete_transaction(db: Session, transaction_id: int):

    transaction = db.query(models.Payment).filter(
        models.Payment.id == transaction_id
    ).first()

    if transaction:

        db.delete(transaction)

        db.commit()

        return {
            "message": "Transaction Deleted"
        }
    

    return {
        "message": "Transaction Not Found"
    }