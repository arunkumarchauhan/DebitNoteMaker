from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from .config import settings

def create_access_token(data:dict, expire_delta:timedelta|None=None):
    to_encode=data.copy()
    if expire_delta:
        expire=datetime.now()+expire_delta
    else:
        expire=datetime.now()+ timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,key=settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return encoded_jwt
