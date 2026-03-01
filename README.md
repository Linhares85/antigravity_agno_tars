# TARS - Sistema de Agentes para Força de Trabalho

Sistema multi-agentes baseado no framework Agno para verticalização da força de trabalho empresarial.

## Agentes Disponíveis

| Agente | Função |
|--------|--------|
| **TARS - Gestão** | Análise e otimização de processos empresariais |
| **TARS - Pesquisa** | Tendências de mercado e análise competitiva |
| **TARS - Produtividade** | Organização de tarefas e técnicas de produtividade |

## Configuração

### 1. Ativar o Ambiente Virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Configurar Chave da OpenAI

```powershell
$env:OPENAI_API_KEY = "sk-sua-chave-aqui"
```

Ou crie um arquivo `.env`:
```
OPENAI_API_KEY=sk-sua-chave-aqui
```

## Executar o Sistema

```powershell
python playground.py
```

O servidor iniciará em `http://localhost:7777`

## Acessar o Playground

1. Acesse **[app.agno.com/playground](https://app.agno.com/playground)**
2. Faça login ou crie uma conta gratuita
3. Clique em **"Add Endpoint"**
4. Insira: `localhost:7777/v1`
5. Conecte e selecione um agente TARS

## Estrutura do Projeto

```
antigravity_project/
├── playground.py      # Servidor com agentes TARS
├── tmp/
│   └── tars_agents.db # Banco de dados de sessões
├── .env               # Variáveis de ambiente (criar)
├── .env.example       # Template de configuração
└── README.md          # Este arquivo
```
