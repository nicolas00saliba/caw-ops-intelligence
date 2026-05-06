# CAW Ops Intelligence

<div align="center">
  <img src="caw-logo.png" alt="CAW Telecom e Energia" width="250" />
</div>

<br />

O **CAW Ops Intelligence** é um protótipo de sistema corporativo de gestão operacional e inteligência de risco, desenvolvido especificamente para o contexto da **CAW Telecom e Energia**. 

Este projeto foi criado para demonstrar habilidades em desenvolvimento Full-Stack (Vue 3 + FastAPI), arquitetura de software, análise de dados e entendimento de regras de negócio voltadas para infraestrutura de telecomunicações e energia.

## 🎯 Objetivo do Sistema

Empresas de infraestrutura gerenciam simultaneamente dezenas de projetos complexos (torres, fundações, subestações) em diferentes localidades. O objetivo deste sistema é:

1. **Centralizar a Gestão:** Substituir planilhas desconectadas por um dashboard gerencial unificado.
2. **Inteligência Preditiva:** Identificar projetos com risco de atraso *antes* que se tornem críticos, utilizando um motor de risco baseado em regras de negócio.
3. **Controle Financeiro:** Monitorar o desvio entre custo previsto e realizado em tempo real.
4. **Rastreabilidade:** Manter o histórico completo de cada etapa do projeto (Orçamento, Projeto Técnico, Produção, Pré-montagem, Expedição, Instalação).

## 🚀 Tecnologias Utilizadas

### Frontend
- **Vue 3** (Composition API)
- **Vite** (Build tool)
- **Vuetify 3** (Material Design UI Framework)
- **Vue Router** (Navegação SPA)
- **Axios** (Comunicação HTTP)
- **ApexCharts** (Visualização de dados e gráficos interativos)

### Backend
- **Python 3.11**
- **FastAPI** (Framework web de alta performance)
- **SQLAlchemy** (ORM para banco de dados)
- **Pydantic** (Validação de dados e schemas)
- **Uvicorn** (Servidor ASGI)
- **SQLite** (Banco de dados embutido para facilitar demonstração local)

### Inteligência e Dados
- **Motor de Risco Customizado:** Algoritmo de score ponderado que avalia estagnação de etapas, proximidade de prazos, desvios de custo e complexidade do serviço.
- **Gerador de Dataset (Seed):** Script inteligente que gera 120 projetos fictícios, porém realistas, com históricos coerentes e distribuições estatísticas plausíveis para o setor.

## ⚙️ Como Executar o Projeto Localmente

O projeto está estruturado em duas pastas principais: `backend` e `frontend`.

### 1. Iniciando o Backend (FastAPI)

Abra um terminal e execute os seguintes comandos:

```bash
# Entre na pasta do backend
cd backend

# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instale as dependências
pip install -r requirements.txt

# Popule o banco de dados com dados fictícios (120 projetos)
python seed.py

# Inicie o servidor FastAPI
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará rodando em `http://localhost:8000`. A documentação interativa da API (Swagger) pode ser acessada em `http://localhost:8000/docs`.

### 2. Iniciando o Frontend (Vue 3)

Abra um **novo terminal** e execute:

```bash
# Entre na pasta do frontend
cd frontend

# Instale as dependências (use npm, yarn ou pnpm)
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará rodando em `http://localhost:3000` (ou a porta indicada no terminal).

### 3. Acesso ao Sistema

Acesse a URL do frontend no seu navegador. Na tela de login, utilize as seguintes credenciais de demonstração:

- **Usuário:** `admin`
- **Senha:** `caw2024`

## 📊 Funcionalidades Principais

- **Dashboard Gerencial:** Visão consolidada com 6 gráficos interativos e cards de indicadores críticos.
- **Gestão de Projetos:** Tabela completa com filtros avançados, paginação e indicadores visuais de status e risco.
- **Análise de Risco Operacional:** Página dedicada que lista os projetos ordenados por probabilidade de atraso, explicando detalhadamente os fatores que compõem o score de risco.
- **Detalhe do Projeto:** Visão aprofundada de um projeto específico, incluindo linha do tempo de etapas, indicadores de custo/prazo e histórico completo.
- **Cadastro/Edição:** Formulários validados para inserção e atualização de dados operacionais.

## 🔮 Sugestões de Evolução Futura

Este projeto foi construído como um protótipo funcional, mas sua arquitetura permite escalabilidade. Sugestões para evolução em um cenário real:

1. **Integração com ERP:** Conectar via API com sistemas como SAP ou TOTVS para sincronização de custos e faturamento.
2. **Autenticação RBAC:** Implementar controle de acesso baseado em papéis (Administrador, Gerente de Projeto, Equipe de Campo).
3. **Banco de Dados em Produção:** Migrar de SQLite para PostgreSQL.
4. **Deploy em Nuvem:** Hospedar na AWS, GCP ou Azure utilizando Docker e CI/CD.
5. **Aplicativo Mobile:** Desenvolver versão mobile (React Native ou Flutter) para apontamento de etapas diretamente pelas equipes de campo.
6. **Machine Learning Avançado:** Substituir o motor de regras atual por um modelo preditivo treinado com dados históricos reais da empresa.

---

<div align="center">
  <p><i>"Eu não apenas desenvolvo telas e APIs; eu consigo entender o negócio, transformar operação em sistema e usar dados para apoiar decisões melhores."</i></p>
</div>
