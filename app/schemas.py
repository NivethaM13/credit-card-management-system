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