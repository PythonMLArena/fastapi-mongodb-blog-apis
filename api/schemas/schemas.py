import motor.motor_asyncio 
import os
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel,Field,EmailStr 

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))


db=client.blog_api
# NOSQL BSON AND JSON HANDLER
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate 
        
    @classmethod
    def validate(cls,v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid object")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls,field_schema):
        field_schema.update(type="string")
        
        
            
    
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
    