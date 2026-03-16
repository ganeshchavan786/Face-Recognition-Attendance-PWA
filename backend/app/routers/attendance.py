from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from typing import Optional
from datetime import date, datetime

from app.database import get_db
from app.models.attendance import Attendance, SyncStatus, AttendanceType
from app.models.employee import Employee
from app.models.user import User
from app.schemas.attendance import (
    AttendanceSyncRequest, AttendanceSyncResponse, 
    SyncResult, AttendanceResponse
)
from app.utils.deps import get_current_user, require_supervisor

router = APIRouter(tags=["Attendance"])


@router.post("/sync", response_model=AttendanceSyncResponse)
async def sync_attendance(
    sync_data: AttendanceSyncRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = []
    synced = 0
    failed = 0
    duplicates = 0
    
    for record in sync_data.records:
        try:
            emp_result = await db.execute(
                select(Employee).where(Employee.id == record.emp_id)
            )
            employee = emp_result.scalar_one_or_none()
            
            if not employee:
                results.append(SyncResult(
                    local_id=record.local_id,
                    status="failed",
                    error="Employee not found"
                ))
                failed += 1
                continue
            
            # Check for duplicate - same employee, same date, same type
            existing = await db.execute(
                select(Attendance).where(
                    and_(
                        Attendance.emp_id == record.emp_id,
                        Attendance.date == record.date,
                        Attendance.attendance_type == record.attendance_type.value
                    )
                )
            )
            if existing.scalar_one_or_none():
                results.append(SyncResult(
                    local_id=record.local_id,
                    status="duplicate",
                    error=f"{record.attendance_type.value} already exists for this date"
                ))
                duplicates += 1
                continue
            
            attendance = Attendance(
                local_id=record.local_id,
                emp_id=record.emp_id,
                attendance_type=AttendanceType(record.attendance_type.value),
                date=record.date,
                time=record.time,
                latitude=record.latitude,
                longitude=record.longitude,
                device_id=sync_data.device_id,
                photo=record.photo,
                sync_status=SyncStatus.SYNCED,
                synced_at=datetime.utcnow()
            )
            
            db.add(attendance)
            await db.flush()
            
            results.append(SyncResult(
                local_id=record.local_id,
                server_id=attendance.id,
                status="synced"
            ))
            synced += 1
            
        except Exception as e:
            results.append(SyncResult(
                local_id=record.local_id,
                status="failed",
                error=str(e)
            ))
            failed += 1
    
    await db.commit()
    
    if failed == 0 and duplicates == 0:
        status = "success"
    elif synced > 0:
        status = "partial"
    else:
        status = "failed"
    
    return AttendanceSyncResponse(
        status=status,
        synced=synced,
        failed=failed,
        duplicates=duplicates,
        results=results
    )


@router.get("", response_model=dict)
async def list_attendance(
    start_date: date = Query(...),
    end_date: date = Query(...),
    emp_id: Optional[str] = None,
    department: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    query = select(Attendance, Employee).join(Employee, Attendance.emp_id == Employee.id)
    count_query = select(func.count(Attendance.id)).join(Employee, Attendance.emp_id == Employee.id)
    
    query = query.where(and_(
        Attendance.date >= start_date,
        Attendance.date <= end_date
    ))
    count_query = count_query.where(and_(
        Attendance.date >= start_date,
        Attendance.date <= end_date
    ))
    
    if emp_id:
        query = query.where(Attendance.emp_id == emp_id)
        count_query = count_query.where(Attendance.emp_id == emp_id)
    
    if department:
        query = query.where(Employee.department == department)
        count_query = count_query.where(Employee.department == department)
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    query = query.order_by(Attendance.date.desc(), Attendance.time.desc())
    query = query.offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    records = result.all()
    
    attendance_list = []
    for att, emp in records:
        attendance_list.append({
            "id": att.id,
            "emp_id": att.emp_id,
            "emp_code": emp.emp_code,
            "emp_name": emp.name,
            "attendance_type": att.attendance_type.value if att.attendance_type else "CHECK_IN",
            "date": att.date.isoformat(),
            "time": att.time.isoformat(),
            "latitude": att.latitude,
            "longitude": att.longitude,
            "device_id": att.device_id,
            "created_at": att.created_at.isoformat()
        })
    
    return {
        "records": attendance_list,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit if total > 0 else 0
    }


@router.get("/summary")
async def attendance_summary(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_supervisor)
):
    total_employees = await db.execute(select(func.count(Employee.id)))
    total_emp_count = total_employees.scalar()
    
    present_query = select(func.count(func.distinct(Attendance.emp_id))).where(
        and_(
            Attendance.date >= start_date,
            Attendance.date <= end_date
        )
    )
    present_result = await db.execute(present_query)
    present_count = present_result.scalar()
    
    total_attendance = await db.execute(
        select(func.count(Attendance.id)).where(
            and_(
                Attendance.date >= start_date,
                Attendance.date <= end_date
            )
        )
    )
    total_att_count = total_attendance.scalar()
    
    return {
        "total_employees": total_emp_count,
        "employees_present": present_count,
        "total_attendance_records": total_att_count,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }
