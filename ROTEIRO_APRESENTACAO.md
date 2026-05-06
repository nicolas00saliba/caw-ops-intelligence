# Roteiro de Apresentação — CAW Ops Intelligence

Este roteiro foi criado para guiar a sua demonstração do projeto durante a entrevista para a vaga de Desenvolvimento de Sistemas na CAW Telecom e Energia.

## 1. Introdução (O "Elevator Pitch")
*Duração sugerida: 2 minutos*

**O que falar:**
- "Olá a todos. Para esta entrevista, decidi ir além de um teste técnico padrão. Eu pesquisei sobre a CAW Telecom e Energia, entendi a área de atuação de vocês em infraestrutura, e construí um protótipo de sistema corporativo chamado **CAW Ops Intelligence**."
- "O objetivo deste sistema não é ser apenas um CRUD (Cadastro, Leitura, Atualização e Exclusão), mas sim uma ferramenta de **inteligência operacional**. Ele foi pensado para resolver um problema real: como gerenciar dezenas de projetos simultâneos (torres, fundações, subestações) e identificar riscos de atraso antes que eles aconteçam."
- "A mensagem central que quero passar com este projeto é: **Eu não apenas desenvolvo telas e APIs; eu consigo entender o negócio, transformar operação em sistema e usar dados para apoiar decisões melhores.**"

## 2. Demonstração da Tela de Login
*Duração sugerida: 1 minuto*

**Ação:** Mostre a tela de login.
**O que falar:**
- "A interface foi construída com Vue 3 e Vuetify, focando em um design limpo e corporativo. Utilizei a identidade visual oficial da CAW."
- "O backend foi feito em Python com FastAPI, garantindo alta performance. A autenticação já utiliza tokens JWT reais."
- *Faça o login com usuário `admin` e senha `caw2024`.*

## 3. Demonstração do Dashboard Gerencial
*Duração sugerida: 3 minutos*

**Ação:** Navegue pelo Dashboard, passando o mouse sobre os gráficos.
**O que falar:**
- "Ao entrar, o gestor tem uma visão consolidada da operação. Para esta demonstração, criei um script em Python que gerou **120 projetos fictícios**, mas com dados estatisticamente realistas para o setor."
- "Temos os indicadores críticos no topo: total de projetos, quantos estão em andamento, quantos estão atrasados e, mais importante, quantos apresentam **risco alto**."
- "Os gráficos (feitos com ApexCharts) mostram a distribuição por tipo de serviço (Torres, Fundações, etc.), o tempo médio que cada etapa costuma levar, e um comparativo crucial: **Custo Previsto vs. Custo Realizado**."

## 4. Demonstração da Lista de Projetos
*Duração sugerida: 2 minutos*

**Ação:** Vá para a aba "Projetos". Use os filtros (ex: filtre por Status "Atrasado" ou Risco "Alto").
**O que falar:**
- "Aqui temos a gestão operacional do dia a dia. A tabela permite filtrar rapidamente os projetos."
- "Notem que além do status tradicional, temos a coluna de **Risco**. Isso é calculado dinamicamente pelo backend."

## 5. Demonstração do Detalhe do Projeto
*Duração sugerida: 2 minutos*

**Ação:** Clique em "Visualizar" em um projeto que esteja com Risco Alto ou Atrasado.
**O que falar:**
- "Entrando no detalhe de um projeto, o gestor não vê apenas dados cadastrais. Ele vê **inteligência**."
- "Temos indicadores visuais de desvio de custo (se o realizado passou do estimado, a barra fica vermelha) e de prazo."
- "Temos também a linha do tempo das etapas, mostrando exatamente onde o projeto está e quanto tempo ficou em cada fase."

## 6. O Diferencial: Análise de Risco Operacional
*Duração sugerida: 3 minutos*

**Ação:** Vá para a aba "Análise de Risco".
**O que falar:**
- "Este é o coração da inteligência do sistema. Eu desenvolvi no backend (FastAPI) um **Motor de Risco**."
- "Ele não apenas diz que o projeto está atrasado, ele **prevê a probabilidade de atraso**. O algoritmo calcula um score de 0 a 100% baseado em 6 fatores ponderados: tempo estagnado na etapa atual, proximidade do prazo final, desvio de custo, complexidade do serviço, histórico e prioridade."
- "O sistema lista os projetos mais críticos no topo e **explica o porquê** (ex: 'Etapa Produção parada há 45 dias', 'Custo 30% acima do previsto'). Isso transforma dados em ação."

## 7. Arquitetura e Código
*Duração sugerida: 2 minutos*

**Ação:** Mostre rapidamente a estrutura de pastas no seu editor de código (VS Code).
**O que falar:**
- "O código foi estruturado com boas práticas. O backend usa FastAPI com SQLAlchemy e Pydantic, totalmente tipado e pronto para migrar de SQLite para PostgreSQL."
- "O frontend usa Vue 3 com Composition API, componentizado e modular."
- "Tudo está documentado no README, pronto para rodar com poucos comandos."

## 8. Conclusão e Próximos Passos
*Duração sugerida: 1 minuto*

**O que falar:**
- "Como próximos passos para um sistema em produção, eu implementaria a integração com o ERP da empresa, migração para nuvem (AWS/Azure) e, no futuro, substituiria o motor de regras atual por um modelo de Machine Learning treinado com os dados históricos reais da CAW."
- "Agradeço o tempo de vocês. Estou à disposição para dúvidas técnicas sobre o código ou sobre as decisões de arquitetura que tomei."
