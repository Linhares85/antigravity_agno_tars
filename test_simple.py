"""
Agente de teste mínimo para diagnóstico
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground

# Agente simples sem ferramentas
test_agent = Agent(
    name="Test Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions=["Você é um assistente de teste. Responda de forma breve."],
    markdown=True,
)

# Playground
playground = Playground(agents=[test_agent])
app = playground.get_app()

if __name__ == "__main__":
    print("Iniciando servidor de teste em http://0.0.0.0:7777")
    playground.serve("test_simple:app", reload=True, host="0.0.0.0", port=7777)
