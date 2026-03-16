from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from app.database import get_db
from app.models.employee import Employee, EmployeeStatus
from app.models.user import User
from app.schemas.employee import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, 
    EmployeeWithDescriptor, FaceEnrollRequest
)
from app.utils.deps import get_current_user, require_admin
from app.utils.encryption import encrypt_descriptor, decrypt_descriptor

router = APIRouter(tags=["Employees"])


@router.get("", response_model=dict)
async def list_employees(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    department: Optional[str] = None,
    status: Optional[EmployeeStatus] = None,
    include_descriptors: bool = Query(False),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = select(Employee)
    count_query = select(func.count(Employee.id))
    
    if department:
        query = query.where(Employee.department == department)
        count_query = count_query.where(Employee.department == department)
    
    if status:
        query = query.where(Employee.status == status)
        count_query = count_query.where(Employee.status == status)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    employees = result.scalars().all()
    
    employee_list = []
    for emp in employees:
        emp_dict = {
            "id": emp.id,
            "emp_code": emp.emp_code,
            "name": emp.name,
            "email": emp.email,
            "department": emp.department,
            "face_enrolled": emp.face_enrolled,
            "status": emp.status,
            "created_at": emp.created_at,
            "updated_at": emp.updated_at
        }
        if include_descriptors and emp.face_descriptor:
            try:
                emp_dict["face_descriptor"] = decrypt_descriptor(emp.face_descriptor)
            except Exception:
                emp_dict["face_descriptor"] = None
        employee_list.append(emp_dict)
    
    return {
        "employees": employee_list,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return EmployeeResponse.model_validate(employee)


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    result = await db.execute(select(Employee).where(Employee.emp_code == employee_data.emp_code))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(status_code=400, detail="Employee code already exists")
    
    employee = Employee(**employee_data.model_dump())
    db.add(employee)
    await db.commit()
    await db.refresh(employee)
    
    return EmployeeResponse.model_validate(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    update_data = employee_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(employee, field, value)
    
    await db.commit()
    await db.refresh(employee)
    
    return EmployeeResponse.model_validate(employee)


@router.delete("/{employee_id}")
async def delete_employee(
    employee_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.status = EmployeeStatus.INACTIVE
    await db.commit()
    
    return {"message": "Employee deactivated successfully"}


@router.post("/{employee_id}/enroll-face")
async def enroll_face(
    employee_id: str,
    face_data: FaceEnrollRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if len(face_data.face_descriptors) < 5:
        raise HTTPException(status_code=400, detail="Minimum 5 face samples required")
    
    num_samples = len(face_data.face_descriptors)
    descriptor_length = len(face_data.face_descriptors[0])
    
    avg_descriptor = []
    for i in range(descriptor_length):
        avg_value = sum(d[i] for d in face_data.face_descriptors) / num_samples
        avg_descriptor.append(avg_value)
    
    encrypted = encrypt_descriptor(avg_descriptor)
    employee.face_descriptor = encrypted
    employee.face_enrolled = True
    
    await db.commit()
    
    return {
        "status": "success",
        "message": "Face enrolled successfully",
        "employee_id": employee_id,
        "samples_processed": num_samples
    }


@router.get("/{employee_id}/face-status")
async def get_face_status(
    employee_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return {
        "employee_id": employee_id,
        "face_enrolled": employee.face_enrolled,
        "enrolled_at": employee.updated_at if employee.face_enrolled else None
    }


@router.delete("/{employee_id}/face")
async def delete_face(
    employee_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    result = await db.execute(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee.face_descriptor = None
    employee.face_enrolled = False
    
    await db.commit()
    
    return {"message": "Face data removed successfully"}
