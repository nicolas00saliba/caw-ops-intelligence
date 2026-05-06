"""
CAW Ops Intelligence - Seed de Dados Fictícios Realistas

Gera entre 80 e 150 projetos fictícios compatíveis com a atuação da CAW Telecom e Energia.
"""

import random
from datetime import date, timedelta
from database import engine, SessionLocal, Base
from models import Project, StageHistory, User
from passlib.hash import bcrypt
from risk_engine import calculate_risk

random.seed(42)

# Dados base para geração
SERVICE_TYPES = [
    "Torre Telecom",
    "Fundação",
    "Poste",
    "Reforço Estrutural",
    "Subestação",
    "Estrutura Metálica",
    "Manutenção",
]

STAGES = [
    "Orçamento",
    "Projeto técnico",
    "Produção",
    "Pré-montagem",
    "Expedição",
    "Instalação",
    "Finalizado",
]

STATUSES = ["Em andamento", "Finalizado", "Atrasado", "Pausado"]

PRIORITIES = ["Crítica", "Alta", "Média", "Baixa"]

CITIES_STATES = [
    ("Campo Largo", "PR"),
    ("Curitiba", "PR"),
    ("Londrina", "PR"),
    ("Maringá", "PR"),
    ("Ponta Grossa", "PR"),
    ("Cascavel", "PR"),
    ("São José dos Pinhais", "PR"),
    ("Colombo", "PR"),
    ("Guarapuava", "PR"),
    ("Paranaguá", "PR"),
    ("Foz do Iguaçu", "PR"),
    ("Joinville", "SC"),
    ("Florianópolis", "SC"),
    ("Blumenau", "SC"),
    ("Chapecó", "SC"),
    ("Criciúma", "SC"),
    ("Porto Alegre", "RS"),
    ("Caxias do Sul", "RS"),
    ("Santa Maria", "RS"),
    ("São Paulo", "SP"),
    ("Campinas", "SP"),
    ("Sorocaba", "SP"),
    ("Ribeirão Preto", "SP"),
]

CLIENTS = [
    "Vivo Telefônica",
    "TIM Brasil",
    "Claro S.A.",
    "Oi S.A.",
    "American Tower",
    "SBA Communications",
    "IHS Towers",
    "Highline do Brasil",
    "Phoenix Tower",
    "Copel Telecom",
    "Energisa",
    "CPFL Energia",
    "Neoenergia",
    "Enel Brasil",
    "Cemig",
    "Prefeitura Municipal",
    "Governo do Estado",
    "Winity Telecom",
    "Algar Telecom",
    "Brisanet",
]

RESPONSIBLES = [
    "Carlos Eduardo Silva",
    "Ana Paula Ferreira",
    "Roberto Mendes",
    "Juliana Costa",
    "Marcos Oliveira",
    "Fernanda Souza",
    "Ricardo Almeida",
    "Patrícia Santos",
    "Lucas Pereira",
    "Camila Rodrigues",
    "André Nascimento",
    "Beatriz Lima",
]

PROJECT_NAMES = {
    "Torre Telecom": [
        "Instalação de Torre Telecom",
        "Montagem de Torre Autoportante",
        "Torre Estaiada para Cobertura 5G",
        "Implantação de Site Telecom",
        "Torre Metálica para Operadora",
        "Instalação de Torre Rooftop",
        "Torre de Telecomunicações Rural",
        "Site Telecom Greenfield",
    ],
    "Fundação": [
        "Projeto de Fundação para Torre",
        "Fundação em Estaca Raiz",
        "Fundação Tipo Sapata para Site",
        "Base de Concreto para Torre",
        "Fundação Profunda para Subestação",
        "Projeto Geotécnico e Fundação",
    ],
    "Poste": [
        "Instalação de Poste Metálico",
        "Poste de Concreto para Telecom",
        "Substituição de Poste Danificado",
        "Poste para Antena Small Cell",
        "Poste Decorativo com Antena",
    ],
    "Reforço Estrutural": [
        "Reforço Estrutural de Site",
        "Reforço de Torre Existente",
        "Adequação Estrutural para 5G",
        "Reforço Metálico de Plataforma",
        "Reforço de Base de Torre",
        "Retrofit Estrutural de Site",
    ],
    "Subestação": [
        "Subestação Metálica",
        "Subestação Compacta",
        "Subestação de Energia para Site",
        "Montagem de Subestação Abrigada",
        "Subestação para Parque Eólico",
    ],
    "Estrutura Metálica": [
        "Estrutura Metálica Industrial",
        "Galpão Metálico para Equipamentos",
        "Cobertura Metálica para Subestação",
        "Estrutura de Aço para Data Center",
        "Plataforma Metálica Elevada",
        "Mezanino Metálico Industrial",
    ],
    "Manutenção": [
        "Manutenção Preventiva de Torre",
        "Manutenção Corretiva de Site",
        "Inspeção e Manutenção de Estrutura",
        "Manutenção de Pintura Anticorrosiva",
        "Revisão Estrutural Periódica",
        "Manutenção de Sistema de Aterramento",
    ],
}


