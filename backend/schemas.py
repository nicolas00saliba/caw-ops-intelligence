from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class ProjectBase(BaseModel):
    name: str
    client: str
    service_type: str
    city: str
    state: str
    responsible: str
    current_stage: str
    status: str
    priority: str
    start_date: date
    expected_end_date: date
    actual_end_date: Optional[date] = None
    estimated_cost: float
    actual_cost: Optional[float] = 0.0
    technical_notes: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    risk_score: Optional[float] = 0.0
    risk_level: Optional[str] = "Baixo"
    risk_factors: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StageHistoryBase(BaseModel):
    project_id: int
    stage: str
    started_at: date
    completed_at: Optional[date] = None
    days_in_stage: Optional[int] = None
    notes: Optional[str] = None


class StageHistoryResponse(StageHistoryBase):
    id: int

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


class DashboardStats(BaseModel):
    total_projects: int
    in_progress: int
    delayed: int
    high_risk: int
    total_estimated_cost: float
    total_actual_cost: float


class RiskAnalysisResponse(BaseModel):
    project_id: int
    project_name: str
    service_type: str
    city: str
    state: str
    current_stage: str
    risk_score: float
    risk_level: str
    risk_factors: List[str]
    days_delayed: int
    cost_overrun_pct: float
