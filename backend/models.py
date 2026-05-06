from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    client = Column(String(255), nullable=False)
    service_type = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    responsible = Column(String(255), nullable=False)
    current_stage = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False)
    priority = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    expected_end_date = Column(Date, nullable=False)
    actual_end_date = Column(Date, nullable=True)
    estimated_cost = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=True, default=0.0)
    technical_notes = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True, default=0.0)
    risk_level = Column(String(20), nullable=True, default="Baixo")
    risk_factors = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class StageHistory(Base):
    __tablename__ = "stage_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    stage = Column(String(100), nullable=False)
    started_at = Column(Date, nullable=False)
    completed_at = Column(Date, nullable=True)
    days_in_stage = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="operator")
