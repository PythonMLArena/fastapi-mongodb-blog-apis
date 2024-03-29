from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.encoders import jsonable_encoder
from api.schemas.schemas import BlogContent,BlogContentResponse,db
from api.oauth2 import get_current_user
from datetime import datetime
from typing import List
from fastapi.responses import JSONResponse

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
    
@router.get("/all",response_description="GET BLOG CONTENT HERE",response_model=List[BlogContentResponse])
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
    
@router.put("/{id}",response_description="Update Blog Here",response_model=BlogContentResponse)
async def update_blog(id:str,blog_content: BlogContent,current_user=Depends(get_current_user)):
    if blog_post := await db["blogPost"].find_one({"id":id}):
        if blog_post["author_id"]==current_user["_id"]:
            try:
                blog_content = {k:v for k,v in blog_content.dict().items() if v is not None}
                if len(blog_content)>=1:
                    update_blog_content=await db["blogPost"].update_one({"_id":id},{"$set":blog_content}) 
                    if update_blog_content.modified_count==1:
                        if (updated_blog_post := await db["blogPost"].find_one({"_id":id})) is not None:
                            return updated_blog_post
                    if (existing_post := await db["blogPost"].find_one({"_id":id})) is not None:
                        return existing_post
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog content not found")            
            except Exception as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized here to update the post")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog content not found")
            
            
@router.delete("/{id}",response_description="Delete post here")
async def delete_blog(id: str,current_user=Depends(get_current_user)):
    if blog_post := await db["blogPost"].find_one({"_id":id}):
        if blog_post["author_id"] == current_user["_id"]:
            try:
                delete_result = await db["blogPost"].delete_one({"_id":id})
                if delete_result.deleted_count==1:
                    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,detail="Content not found")
            except Exception as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Internal Server Error")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized here to update the post")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog content not found")
            
    
    
    