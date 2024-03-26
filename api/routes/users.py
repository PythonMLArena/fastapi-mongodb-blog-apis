from fastapi import APIRouter,HTTPException,status
from fastapi.encoders import jsonable_encoder
from api.schemas.schemas import User,PyObjectId, db,UserResponse
from api.utils import get_password_hash
import secrets

router = APIRouter(
    tags=["User Routes"]
    
)

@router.get("/")
def get():
    return {"message": "Hello World"}


@router.post("/registration",response_description="Register a User",response_model=UserResponse)
async def registration(user_info: User):
    user_info=jsonable_encoder(user_info)
    print(user_info)
    username_found=await db['users'].find_one({"name":user_info["name"]})
    email_found=await db['users'].find_one({"email":user_info["email"]})
    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username already taken")
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already taken")
    # hashed user password here                                   
    user_info["password"]=get_password_hash(user_info["password"])
    # create api key
    user_info["api_key"]=secrets.token_hex(30)
    new_user=await db["users"].insert_one(user_info)
    print(new_user)
    created_user=await db["users"].find_one({"_id": new_user.inserted_id})
    
    
    # send email 
    
    return created_user
    
    

