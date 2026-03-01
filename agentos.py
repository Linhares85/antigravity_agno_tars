"""
TARS - Sistema Multi-Agentes para Verticalização da Força de Trabalho
=====================================================================

Sistema baseado no framework Agno v2 para gerenciamento de agentes especializados.

Para acessar o playground (Agent UI):
1. Execute: python agentos.py
2. Servidor inicia em: http://localhost:7777
3. Use o Agent UI local ou conecte via app.agno.com
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from supabase_tools import SupabaseTools
from knowledge_base import VectorSearchTools

# Caminho do banco de dados para armazenar sessões
AGENT_STORAGE = "tmp/agents.db"

# =============================================================================
# AGENTE TARS PRINCIPAL - Gestão e Estratégia
# =============================================================================
tars_agent = Agent(
    name="TARS - Gestão",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Você é TARS, um sistema avançado de IA para otimizar a força de trabalho empresarial.",
        "Analise processos, identifique gargalos e sugira melhorias.",
        "Seja objetivo, profissional e fale em português brasileiro.",
        "Forneça respostas baseadas em dados quando possível.",
        "Sempre inclua fontes quando pesquisar informações.",
    ],
    db=SqliteDb(db_file=AGENT_STORAGE),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=10,
    markdown=True,
)

# =============================================================================
# AGENTE DE PESQUISA - Análise de Mercado e Tendências
# =============================================================================
research_agent = Agent(
    name="TARS - Pesquisa",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Você é o módulo de pesquisa do TARS.",
        "Pesquise tendências de mercado, concorrentes e inovações.",
        "Sempre use tabelas para apresentar dados comparativos.",
        "Inclua fontes e datas nas informações.",
        "Fale em português brasileiro.",
    ],
    db=SqliteDb(db_file=AGENT_STORAGE),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# =============================================================================
# AGENTE DE PRODUTIVIDADE - Tarefas e Organização
# =============================================================================
productivity_agent = Agent(
    name="TARS - Produtividade",
    model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Você é o módulo de produtividade do TARS.",
        "Ajude a organizar tarefas, priorizar atividades e criar cronogramas.",
        "Sugira técnicas de produtividade como Pomodoro, GTD, Kanban.",
        "Forneça templates e checklists quando apropriado.",
        "Fale em português brasileiro.",
    ],
    db=SqliteDb(db_file=AGENT_STORAGE),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# =============================================================================
# AGENTE SUPERVISOR - Visão Global e Delegação
# =============================================================================
supervisor_agent = Agent(
    name="TARS - Supervisor",
    model=OpenAIChat(id="gpt-4o"),
    team=[tars_agent, research_agent, productivity_agent],
    tools=[DuckDuckGoTools(), SupabaseTools(), VectorSearchTools()],
    instructions=[
        "Você é o Agente Supervisor do sistema TARS.",
        "Você tem visão global da arquitetura e acesso TOTAL ao banco de dados.",
        "Use 'SupabaseTools' para consultar tabelas tradicionais (SQL).",
        "Use 'VectorSearchTools' para consultar a base de conhecimento (Vector BD - WaSeller e FlowSeller).",
        "Você pode e deve delegar tarefas para os especialistas da sua equipe (Gestão, Pesquisa e Produtividade).",
        "Sempre determine qual agente é o mais adequado para resolver a solicitação do usuário antes de delegar.",
        "Fale em português brasileiro.",
    ],
    db=SqliteDb(db_file=AGENT_STORAGE),
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=10,
    markdown=True,
)

# =============================================================================
# CONFIGURAÇÃO DO AGENTOS
# =============================================================================
agent_os = AgentOS(agents=[supervisor_agent, tars_agent, research_agent, productivity_agent])

app = agent_os.get_app()

if __name__ == "__main__":
    print("=" * 60)
    print("  TARS - Sistema de Agentes para Força de Trabalho")
    print("=" * 60)
    print()
    print("  Servidor iniciando em: http://localhost:7777")
    print()
    print("  Para acessar o Agent UI:")
    print("  1. Clone: git clone https://github.com/agno-agi/agent-ui.git")
    print("  2. Execute: cd agent-ui && npm install && npm run dev")
    print("  3. Acesse: http://localhost:3000")
    print("  4. Conecte em: localhost:7777")
    print()
    print("  Ou acesse: https://app.agno.com/playground")
    print("  E conecte em: localhost:7777")
    print()
    print("  Agentes disponíveis:")
    print("  • TARS - Supervisor: Visão global e delegação p/ equipe")
    print("  • TARS - Gestão: Análise e otimização de processos")
    print("  • TARS - Pesquisa: Tendências e análise de mercado")
    print("  • TARS - Produtividade: Tarefas e organização")
    print()
    print("=" * 60)
    
    agent_os.serve("agentos:app", reload=True)
