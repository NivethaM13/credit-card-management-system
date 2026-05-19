import hashlib

from jose import jwt, JWTError

from datetime import datetime, timedelta


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


# ================= VERIFY TOKEN =================

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        return email

    except JWTError:

        return None