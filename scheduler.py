import os
import time
from apscheduler.schedulers.background import BackgroundScheduler
from agno.agent import Agent
from playground import research_agent

def run_daily_market_research():
    """
    Função exemplo que aciona o Agente de Pesquisa automaticamente.
    Esta função roda em background e pode salvar os resultados no Supabase 
    ou enviar por email/webhook de acordo com sua necessidade futura.
    """
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Iniciando tarefa agendada: Pesquisa de Mercado...")
    
    try:
        # Acionando o agente de pesquisa para executar uma tarefa pré-definida
        resposta = research_agent.run("Faça um resumo rápido das 3 maiores novidades sobre Inteligência Artificial nas últimas 24 horas.")
        print("Resultado da Pesquisa Agendada: Sucesso!")
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Tarefa agendada concluída.\n")
    except Exception as e:
        print(f"Erro ao executar tarefa agendada: {e}")

def start_scheduler():
    """
    Inicializa o agendador de tarefas em background.
    """
    scheduler = BackgroundScheduler()
    
    # Exemplos de Agendamentos:
    
    # 1. Roda a cada 60 minutos (ideal para testes)
    # scheduler.add_job(run_daily_market_research, 'interval', minutes=60)
    
    # 2. Roda todos os dias às 08:00 (cron job real)
    scheduler.add_job(run_daily_market_research, 'cron', hour=8, minute=0)
    
    scheduler.start()
    print("⏳ Agendador de tarefas iniciado (APScheduler).")
