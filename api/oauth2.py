from jose import jwt ,JWTError
from typing import Dict
from datetime import datetime,timedelta
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import os
from api.schemas.schemas import TokenData,db

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MIN")
ALGORITHM=os.getenv("ALGORITHM")
SECRET_KEY=os.getenv("SECRET_KEY")

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(payload: Dict):
    to_encode= payload.copy()
    
    expiration_time= datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp":expiration_time})
    jwt_token=jwt.encode(to_encode,key="8xaR8r1nrDJwKSBiQ8rddnQ4ShV_mOqdlpFvQlcc",algorithm="HS256")
    print(jwt_token)
    return jwt_token


def verify_access_token(token: str, credential_exception):
    try:
        payload=jwt.decode(token,key="8xaR8r1nrDJwKSBiQ8rddnQ4ShV_mOqdlpFvQlcc",algorithm="HS256")
        id: str = payload.get("id")
        if not id:
            raise credential_exception
        token_data= TokenData(id=id)
        return token_data
    except JWTError:
        raise credential_exception
        
async def get_current_user(token: str):
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token not found",
        headers={"WWW-Authenticate":"Bearer"}
    )
    current_user_id=verify_access_token(token,credential_exception).id
    
    current_user = await db["users"].find_one({"_id":current_user_id})
    return current_user
    
    


    
    
    

    
    
    