def generate_projects(num_projects: int = 120):
    """Gera uma lista de projetos fictícios realistas."""
    projects = []

    today = date.today()

    for i in range(num_projects):
        service_type = random.choice(SERVICE_TYPES)
        city, state = random.choice(CITIES_STATES)
        client = random.choice(CLIENTS)
        responsible = random.choice(RESPONSIBLES)
        priority = random.choices(PRIORITIES, weights=[10, 25, 45, 20])[0]

        # Nome do projeto
        name_options = PROJECT_NAMES[service_type]
        base_name = random.choice(name_options)
        project_name = f"{base_name} — {city}/{state}"

        # Datas
        start_offset = random.randint(-180, -10)
        start_date = today + timedelta(days=start_offset)

        duration = random.randint(30, 180)
        expected_end_date = start_date + timedelta(days=duration)

        # Status e etapa
        if expected_end_date < today:
            # Projeto deveria ter terminado
            if random.random() < 0.6:
                status = "Finalizado"
                current_stage = "Finalizado"
                actual_end_date = expected_end_date + timedelta(days=random.randint(-10, 30))
            else:
                status = "Atrasado"
                current_stage = random.choice(STAGES[2:6])
                actual_end_date = None
        elif start_date < today:
            # Projeto em andamento
            elapsed_ratio = (today - start_date).days / max(duration, 1)
            stage_index = min(int(elapsed_ratio * 6), 5)

            if random.random() < 0.1:
                status = "Pausado"
                current_stage = STAGES[max(1, stage_index - 1)]
            elif random.random() < 0.15:
                status = "Atrasado"
                current_stage = STAGES[max(0, stage_index - 1)]
            else:
                status = "Em andamento"
                current_stage = STAGES[stage_index]
            actual_end_date = None
        else:
            status = "Em andamento"
            current_stage = "Orçamento"
            actual_end_date = None

        # Custos
        base_costs = {
            "Torre Telecom": (150000, 500000),
            "Fundação": (80000, 250000),
            "Poste": (30000, 120000),
            "Reforço Estrutural": (60000, 200000),
            "Subestação": (200000, 800000),
            "Estrutura Metálica": (120000, 450000),
            "Manutenção": (20000, 80000),
        }

        cost_range = base_costs[service_type]
        estimated_cost = round(random.uniform(*cost_range), 2)

        # Custo realizado
        if status == "Finalizado":
            cost_variation = random.uniform(0.85, 1.35)
            actual_cost = round(estimated_cost * cost_variation, 2)
        elif status == "Atrasado":
            cost_variation = random.uniform(0.7, 1.45)
            actual_cost = round(estimated_cost * cost_variation, 2)
        elif current_stage == "Orçamento":
            actual_cost = 0.0
        else:
            progress = STAGES.index(current_stage) / 6
            cost_variation = random.uniform(0.8, 1.2)
            actual_cost = round(estimated_cost * progress * cost_variation, 2)

        # Observações técnicas
        notes_options = [
            "Solo com boa capacidade de suporte. Fundação direta viável.",
            "Necessário estudo geotécnico complementar.",
            "Acesso ao local dificultado por estrada não pavimentada.",
            "Cliente solicitou alteração de escopo durante a produção.",
            "Condições climáticas adversas atrasaram a instalação.",
            "Material importado com prazo de entrega estendido.",
            "Equipe reduzida por conta de outro projeto prioritário.",
            "Aprovação ambiental pendente junto ao órgão municipal.",
            "Projeto executivo revisado após vistoria técnica.",
            "Terreno com declividade acentuada, requer terraplenagem.",
            "Interferência com rede de distribuição existente.",
            "Licenciamento junto à ANATEL em andamento.",
            "Fornecedor de aço com atraso na entrega.",
            "Necessário reforço na base existente antes da montagem.",
            "Projeto dentro do cronograma previsto.",
            None,
            None,
            None,
        ]

        technical_notes = random.choice(notes_options)

        projects.append({
            "name": project_name,
            "client": client,
            "service_type": service_type,
            "city": city,
            "state": state,
            "responsible": responsible,
            "current_stage": current_stage,
            "status": status,
            "priority": priority,
            "start_date": start_date,
            "expected_end_date": expected_end_date,
            "actual_end_date": actual_end_date,
            "estimated_cost": estimated_cost,
            "actual_cost": actual_cost,
            "technical_notes": technical_notes,
        })

    return projects


