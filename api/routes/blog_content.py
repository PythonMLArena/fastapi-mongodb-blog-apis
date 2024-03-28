from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.encoders import jsonable_encoder
from api.schemas.schemas import BlogContent,BlogContentResponse,db
from api.oauth2 import get_current_user
from datetime import datetime
from typing import List

router = APIRouter(prefix="/blog",tags=["Blog Content"])




@router.post("",response_description="Create a new blog",response_model=BlogContentResponse)
async def create_blog(blog_content: BlogContent,current_user=Depends(get_current_user)):
    try:
        blog_content=jsonable_encoder(blog_content)
        blog_content["auther_name"]=current_user["name"]
        blog_content["auther_id"]=current_user["_id"]
        blog_content["created_at"]=str(datetime.utcnow())
        new_blog_content=await db["blogPost"].insert_one(blog_content)
        
        create_blog_post=await db["blogPost"].find_one({"_id":new_blog_content.inserted_id})
        return create_blog_post
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")
    
@router.get("",response_description="GET BLOG CONTENT HERE",response_model=List[BlogContentResponse])
async def get_blog_content(limit: int=4,orderby: str="created_at",current_user=Depends(get_current_user)):
    try:
        output=await db["blogPost"].find().sort(orderby,-1).to_list(limit)
        return output
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")
    
@router.get("",response_description="GET BLOG CONTENT HERE",response_model=BlogContentResponse)
async def get_blog_by_id(id: str,current_user=Depends(get_current_user)):
    try:
        output=await db["blogPost"].find_one({"_id":id})
        if output is None:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog with this id not found")
            
        return output
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal server error")