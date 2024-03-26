from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from api.schemas.schemas import db
from api.utils import verify_password
from api.oauth2 import create_access_token



router = APIRouter(prefix="/login",tags=["Authentication"])


@router.post("",status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm=Depends()):
    user= await db["users"].find_one({"name": user_credentials.username})
    if user and verify_password(user_credentials.password,user["password"]):
        # bearer token generation
        access_token=create_access_token({"id": user["_id"]})
        return ({"access_token":access_token, "token_type": "bearer"})
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid User")
        
    

