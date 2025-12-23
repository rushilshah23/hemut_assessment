from pydantic import BaseModel, EmailStr


class CreateAdmin(BaseModel):
    email:EmailStr
    password:str
    confirm_password:str
    
    
class CreateAdminResponse(BaseModel):
    id:str
    user_id:str
    email:EmailStr


class LoginAdmin(BaseModel):
    email: EmailStr
    password: str
    
class LoginAdminResponse(BaseModel):
    id: str
    user_id: str
    email: str
    access_token: str