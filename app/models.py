from sqlalchemy import Column, Integer, String, Float
from app.database import Base
from datetime import datetime


# ================= USERS TABLE =================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))

    email = Column(String(100), unique=True)

    password = Column(String(200))

    role = Column(String(50), default="USER")


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


# ================= WALLET TABLE =================

class Wallet(Base):

    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    balance = Column(Float, default=0)

    wallet_status = Column(String(50))

    created_at = Column(String(100))


# ================= WALLET TRANSACTIONS TABLE =================

class WalletTransaction(Base):

    __tablename__ = "wallet_transactions"

    id = Column(Integer, primary_key=True, index=True)

    wallet_id = Column(Integer)

    amount = Column(Float)

    transaction_type = Column(String(50))

    status = Column(String(50))

    created_at = Column(String(100))


# ================= RECEIPTS TABLE =================

class Receipt(Base):

    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(Integer)

    receipt_number = Column(String(100))

    file_url = Column(String(200))

    generated_at = Column(String(100))


# ================= REFUNDS TABLE =================

class Refund(Base):

    __tablename__ = "refunds"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(Integer)

    refund_amount = Column(Float)

    refund_status = Column(String(50))

    reason = Column(String(200))

    created_at = Column(String(100))


# ================= SECURITY LOGS TABLE =================

class SecurityLog(Base):

    __tablename__ = "security_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    activity = Column(String(200))

    ip_address = Column(String(100))

    status = Column(String(50))

    created_at = Column(String(100))


# ================= NOTIFICATIONS TABLE =================

class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    title = Column(String(100))

    message = Column(String(300))

    is_read = Column(String(20))

    created_at = Column(String(100))

class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    action = Column(String(200))

    entity = Column(String(100))

    created_at = Column(String(100))

class StatementLog(Base):

    __tablename__ = "statement_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    statement_type = Column(String(100))

    generated_at = Column(String(100))


    