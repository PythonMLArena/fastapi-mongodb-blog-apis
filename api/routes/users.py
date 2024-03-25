from fastapi import APIRouter,HTTPException,status
from fastapi.encoders import jsonable_encoder
from schemas.schemas import User,PyObjectId, db

router = APIRouter(
    tags=["User Routes"]
    
)

@router.get("/")
def get():
    return {"message": "Hello World"}


@router.post("/registration",response_description="Register a User")
async def registration(user_info: User):
    user_info=jsonable_encoder(user_info)
    print(user_info)
    username_found=await db['users'].find_one({"name":user_info["name"]})
    email_found=await db['users'].find_one({"email":user_info["email"]})
    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username already taken")
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already taken")
                                           
    #user_info["password"]=
    

