from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum


class AttendanceTypeEnum(str, Enum):
    CHECK_IN = "CHECK_IN"
    CHECK_OUT = "CHECK_OUT"


class AttendanceRecord(BaseModel):
    local_id: str
    emp_id: str
    attendance_type: AttendanceTypeEnum = AttendanceTypeEnum.CHECK_IN
    date: date
    time: time
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photo: Optional[str] = None


class AttendanceSyncRequest(BaseModel):
    device_id: str
    records: List[AttendanceRecord]


class SyncResult(BaseModel):
    local_id: str
    server_id: Optional[str] = None
    status: str  # "synced", "failed", "duplicate"
    error: Optional[str] = None


class AttendanceSyncResponse(BaseModel):
    status: str  # "success", "partial", "failed"
    synced: int
    failed: int
    duplicates: int
    results: List[SyncResult]


class AttendanceResponse(BaseModel):
    id: str
    emp_id: str
    emp_code: Optional[str] = None
    emp_name: Optional[str] = None
    attendance_type: AttendanceTypeEnum = AttendanceTypeEnum.CHECK_IN
    date: date
    time: time
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    device_id: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
