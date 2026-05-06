"""
CAW Ops Intelligence - Motor de Análise de Risco Operacional

Este módulo implementa um sistema de scoring de risco de atraso para projetos
de infraestrutura de telecomunicações e energia. O modelo utiliza uma combinação
de regras de negócio e pesos calibrados para calcular a probabilidade de atraso.

Fatores considerados:
1. Tempo na etapa atual (estagnação)
2. Desvio de custo (custo realizado vs. estimado)
3. Proximidade do prazo de vencimento
4. Complexidade do tipo de serviço
5. Histórico de atrasos em serviços semelhantes
6. Prioridade do projeto
"""

from datetime import date, timedelta
from typing import List, Tuple
import numpy as np


# Complexidade por tipo de serviço (0 a 1)
SERVICE_COMPLEXITY = {
    "Torre Telecom": 0.85,
    "Fundação": 0.70,
    "Poste": 0.45,
    "Reforço Estrutural": 0.75,
    "Subestação": 0.90,
    "Estrutura Metálica": 0.80,
    "Manutenção": 0.40,
}

# Tempo médio esperado por etapa (em dias)
EXPECTED_STAGE_DURATION = {
    "Orçamento": 15,
    "Projeto técnico": 30,
    "Produção": 45,
    "Pré-montagem": 20,
    "Expedição": 10,
    "Instalação": 25,
    "Finalizado": 0,
}

# Peso de cada fator no score final
WEIGHTS = {
    "stagnation": 0.25,
    "cost_overrun": 0.20,
    "deadline_proximity": 0.25,
    "complexity": 0.15,
    "historical_delay": 0.10,
    "priority": 0.05,
}

# Prioridade como fator de risco
PRIORITY_RISK = {
    "Crítica": 0.9,
    "Alta": 0.7,
    "Média": 0.4,
    "Baixa": 0.2,
}


def calculate_stagnation_score(current_stage: str, start_date: date, stage_history: list) -> Tuple[float, str]:
    """Calcula o score de estagnação baseado no tempo na etapa atual."""
    if current_stage == "Finalizado":
        return 0.0, ""

    expected_days = EXPECTED_STAGE_DURATION.get(current_stage, 20)

    # Encontrar quando a etapa atual começou
    stage_start = start_date
    for h in stage_history:
        if h.get("stage") == current_stage and h.get("started_at"):
            stage_start = h["started_at"] if isinstance(h["started_at"], date) else date.fromisoformat(str(h["started_at"]))
            break

    days_in_stage = (date.today() - stage_start).days
    ratio = days_in_stage / max(expected_days, 1)

    if ratio > 2.5:
        score = 1.0
        factor = f"Etapa '{current_stage}' parada há {days_in_stage} dias (esperado: {expected_days} dias)"
    elif ratio > 1.5:
        score = 0.75
        factor = f"Etapa '{current_stage}' com {days_in_stage} dias, acima do esperado ({expected_days} dias)"
    elif ratio > 1.0:
        score = 0.4
        factor = f"Etapa '{current_stage}' levemente acima do prazo esperado"
    else:
        score = ratio * 0.3
        factor = ""

    return min(score, 1.0), factor


def calculate_cost_overrun_score(estimated_cost: float, actual_cost: float) -> Tuple[float, str]:
    """Calcula o score de desvio de custo."""
    if estimated_cost <= 0:
        return 0.0, ""

    overrun_pct = ((actual_cost - estimated_cost) / estimated_cost) * 100

    if overrun_pct > 30:
        score = 1.0
        factor = f"Custo realizado {overrun_pct:.0f}% acima do previsto"
    elif overrun_pct > 15:
        score = 0.7
        factor = f"Custo realizado {overrun_pct:.0f}% acima do previsto"
    elif overrun_pct > 5:
        score = 0.4
        factor = f"Custo realizado {overrun_pct:.0f}% acima do previsto"
    elif overrun_pct > 0:
        score = 0.2
        factor = ""
    else:
        score = 0.0
        factor = ""

    return min(score, 1.0), factor


def calculate_deadline_proximity_score(expected_end_date: date, current_stage: str) -> Tuple[float, str]:
    """Calcula o score de proximidade do prazo."""
    if current_stage == "Finalizado":
        return 0.0, ""

    days_remaining = (expected_end_date - date.today()).days

    if days_remaining < 0:
        score = 1.0
        factor = f"Prazo vencido há {abs(days_remaining)} dias"
    elif days_remaining < 7:
        score = 0.9
        factor = f"Prazo vence em {days_remaining} dias"
    elif days_remaining < 15:
        score = 0.7
        factor = f"Prazo próximo do vencimento ({days_remaining} dias restantes)"
    elif days_remaining < 30:
        score = 0.4
        factor = ""
    else:
        score = max(0.0, 0.3 - (days_remaining / 200))
        factor = ""

    return min(score, 1.0), factor


