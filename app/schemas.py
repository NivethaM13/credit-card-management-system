from pydantic import BaseModel



class UserCreate(BaseModel):

    name: str

    email: str

    password: str


class UserLogin(BaseModel):

    email: str

    password: str



class CardCreate(BaseModel):

    user_id: int

    card_holder: str

    card_number: str

    expiry: str




class PaymentCreate(BaseModel):

    user_id: int

    card_id: int

    amount: float


class LoginSchema(BaseModel):
    email: str
    
    password: str

    # ================= WALLET =================

class WalletCreate(BaseModel):

    user_id: int


class AddMoney(BaseModel):

    wallet_id: int

    amount: float

# ================= RECEIPT =================

class ReceiptCreate(BaseModel):

    transaction_id: int    


    # ================= REFUND =================

class RefundCreate(BaseModel):

    transaction_id: int

    refund_amount: float

    reason: str

# ================= SECURITY LOG =================

class SecurityLogCreate(BaseModel):

    user_id: int

    activity: str

    ip_address: str

    status: str   

# ================= NOTIFICATION =================

class NotificationCreate(BaseModel):

    user_id: int

    title: str

    message: str  

    # ================= AUDIT LOG =================

class AuditLogCreate(BaseModel):

    user_id: int

    action: str

    entity: str 

 # ================= STATEMENT LOG =================

class StatementLogCreate(BaseModel):

    user_id: int

    statement_type: str   
