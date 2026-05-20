from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
import csv

import csv
from reportlab.pdfgen import canvas

from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas, crud

from app.database import engine, Base, get_db
from app.auth import (
    verify_password,
    create_access_token,
    admin_only
)


# ================= FASTAPI APP =================

app = FastAPI()


# ================= CORS =================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================= CREATE TABLES =================

Base.metadata.create_all(bind=engine)


# ================= HOME =================

@app.get("/")
def home():

    return {
        "message": "Credit Card Management System Running"
    }


# ================= REGISTER =================

@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)


# ================= LOGIN =================

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = crud.login_user(
        db,
        form_data.username
    )

    if not db_user:

        return {
            "message": "User not found"
        }

    if not verify_password(
        form_data.password,
        db_user.password
    ):

        return {
            "message": "Invalid password"
        }

    token = create_access_token(
        data={
            "sub": db_user.email,
            "role":db_user.role

        }
    )

    return {
        "message": "Login Successful",
        "access_token": token,
        "role": db_user.role
    }


# ================= ADD CARD =================

@app.post("/add-card")
def add_card(
    card: schemas.CardCreate,
    db: Session = Depends(get_db)
):

    return crud.create_card(
        db,
        card
    )


# ================= VIEW CARDS =================

@app.get("/cards")
def view_cards(
    db: Session = Depends(get_db)
):

    return crud.get_cards(db)


# ================= DELETE CARD =================

@app.delete("/delete-card/{card_id}")
def remove_card(
    card_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_card(
        db,
        card_id
    )


# ================= MAKE PAYMENT =================

@app.post("/make-payment")
def make_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):

    return crud.create_payment(
        db,
        payment
    )


# ================= PAYMENT HISTORY =================

@app.get("/payment-history")
def payment_history(
    db: Session = Depends(get_db)
):

    return crud.get_payments(db)


# ================= TRANSACTIONS =================

@app.get("/transactions")
def view_transactions(
    db: Session = Depends(get_db)
):

    return crud.get_transactions(db)


# ================= DELETE TRANSACTION =================

@app.delete("/delete-transaction/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_transaction(
        db,
        transaction_id
    )


# ================= CREATE WALLET =================

@app.post("/create-wallet")
def create_wallet(
    wallet: schemas.WalletCreate,
    db: Session = Depends(get_db)
):

    return crud.create_wallet(
        db,
        wallet
    )


# ================= ADD MONEY =================

@app.post("/add-money")
def add_money(
    wallet_data: schemas.AddMoney,
    db: Session = Depends(get_db)
):

    return crud.add_money(
        db,
        wallet_data
    )


# ================= CREATE RECEIPT =================

@app.post("/create-receipt")
def create_receipt(
    receipt: schemas.ReceiptCreate,
    db: Session = Depends(get_db)
):

    return crud.create_receipt(
        db,
        receipt
    )


# ================= CREATE REFUND =================

@app.post("/create-refund")
def create_refund(
    refund: schemas.RefundCreate,
    db: Session = Depends(get_db)
):

    return crud.create_refund(
        db,
        refund
    )


# ================= SECURITY LOG =================

@app.post("/create-security-log")
def create_security_log(
    log: schemas.SecurityLogCreate,
    db: Session = Depends(get_db)
):

    return crud.create_security_log(
        db,
        log
    )


# ================= PAYMENT ANALYTICS =================

@app.get("/payment-analytics")
def payment_analytics(
    db: Session = Depends(get_db),
    admin: str = Depends(admin_only)
):

    return crud.get_payment_analytics(db)


# ================= CREATE NOTIFICATION =================

@app.post("/create-notification")
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):

    return crud.create_notification(
        db,
        notification
    )


# ================= FILTER TRANSACTIONS =================


@app.get("/filter-transactions")
def filter_transactions(
    status: str = None,
    min_amount: float = None,
    max_amount: float = None,
    db: Session = Depends(get_db)
):

    return crud.filter_transactions(
        db,
        status,
        min_amount,
        max_amount
    )

# ================= CREATE AUDIT LOG =================

@app.post("/create-audit-log")
def create_audit_log(
    audit: schemas.AuditLogCreate,
    db: Session = Depends(get_db)
):

    return crud.create_audit_log(
        db,
        audit
    )


# ================= CREATE STATEMENT LOG =================

@app.post("/create-statement-log")
def create_statement_log(
    statement: schemas.StatementLogCreate,
    db: Session = Depends(get_db)
):

    return crud.create_statement_log(
        db=db,
        user_id=statement.user_id,
        statement_type=statement.statement_type
    )


# ================= GET STATEMENT LOGS =================

@app.get("/statement-logs")
def get_statement_logs(
    db: Session = Depends(get_db)
):

    return crud.get_statement_logs(db)


# ================= DOWNLOAD CSV STATEMENT =================

@app.get("/download-statement-csv")
def download_statement_csv(
    db: Session = Depends(get_db)
):

    transactions = crud.get_transactions(db)

    crud.create_statement_log(
        db=db,
        user_id=1,
        statement_type="CSV"
    )

    filename = "statement.csv"

    with open(filename, mode="w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Transaction ID",
            "Amount",
            "Status"
        ])

        for transaction in transactions:

            writer.writerow([
                transaction.id,
                transaction.amount,
                transaction.status
            ])

    return FileResponse(
        path=filename,
        filename=filename,
        media_type='text/csv'
    )