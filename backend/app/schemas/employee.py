from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.employee import EmployeeStatus


class EmployeeCreate(BaseModel):
    emp_code: str = Field(..., min_length=1, max_length=20)
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = None


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    status: Optional[EmployeeStatus] = None


class EmployeeResponse(BaseModel):
    id: str
    emp_code: str
    name: str
    email: Optional[str] = None
    department: Optional[str] = None
    face_enrolled: bool
    status: EmployeeStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class EmployeeWithDescriptor(EmployeeResponse):
    face_descriptor: Optional[List[float]] = None


class FaceEnrollRequest(BaseModel):
    face_descriptors: List[List[float]] = Field(..., min_length=5, max_length=10)
