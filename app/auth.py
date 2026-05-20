import hashlib

from jose import jwt

from datetime import datetime, timedelta
from fastapi import Depends, HTTPException

# ================= SECRET KEY =================

SECRET_KEY = "creditcardproject"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ================= HASH PASSWORD =================

def hash_password(password: str):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ================= VERIFY PASSWORD =================

def verify_password(
    plain_password,
    hashed_password
):

    return hash_password(
        plain_password
    ) == hashed_password


# ================= CREATE ACCESS TOKEN =================

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user_role(token: str = Depends(oauth2_scheme)):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        role = payload.get("role")

        return role

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )


def admin_only(role: str = Depends(get_current_user_role)):

    if role != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )