"""
TARS - Sistema Multi-Agentes para Verticalização da Força de Trabalho
=====================================================================

Sistema baseado no framework Agno para gerenciamento de agentes especializados.
Acesse o playground em: https://os.agno.com (conectar em localhost:8000)
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# Instruções do Sistema TARS
TARS_INSTRUCTIONS = """
Você é TARS, um sistema avançado de inteligência artificial projetado para 
otimizar e verticalizar a força de trabalho empresarial.

## Suas Capacidades:
1. **Análise de Processos**: Identificar gargalos e oportunidades de melhoria
2. **Gestão de Tarefas**: Organizar, priorizar e delegar atividades
3. **Automação**: Sugerir automações para tarefas repetitivas
4. **Relatórios**: Gerar insights sobre produtividade e eficiência

## Diretrizes:
- Seja objetivo e profissional
- Forneça respostas baseadas em dados quando possível
- Sugira melhorias de forma proativa
- Mantenha confidencialidade sobre informações da empresa
- Fale em português brasileiro

## Tom de Comunicação:
Profissional, mas acessível. Como um consultor sênior de gestão.
"""

# Configuração do Agente TARS Principal
tars_agent = Agent(
    name="TARS",
    model=OpenAIChat(id="gpt-4o"),
    db=SqliteDb(db_file="tars_memory.db"),
    instructions=TARS_INSTRUCTIONS,
    add_history_to_context=True,
    num_history_responses=10,
    markdown=True,
    show_tool_calls=True,
    debug_mode=False,
)

# Configuração do AgentOS (servidor para o playground)
agent_os = AgentOS(
    agents=[tars_agent],
    name="TARS OS",
    description="Sistema de Verticalização da Força de Trabalho",
)

# Aplicação FastAPI
app = agent_os.get_app()

if __name__ == "__main__":
    print("=" * 60)
    print("  TARS - Sistema de Agentes para Força de Trabalho")
    print("=" * 60)
    print()
    print("  Iniciando servidor em: http://localhost:8000")
    print("  Documentação API: http://localhost:8000/docs")
    print()
    print("  Para conectar ao playground:")
    print("  1. Acesse https://os.agno.com")
    print("  2. Clique em 'Add new OS' → 'Local'")
    print("  3. Insira: http://localhost:8000")
    print()
    print("=" * 60)
    
    agent_os.serve(app="tars_agent:app", reload=True)
