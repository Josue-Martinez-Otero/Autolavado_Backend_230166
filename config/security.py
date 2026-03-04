import os
from fastapi.security import APIKeyHeader
from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# ==============================
# 🔑 CONFIGURACIÓN HASH
# ==============================
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Genera hash seguro de contraseña."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# 🔐 HEADER AUTHORIZATION
# ==============================
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)


# ==============================
# 🔑 CONFIGURACIÓN JWT
# ==============================
SECRET_KEY = os.getenv("SECRET_KEY") or "clave_por_defecto_para_test_123!"
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


# ==============================
# 🎟 CREAR TOKEN
# ==============================
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Crea un JSON Web Token (JWT) firmado.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt  


# ==============================
# 🔎 VALIDAR TOKEN
# ==============================
def get_current_user(token: str = Depends(api_key_scheme)):
    """
    Valida el token recibido en el header Authorization.
    """
    credentials_exception = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        # Quitar "Bearer " si viene en el token
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        return username

    except (JWTError, IndexError, AttributeError):
        raise credentials_exception