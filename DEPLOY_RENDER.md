# Guia de Deploy no Render.com

Este guia explica como publicar o **CAW Ops Intelligence** gratuitamente no Render.com. O projeto foi reestruturado para um deploy unificado: o backend (FastAPI) agora serve o frontend (Vue 3) compilado, exigindo apenas um único serviço no Render.

## Pré-requisitos

1. Uma conta no [GitHub](https://github.com/).
2. Uma conta no [Render.com](https://render.com/) (vinculada ao seu GitHub).

## Passo 1: Subir o código para o GitHub

1. Extraia o arquivo `.zip` atualizado que você recebeu.
2. Crie um novo repositório público ou privado no seu GitHub (ex: `caw-ops-intelligence`).
3. Abra o terminal na pasta extraída e execute:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/caw-ops-intelligence.git
git push -u origin main
```

*(Nota: O arquivo `.gitignore` já está configurado para não subir pastas pesadas como `node_modules` ou `venv`)*.

## Passo 2: Deploy Automático no Render (Recomendado)

O projeto já inclui um arquivo `render.yaml` na raiz, o que torna o deploy praticamente automático (Infrastructure as Code).

1. Acesse o painel do [Render.com](https://dashboard.render.com/).
2. Clique no botão **New +** e selecione **Blueprint**.
3. Conecte o seu repositório do GitHub (`caw-ops-intelligence`).
4. O Render lerá automaticamente o arquivo `render.yaml` e configurará o serviço Web (Docker).
5. Clique em **Apply** no final da página.

O Render começará a construir a imagem Docker (isso pode levar de 3 a 5 minutos). Quando terminar, ele fornecerá uma URL pública (ex: `https://caw-ops-intelligence.onrender.com`).

## Passo 3: Deploy Manual no Render (Alternativa)

Se preferir não usar o Blueprint, você pode criar o serviço manualmente:

1. No painel do Render, clique em **New +** e selecione **Web Service**.
2. Escolha **Build and deploy from a Git repository** e conecte seu repositório.
3. Preencha as configurações:
   - **Name:** `caw-ops-intelligence`
   - **Region:** Escolha a mais próxima (ex: Ohio ou Frankfurt)
   - **Branch:** `main`
   - **Runtime:** `Docker` (O Render detectará o `Dockerfile` automaticamente)
   - **Instance Type:** `Free`
4. Em **Advanced**, adicione as seguintes variáveis de ambiente (Environment Variables):
   - `PORT` = `8000`
   - `JWT_SECRET_KEY` = *(clique em "Generate" para criar uma chave segura)*
5. Clique em **Create Web Service**.

## Como funciona a arquitetura de Deploy?

Para simplificar a hospedagem gratuita, utilizamos um **Build Multi-stage no Docker**:

1. **Stage 1 (Node.js):** O Docker baixa as dependências do frontend (`npm install --legacy-peer-deps`) e compila o Vue 3 para arquivos estáticos HTML/CSS/JS na pasta `dist`.
2. **Stage 2 (Python):** O Docker instala o FastAPI, copia o backend, e depois copia a pasta `dist` gerada no Stage 1.
3. **Execução:** O script `seed.py` roda automaticamente para popular o banco de dados SQLite com os 120 projetos fictícios. Em seguida, o Uvicorn inicia o servidor na porta 8000.
4. **Roteamento:** O FastAPI foi configurado para responder rotas `/api/*` normalmente, e para qualquer outra rota, ele serve o `index.html` do Vue 3, permitindo que o Vue Router gerencie a navegação da SPA (Single Page Application).

## Acesso ao Sistema

Após o deploy concluído, acesse a URL fornecida pelo Render. As credenciais padrão geradas pelo `seed.py` são:

- **Usuário:** `admin`
- **Senha:** `caw2024`

*(Nota: Como o Render Free desliga a máquina após 15 minutos de inatividade, o primeiro acesso do dia pode demorar cerca de 50 segundos para carregar enquanto o servidor "acorda". O banco de dados SQLite é recriado a cada deploy, o que é ideal para demonstrações de portfólio).*
