from pydantic import BaseModel, EmailStr

class Applicant(BaseModel):
    name: str
    email: EmailStr
    mobile: str