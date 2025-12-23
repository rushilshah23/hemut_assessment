from pydantic import BaseModel


class CreateAdmin(BaseModel):
    email:str
    password:str
    confirm_password:str
    
    
class CreateAdminResponse(BaseModel):
    id:str
    user_id:str
    email:str
