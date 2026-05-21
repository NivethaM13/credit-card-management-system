from sqlalchemy.orm import Session
from app import models
from app import schemas
import uuid
import pandas as pd

from app.auth import hash_password


# ================= CREATE USER =================

def create_user(db: Session, user: schemas.UserCreate):

    hashed_password = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role="USER"
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


# ================= CREATE WALLET =================

def create_wallet(
    db: Session,
    wallet: schemas.WalletCreate
):

    new_wallet = models.Wallet(
        user_id=wallet.user_id,
        balance=0,
        wallet_status="ACTIVE",
        created_at="2026"
    )

    db.add(new_wallet)

    db.commit()

    db.refresh(new_wallet)

    return new_wallet


# ================= ADD MONEY =================

def add_money(
    db: Session,
    wallet_data: schemas.AddMoney
):

    wallet = db.query(models.Wallet).filter(
        models.Wallet.id == wallet_data.wallet_id
    ).first()

    if not wallet:

        return {
            "message": "Wallet Not Found"
        }

    wallet.balance += wallet_data.amount

    transaction = models.WalletTransaction(
        wallet_id=wallet.id,
        amount=wallet_data.amount,
        transaction_type="CREDIT",
        status="SUCCESS",
        created_at="2026"
    )

    db.add(transaction)

    db.commit()

    return {
        "message": "Money Added Successfully",
        "balance": wallet.balance
    }


# ================= CREATE RECEIPT =================

def create_receipt(
    db: Session,
    receipt: schemas.ReceiptCreate
):

    receipt_number = "RCPT-" + str(uuid.uuid4())[:8]

    new_receipt = models.Receipt(
        transaction_id=receipt.transaction_id,
        receipt_number=receipt_number,
        file_url="receipt.pdf",
        generated_at="2026"
    )

    db.add(new_receipt)

    db.commit()

    db.refresh(new_receipt)

    return new_receipt


# ================= CREATE REFUND =================

def create_refund(
    db: Session,
    refund: schemas.RefundCreate
):

    new_refund = models.Refund(
        transaction_id=refund.transaction_id,
        refund_amount=refund.refund_amount,
        refund_status="PENDING",
        reason=refund.reason,
        created_at="2026"
    )

    db.add(new_refund)

    db.commit()

    db.refresh(new_refund)

    return new_refund


# ================= CREATE SECURITY LOG =================

def create_security_log(
    db: Session,
    log: schemas.SecurityLogCreate
):

    new_log = models.SecurityLog(
        user_id=log.user_id,
        activity=log.activity,
        ip_address=log.ip_address,
        status=log.status,
        created_at="2026"
    )

    db.add(new_log)

    db.commit()

    db.refresh(new_log)

    return new_log


# ================= PAYMENT ANALYTICS =================

def get_payment_analytics(db: Session):

    total_transactions = db.query(
        models.Payment
    ).count()

    successful_payments = db.query(
        models.Payment
    ).filter(
        models.Payment.status == "SUCCESS"
    ).count()

    total_revenue = 0

    payments = db.query(models.Payment).all()

    for payment in payments:

        total_revenue += payment.amount

    return {
        "total_transactions": total_transactions,
        "successful_payments": successful_payments,
        "total_revenue": total_revenue
    }


# ================= CREATE NOTIFICATION =================

def create_notification(
    db: Session,
    notification: schemas.NotificationCreate
):

    new_notification = models.Notification(
        user_id=notification.user_id,
        title=notification.title,
        message=notification.message,
        is_read="NO",
        created_at="2026"
    )

    db.add(new_notification)

    db.commit()

    db.refresh(new_notification)

    return new_notification




def filter_transactions(
    db,
    status=None,
    min_amount=None,
    max_amount=None,
    start_date=None,
    end_date=None
):

    query = db.query(models.Transaction)

    if status:

        query = query.filter(
            models.Transaction.status == status
        )

    if min_amount:

        query = query.filter(
            models.Transaction.amount >= min_amount
        )

    if max_amount:

        query = query.filter(
            models.Transaction.amount <= max_amount
        )

    if start_date:

        query = query.filter(
            models.Transaction.created_at >= start_date
        )

    if end_date:

        query = query.filter(
            models.Transaction.created_at <= end_date
        )

    return query.all()
# ================= CREATE AUDIT LOG =================

def create_audit_log(
    db: Session,
    audit: schemas.AuditLogCreate
):

    new_audit = models.AuditLog(
        user_id=audit.user_id,
        action=audit.action,
        entity=audit.entity,
        created_at="2026"
    )

    db.add(new_audit)

    db.commit()

    db.refresh(new_audit)

    return new_audit

# ================= CREATE STATEMENT LOG =================

def create_statement_log(
    db: Session,
    statement: schemas.StatementLogCreate
):

    new_statement = models.StatementLog(
        user_id=statement.user_id,
        statement_type=statement.statement_type,
        generated_at="2026"
    )

    db.add(new_statement)

    db.commit()

    db.refresh(new_statement)

    return new_statement

# ================= EXPORT CSV =================

def export_transactions_csv(db: Session):

    payments = db.query(models.Payment).all()

    data = []

    for payment in payments:

        data.append({
            "ID": payment.id,
            "User ID": payment.user_id,
            "Card ID": payment.card_id,
            "Amount": payment.amount,
            "Status": payment.status,
            "Transaction ID": payment.transaction_id
        })

    df = pd.DataFrame(data)

    file_name = "transactions.csv"

    df.to_csv(file_name, index=False)

    return {
        "message": "CSV Exported Successfully",
        "file": file_name
    }


def create_statement_log(db, user_id, statement_type):

    statement = models.StatementLog(
        user_id=user_id,
        statement_type=statement_type
    )

    db.add(statement)
    db.commit()
    db.refresh(statement)

    return statement

def get_statement_logs(db):

    return db.query(models.StatementLog).all()


def track_failed_login(db, email):

    attempt = db.query(
        models.FailedLoginAttempt
    ).filter(
        models.FailedLoginAttempt.email == email
    ).first()

    if attempt:

        attempt.attempt_count += 1

        if attempt.attempt_count >= 3:

            attempt.is_blocked = "YES"

    else:

        attempt = models.FailedLoginAttempt(
            email=email,
            attempt_count=1
        )

        db.add(attempt)

    db.commit()

    db.refresh(attempt)

    return attempt


def mark_notification_as_read(
    db,
    notification_id
):

    notification = db.query(
        models.Notification
    ).filter(
        models.Notification.id == notification_id
    ).first()

    if not notification:

        return {
            "message": "Notification not found"
        }

    notification.is_read = True

    db.commit()

    db.refresh(notification)

    return notification


def search_transaction_by_id(
    db,
    transaction_id
):

    transaction = db.query(
        models.Transaction
    ).filter(
        models.Transaction.id == transaction_id
    ).first()

    if not transaction:

        return {
            "message": "Transaction not found"
        }

    return transaction

def reset_failed_attempts(
    db,
    email
):

    attempt = db.query(
        models.FailedLoginAttempt
    ).filter(
        models.FailedLoginAttempt.email == email
    ).first()

    if attempt:

        attempt.attempt_count = 0

        attempt.is_blocked = "NO"

        db.commit()