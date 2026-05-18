from sqlalchemy import Column, Integer, String, Float
from app.database import Base


# ================= USERS TABLE =================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))

    email = Column(String(100), unique=True)

    password = Column(String(200))


# ================= CARDS TABLE =================

class Card(Base):

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    card_holder = Column(String(100))

    card_number = Column(String(20))

    expiry = Column(String(10))

    balance = Column(Float, default=50000)


# ================= PAYMENTS TABLE =================

class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    card_id = Column(Integer)

    amount = Column(Float)

    status = Column(String(50))

    transaction_id = Column(String(100))


# ================= TRANSACTIONS TABLE =================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    card_id = Column(Integer)

    amount = Column(Float)

    status = Column(String(100))