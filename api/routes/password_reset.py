from fastapi import APIRouter,HTTPException,status
from api.oauth2 import create_access_token
from api.schemas.schemas import PasswordReset,db,NewPassword 
from api.utils import get_password_hash
from api.oauth2 import get_current_user

router = APIRouter(prefix="/password",tags=["Password Reset"])


@router.post("",response_description="Reset Password")
async def reset_password(user_email: PasswordReset):
    user = await db["users"].find_one({"email": user_email.email})
    if user is not None:
        token=create_access_token({"id":user["_id"]})
        ## Reset link and send email can be implemented here
        return token
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email not found")

@router.put("",response_description="Reset Password")
async def reset(token: str,new_password: NewPassword):
    request_data={k:v for k,v in new_password.dict().items() if v is not None}
    print(request_data)
    request_data['password']=get_password_hash(request_data['password'])
    if len(request_data)>=1:
        user= await get_current_user(token)
        update_result= await db["users"].update_one({"_id":user["_id"]}, {"$set":request_data})
        if update_result.modified_count==1:
            update_user= await db["users"].find_one({"_id":user["_id"]})
            if (update_user) is not None:
                return update_user
            else:
                return HTTPException()
        else:
            raise HTTPException()
    existing_user=await db["users"].find_one({"_id":user["_id"]})