def calculate_complexity_score(service_type: str) -> Tuple[float, str]:
    """Calcula o score de complexidade do serviço."""
    complexity = SERVICE_COMPLEXITY.get(service_type, 0.5)

    if complexity >= 0.8:
        factor = f"Projeto de alta complexidade (tipo: {service_type})"
    else:
        factor = ""

    return complexity, factor


def calculate_historical_delay_score(service_type: str, all_projects: list) -> Tuple[float, str]:
    """Calcula o score baseado no histórico de atrasos em serviços semelhantes."""
    similar_projects = [p for p in all_projects if p.get("service_type") == service_type and p.get("status") == "Finalizado"]

    if not similar_projects:
        return 0.3, ""  # Score neutro quando não há histórico

    delayed_count = sum(1 for p in similar_projects if p.get("actual_end_date") and p.get("expected_end_date") and p["actual_end_date"] > p["expected_end_date"])
    delay_rate = delayed_count / len(similar_projects)

    if delay_rate > 0.5:
        factor = f"Histórico de atraso em {delay_rate*100:.0f}% dos projetos de {service_type}"
    else:
        factor = ""

    return min(delay_rate, 1.0), factor


def calculate_priority_score(priority: str) -> Tuple[float, str]:
    """Calcula o score baseado na prioridade."""
    score = PRIORITY_RISK.get(priority, 0.4)
    factor = ""
    return score, factor


def calculate_risk(project: dict, all_projects: list = None, stage_history: list = None) -> dict:
    """
    Calcula o risco total de atraso de um projeto.

    Retorna:
        dict com risk_score (0-100), risk_level, risk_factors
    """
    if all_projects is None:
        all_projects = []
    if stage_history is None:
        stage_history = []

    factors = []

    # 1. Estagnação
    stag_score, stag_factor = calculate_stagnation_score(
        project["current_stage"],
        project["start_date"] if isinstance(project["start_date"], date) else date.fromisoformat(str(project["start_date"])),
        stage_history
    )
    if stag_factor:
        factors.append(stag_factor)

    # 2. Desvio de custo
    cost_score, cost_factor = calculate_cost_overrun_score(
        project.get("estimated_cost", 0),
        project.get("actual_cost", 0)
    )
    if cost_factor:
        factors.append(cost_factor)

    # 3. Proximidade do prazo
    deadline_score, deadline_factor = calculate_deadline_proximity_score(
        project["expected_end_date"] if isinstance(project["expected_end_date"], date) else date.fromisoformat(str(project["expected_end_date"])),
        project["current_stage"]
    )
    if deadline_factor:
        factors.append(deadline_factor)

    # 4. Complexidade
    complex_score, complex_factor = calculate_complexity_score(project["service_type"])
    if complex_factor:
        factors.append(complex_factor)

    # 5. Histórico
    hist_score, hist_factor = calculate_historical_delay_score(project["service_type"], all_projects)
    if hist_factor:
        factors.append(hist_factor)

    # 6. Prioridade
    prio_score, prio_factor = calculate_priority_score(project.get("priority", "Média"))
    if prio_factor:
        factors.append(prio_factor)

    # Cálculo do score ponderado
    weighted_score = (
        WEIGHTS["stagnation"] * stag_score +
        WEIGHTS["cost_overrun"] * cost_score +
        WEIGHTS["deadline_proximity"] * deadline_score +
        WEIGHTS["complexity"] * complex_score +
        WEIGHTS["historical_delay"] * hist_score +
        WEIGHTS["priority"] * prio_score
    )

    # Converter para percentual (0-100)
    risk_percentage = round(weighted_score * 100, 1)

    # Determinar nível de risco
    if risk_percentage >= 65:
        risk_level = "Alto"
    elif risk_percentage >= 35:
        risk_level = "Médio"
    else:
        risk_level = "Baixo"

    # Calcular dias de atraso
    expected_end = project["expected_end_date"] if isinstance(project["expected_end_date"], date) else date.fromisoformat(str(project["expected_end_date"]))
    if project["current_stage"] != "Finalizado":
        days_delayed = max(0, (date.today() - expected_end).days)
    else:
        actual_end = project.get("actual_end_date")
        if actual_end:
            actual_end = actual_end if isinstance(actual_end, date) else date.fromisoformat(str(actual_end))
            days_delayed = max(0, (actual_end - expected_end).days)
        else:
            days_delayed = 0

    # Calcular overrun de custo
    estimated = project.get("estimated_cost", 0)
    actual = project.get("actual_cost", 0)
    cost_overrun_pct = round(((actual - estimated) / max(estimated, 1)) * 100, 1) if estimated > 0 else 0.0

    if not factors:
        factors.append("Nenhum fator de risco significativo identificado")

    return {
        "risk_score": risk_percentage,
        "risk_level": risk_level,
        "risk_factors": factors,
        "days_delayed": days_delayed,
        "cost_overrun_pct": cost_overrun_pct,
    }
