from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import os

SECRET_KEY = os.environ.get("JWT_SECRET", "supersecretkey")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {"id": user_id}

    except:
        raise HTTPException(status_code=401, detail="Invalid token")