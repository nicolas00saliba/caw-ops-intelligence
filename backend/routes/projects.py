from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date

from database import get_db
from models import Project, StageHistory
from schemas import ProjectCreate, ProjectUpdate, ProjectResponse, StageHistoryResponse, RiskAnalysisResponse
from risk_engine import calculate_risk

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectResponse])
def list_projects(
    status: Optional[str] = Query(None),
    service_type: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    responsible: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    risk_level: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Project)

    if status:
        query = query.filter(Project.status == status)
    if service_type:
        query = query.filter(Project.service_type == service_type)
    if city:
        query = query.filter(Project.city == city)
    if state:
        query = query.filter(Project.state == state)
    if responsible:
        query = query.filter(Project.responsible == responsible)
    if priority:
        query = query.filter(Project.priority == priority)
    if risk_level:
        query = query.filter(Project.risk_level == risk_level)
    if search:
        query = query.filter(Project.name.ilike(f"%{search}%"))

    projects = query.order_by(Project.id.desc()).all()
    return projects


@router.get("/filters")
def get_filter_options(db: Session = Depends(get_db)):
    """Retorna opções disponíveis para filtros."""
    projects = db.query(Project).all()

    statuses = sorted(set(p.status for p in projects))
    service_types = sorted(set(p.service_type for p in projects))
    cities = sorted(set(p.city for p in projects))
    states = sorted(set(p.state for p in projects))
    responsibles = sorted(set(p.responsible for p in projects))
    priorities = ["Crítica", "Alta", "Média", "Baixa"]
    risk_levels = ["Alto", "Médio", "Baixo"]

    return {
        "statuses": statuses,
        "service_types": service_types,
        "cities": cities,
        "states": states,
        "responsibles": responsibles,
        "priorities": priorities,
        "risk_levels": risk_levels,
    }


@router.get("/risk-analysis", response_model=List[RiskAnalysisResponse])
def get_risk_analysis(db: Session = Depends(get_db)):
    """Retorna análise de risco de todos os projetos ativos."""
    projects = db.query(Project).filter(Project.status != "Finalizado").all()
    all_projects_data = [
        {
            "service_type": p.service_type,
            "status": p.status,
            "actual_end_date": p.actual_end_date,
            "expected_end_date": p.expected_end_date,
        }
        for p in db.query(Project).all()
    ]

    results = []
    for project in projects:
        # Buscar histórico de etapas
        stage_history = db.query(StageHistory).filter(
            StageHistory.project_id == project.id
        ).all()

        history_data = [
            {"stage": sh.stage, "started_at": sh.started_at, "completed_at": sh.completed_at}
            for sh in stage_history
        ]

        project_data = {
            "current_stage": project.current_stage,
            "start_date": project.start_date,
            "expected_end_date": project.expected_end_date,
            "actual_end_date": project.actual_end_date,
            "estimated_cost": project.estimated_cost,
            "actual_cost": project.actual_cost,
            "service_type": project.service_type,
            "priority": project.priority,
            "status": project.status,
        }

        risk = calculate_risk(project_data, all_projects_data, history_data)

        results.append(RiskAnalysisResponse(
            project_id=project.id,
            project_name=project.name,
            service_type=project.service_type,
            city=project.city,
            state=project.state,
            current_stage=project.current_stage,
            risk_score=risk["risk_score"],
            risk_level=risk["risk_level"],
            risk_factors=risk["risk_factors"],
            days_delayed=risk["days_delayed"],
            cost_overrun_pct=risk["cost_overrun_pct"],
        ))

    # Ordenar por risco decrescente
    results.sort(key=lambda x: x.risk_score, reverse=True)
    return results


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return project


@router.get("/{project_id}/history", response_model=List[StageHistoryResponse])
def get_project_history(project_id: int, db: Session = Depends(get_db)):
    history = db.query(StageHistory).filter(
        StageHistory.project_id == project_id
    ).order_by(StageHistory.started_at).all()
    return history


@router.get("/{project_id}/risk")
def get_project_risk(project_id: int, db: Session = Depends(get_db)):
    """Retorna análise de risco detalhada de um projeto específico."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    all_projects_data = [
        {
            "service_type": p.service_type,
            "status": p.status,
            "actual_end_date": p.actual_end_date,
            "expected_end_date": p.expected_end_date,
        }
        for p in db.query(Project).all()
    ]

    stage_history = db.query(StageHistory).filter(
        StageHistory.project_id == project_id
    ).all()

    history_data = [
        {"stage": sh.stage, "started_at": sh.started_at, "completed_at": sh.completed_at}
        for sh in stage_history
    ]

    project_data = {
        "current_stage": project.current_stage,
        "start_date": project.start_date,
        "expected_end_date": project.expected_end_date,
        "actual_end_date": project.actual_end_date,
        "estimated_cost": project.estimated_cost,
        "actual_cost": project.actual_cost,
        "service_type": project.service_type,
        "priority": project.priority,
        "status": project.status,
    }

    risk = calculate_risk(project_data, all_projects_data, history_data)
    return risk


@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    # Calcular risco inicial
    project_data = {
        "current_stage": project.current_stage,
        "start_date": project.start_date,
        "expected_end_date": project.expected_end_date,
        "actual_end_date": project.actual_end_date,
        "estimated_cost": project.estimated_cost,
        "actual_cost": project.actual_cost or 0,
        "service_type": project.service_type,
        "priority": project.priority,
        "status": project.status,
    }

    risk = calculate_risk(project_data, [], [])

    db_project = Project(
        **project.model_dump(),
        risk_score=risk["risk_score"],
        risk_level=risk["risk_level"],
        risk_factors="|".join(risk["risk_factors"]),
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # Criar entrada no histórico
    stage_entry = StageHistory(
        project_id=db_project.id,
        stage=project.current_stage,
        started_at=project.start_date,
    )
    db.add(stage_entry)
    db.commit()

    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    # Verificar se a etapa mudou
    old_stage = db_project.current_stage
    new_stage = project.current_stage

    # Atualizar campos
    for key, value in project.model_dump().items():
        setattr(db_project, key, value)

    # Recalcular risco
    project_data = {
        "current_stage": project.current_stage,
        "start_date": project.start_date,
        "expected_end_date": project.expected_end_date,
        "actual_end_date": project.actual_end_date,
        "estimated_cost": project.estimated_cost,
        "actual_cost": project.actual_cost or 0,
        "service_type": project.service_type,
        "priority": project.priority,
        "status": project.status,
    }

    risk = calculate_risk(project_data, [], [])
    db_project.risk_score = risk["risk_score"]
    db_project.risk_level = risk["risk_level"]
    db_project.risk_factors = "|".join(risk["risk_factors"])

    # Se a etapa mudou, registrar no histórico
    if old_stage != new_stage:
        # Finalizar etapa anterior
        old_history = db.query(StageHistory).filter(
            StageHistory.project_id == project_id,
            StageHistory.stage == old_stage,
            StageHistory.completed_at.is_(None),
        ).first()
        if old_history:
            old_history.completed_at = date.today()
            old_history.days_in_stage = (date.today() - old_history.started_at).days

        # Criar nova entrada
        new_history = StageHistory(
            project_id=project_id,
            stage=new_stage,
            started_at=date.today(),
        )
        db.add(new_history)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")

    db.query(StageHistory).filter(StageHistory.project_id == project_id).delete()
    db.delete(db_project)
    db.commit()
    return {"message": "Projeto excluído com sucesso"}