def generate_stage_history(project: dict, project_id: int):
    """Gera histórico de etapas para um projeto."""
    history = []
    current_stage = project["current_stage"]
    start_date = project["start_date"]

    current_date = start_date
    for stage in STAGES:
        if stage == current_stage and current_stage != "Finalizado":
            # Etapa atual - sem data de conclusão
            history.append({
                "project_id": project_id,
                "stage": stage,
                "started_at": current_date,
                "completed_at": None,
                "days_in_stage": (date.today() - current_date).days,
                "notes": None,
            })
            break
        else:
            days_in_stage = random.randint(5, 35)
            completed_date = current_date + timedelta(days=days_in_stage)
            history.append({
                "project_id": project_id,
                "stage": stage,
                "started_at": current_date,
                "completed_at": completed_date,
                "days_in_stage": days_in_stage,
                "notes": None,
            })
            current_date = completed_date

        if stage == current_stage:
            break

    return history


def seed_database():
    """Popula o banco de dados com dados fictícios."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Criar usuário demo
        demo_user = User(
            username="admin",
            hashed_password=bcrypt.hash("caw2024"),
            full_name="Administrador CAW",
            role="admin"
        )
        db.add(demo_user)

        operator_user = User(
            username="operador",
            hashed_password=bcrypt.hash("caw2024"),
            full_name="Operador de Projetos",
            role="operator"
        )
        db.add(operator_user)

        # Gerar projetos
        projects_data = generate_projects(120)

        # Calcular risco para cada projeto
        all_projects_for_risk = [
            {**p, "start_date": p["start_date"], "expected_end_date": p["expected_end_date"]}
            for p in projects_data
        ]

        for i, proj_data in enumerate(projects_data):
            # Calcular risco
            risk_result = calculate_risk(proj_data, all_projects_for_risk, [])

            project = Project(
                name=proj_data["name"],
                client=proj_data["client"],
                service_type=proj_data["service_type"],
                city=proj_data["city"],
                state=proj_data["state"],
                responsible=proj_data["responsible"],
                current_stage=proj_data["current_stage"],
                status=proj_data["status"],
                priority=proj_data["priority"],
                start_date=proj_data["start_date"],
                expected_end_date=proj_data["expected_end_date"],
                actual_end_date=proj_data["actual_end_date"],
                estimated_cost=proj_data["estimated_cost"],
                actual_cost=proj_data["actual_cost"],
                technical_notes=proj_data["technical_notes"],
                risk_score=risk_result["risk_score"],
                risk_level=risk_result["risk_level"],
                risk_factors="|".join(risk_result["risk_factors"]),
            )
            db.add(project)
            db.flush()

            # Gerar histórico de etapas
            stage_history = generate_stage_history(proj_data, project.id)
            for sh in stage_history:
                stage_record = StageHistory(
                    project_id=sh["project_id"],
                    stage=sh["stage"],
                    started_at=sh["started_at"],
                    completed_at=sh["completed_at"],
                    days_in_stage=sh["days_in_stage"],
                    notes=sh["notes"],
                )
                db.add(stage_record)

        db.commit()
        print(f"✓ Banco de dados populado com {len(projects_data)} projetos")
        print(f"✓ Usuário demo: admin / caw2024")
        print(f"✓ Usuário operador: operador / caw2024")

    except Exception as e:
        db.rollback()
        print(f"✗ Erro ao popular banco: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
