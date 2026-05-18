from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, schemas, crud

from app.database import engine, Base, get_db
from app.auth import verify_password,create_access_token

app = FastAPI()



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




@app.post("/register")
def register(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    return crud.create_user(db, user)




@app.post("/login")
@app.post("/login")
def login(user: schemas.LoginSchema, db: Session = Depends(get_db)):

    db_user = crud.login_user(db, user.email)

    if not db_user:
        return {
            "message": "User not found"
        }

    if not verify_password(user.password, db_user.password):
        return {
            "message": "Invalid password"
        }

    token = create_access_token(
        data={"sub": db_user.email}
    )

    return {
        "message": "Login Successful",
        "access_token": token
    }


@app.post("/add-card")
def add_card(
    card: schemas.CardCreate,
    db: Session = Depends(get_db)
):

    return crud.create_card(db, card)




@app.post("/make-payment")
def make_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):

    return crud.create_payment(
        db,
        payment
    )


@app.get("/payment-history")
def payment_history(
    db: Session = Depends(get_db)
):

    return crud.get_payments(db)


@app.get("/cards")
def view_cards(db: Session = Depends(get_db)):

    return crud.get_cards(db)

@app.get("/transactions")
def view_transactions(
    db: Session = Depends(get_db)
):

    return crud.get_transactions(db)



@app.delete("/delete-card/{card_id}")
def remove_card(
    card_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_card(db, card_id)