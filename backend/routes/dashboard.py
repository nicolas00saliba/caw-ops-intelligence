from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from collections import defaultdict

from database import get_db
from models import Project, StageHistory
from schemas import DashboardStats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais para o dashboard."""
    projects = db.query(Project).all()

    total = len(projects)
    in_progress = sum(1 for p in projects if p.status == "Em andamento")
    delayed = sum(1 for p in projects if p.status == "Atrasado")
    high_risk = sum(1 for p in projects if p.risk_level == "Alto")
    total_estimated = sum(p.estimated_cost for p in projects)
    total_actual = sum(p.actual_cost or 0 for p in projects)

    return DashboardStats(
        total_projects=total,
        in_progress=in_progress,
        delayed=delayed,
        high_risk=high_risk,
        total_estimated_cost=round(total_estimated, 2),
        total_actual_cost=round(total_actual, 2),
    )


@router.get("/charts/status")
def get_projects_by_status(db: Session = Depends(get_db)):
    """Projetos por status para gráfico de pizza/donut."""
    results = (
        db.query(Project.status, func.count(Project.id))
        .group_by(Project.status)
        .all()
    )
    return {
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results],
    }


@router.get("/charts/service-type")
def get_projects_by_service_type(db: Session = Depends(get_db)):
    """Projetos por tipo de serviço para gráfico de barras."""
    results = (
        db.query(Project.service_type, func.count(Project.id))
        .group_by(Project.service_type)
        .order_by(func.count(Project.id).desc())
        .all()
    )
    return {
        "labels": [r[0] for r in results],
        "values": [r[1] for r in results],
    }


@router.get("/charts/avg-delay-by-stage")
def get_avg_delay_by_stage(db: Session = Depends(get_db)):
    """Atraso médio por etapa (em dias)."""
    stages = ["Orçamento", "Projeto técnico", "Produção", "Pré-montagem", "Expedição", "Instalação"]

    results = []
    for stage in stages:
        avg_days = (
            db.query(func.avg(StageHistory.days_in_stage))
            .filter(StageHistory.stage == stage, StageHistory.days_in_stage.isnot(None))
            .scalar()
        )
        results.append(round(avg_days or 0, 1))

    return {
        "labels": stages,
        "values": results,
    }


@router.get("/charts/cost-comparison")
def get_cost_comparison(db: Session = Depends(get_db)):
    """Custo previsto vs. realizado por tipo de serviço."""
    service_types = (
        db.query(Project.service_type).distinct().all()
    )

    labels = []
    estimated = []
    actual = []

    for (st,) in sorted(service_types, key=lambda x: x[0]):
        projects = db.query(Project).filter(Project.service_type == st).all()
        total_est = sum(p.estimated_cost for p in projects)
        total_act = sum(p.actual_cost or 0 for p in projects)
        labels.append(st)
        estimated.append(round(total_est, 2))
        actual.append(round(total_act, 2))

    return {
        "labels": labels,
        "estimated": estimated,
        "actual": actual,
    }


@router.get("/charts/risk-distribution")
def get_risk_distribution(db: Session = Depends(get_db)):
    """Distribuição de risco entre projetos ativos."""
    active_projects = db.query(Project).filter(Project.status != "Finalizado").all()

    distribution = {"Baixo": 0, "Médio": 0, "Alto": 0}
    for p in active_projects:
        level = p.risk_level or "Baixo"
        if level in distribution:
            distribution[level] += 1

    return {
        "labels": list(distribution.keys()),
        "values": list(distribution.values()),
    }


@router.get("/charts/projects-by-city")
def get_projects_by_city(db: Session = Depends(get_db)):
    """Top 10 cidades com mais projetos."""
    results = (
        db.query(Project.city, Project.state, func.count(Project.id))
        .group_by(Project.city, Project.state)
        .order_by(func.count(Project.id).desc())
        .limit(10)
        .all()
    )
    return {
        "labels": [f"{r[0]}/{r[1]}" for r in results],
        "values": [r[2] for r in results],
    }


@router.get("/charts/monthly-progress")
def get_monthly_progress(db: Session = Depends(get_db)):
    """Projetos iniciados e finalizados por mês (últimos 6 meses)."""
    from datetime import date, timedelta

    today = date.today()
    months = []
    started = []
    finished = []

    for i in range(5, -1, -1):
        month_start = date(today.year, today.month, 1) - timedelta(days=30 * i)
        month_end = date(month_start.year, month_start.month + 1, 1) if month_start.month < 12 else date(month_start.year + 1, 1, 1)

        started_count = (
            db.query(func.count(Project.id))
            .filter(Project.start_date >= month_start, Project.start_date < month_end)
            .scalar()
        )

        finished_count = (
            db.query(func.count(Project.id))
            .filter(Project.actual_end_date >= month_start, Project.actual_end_date < month_end)
            .scalar()
        )

        month_names = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
        months.append(f"{month_names[month_start.month - 1]}/{month_start.year}")
        started.append(started_count or 0)
        finished.append(finished_count or 0)

    return {
        "labels": months,
        "started": started,
        "finished": finished,
    }
