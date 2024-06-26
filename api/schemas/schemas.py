from typing import Any
import motor.motor_asyncio 
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel,Field,EmailStr 
from pydantic_core import core_schema
load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://prathameshmane852:2aKnYDkcVgROyUWo@cluster0.5vrltau.mongodb.net/")


db=client["blog_api"]
# NOSQL BSON AND JSON HANDLER
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")

        return ObjectId(value)
        
        
            
    
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    class Config:
        allowed_population_by_field_name= True
        arbitrary_type_allowed= True
        json_encoders={ObjectId: str}
        schema_extra={
            "example":{
                "name": "This is the name",
                "email": "This is the email",
                "password": "This is the password"
            }
        }
    
class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    class Config:
        allowed_population_by_field_name= True
        arbitrary_type_allowed= True
        json_encoders={ObjectId: str}
        schema_extra={
            "example":{
                "name": "This is the name",
                "email": "This is the email",
            }
        }
        
class TokenData(BaseModel):
    id: str 
    
    
class PasswordReset(BaseModel):
    email: EmailStr
    
class NewPassword(BaseModel):
    password: str
    
    
class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    title : str = Field(...)
    body : str = Field(...)
    
    
    class Config:
        allowed_population_by_field_name= True
        arbitrary_type_allowed= True
        json_encoders={ObjectId: str}
        schema_extra={
            "example":{
                "title": "This is the title of the blog",
                "body": "This is the body of the blog",
            }
        }
    
    
class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
    title : str = Field(...)
    body : str = Field(...)
    auther_name : str = Field(...)
    auther_id : str = Field(...)
    created_at : str = Field(...)
    
    
    class Config:
        allowed_population_by_field_name= True
        arbitrary_type_allowed= True
        json_encoders={ObjectId: str}
        schema_extra={
            "example":{
                "title": "This is the title of the blog",
                "body": "This is the body of the blog",
                "auther_name": "This is the auther name of the blog",
                "auther_id": "This is the id of the auther",
                "created_at": "date created",
            }
        }