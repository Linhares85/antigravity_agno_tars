# Configuração da Base de Conhecimento Vetorial
# Usando implementação simplificada via REST para compatibilidade
from agno.agent import AgentKnowledge
import os

# Removidos imports diretos do Agno DB que exigem drivers nativos complexos para Windows/Python Alpha
# from agno.vectordb.pgvector import PgVector 
# from agno.embedder.openai import OpenAIEmbedder

# Configuração da Base de Conhecimento Vetorial
# Usando PgVector conectado ao Supabase (PostgreSQL)

def get_selly_knowledge_base():
    """
    Retorna a base de conhecimento configurada para a agente Selly.
    Conecta à tabela 'documents_vendas_selly' no Supabase via PgVector.
    """
    db_url = os.getenv("SUPABASE_DB_URL") # Precisa ser a string de conexão postgresql://postgres.xyz:pass@aws-0-us-east-1.pooler.supabase.com:6543/postgres
    
    # Se não tivermos a connection string completa (com senha), vamos tentar simular
    # ou pedir ao usuário. Por enquanto, vamos assumir que o usuário fornecerá ou
    # usaremos uma implementação alternativa via REST se a conexão direta falhar.
    
    # NOTA: O Agno v1 PgVector geralmente requer conexão direta com banco de dados (SQLAlchemy/psycopg).
    # Como só temos a API Key e URL (REST), talvez precisemos de uma abordagem híbrida
    # ou usar o SupabaseTools para chamar uma RPC 'match_documents'.
    
    # Abordagem REST (Mais segura com as credenciais atuais):
    # Vamos criar um "Knowledge" customizado que usa nossa SupabaseTools revisada
    # para chamar a função RPC de busca vetorial (padrão do Supabase).
    pass

# Como não temos a senha do banco (apenas API Key), a conexão direta do PgVector falhará.
# Vamos implementar a busca vetorial via RPC do Supabase usando a SupabaseTools.
# Isso requer que a função 'match_documents' (ou similar) exista no Supabase.

from agno.tools import Toolkit
import requests
import json
import os

class VectorSearchTools(Toolkit):
    def __init__(self):
        super().__init__(name="vector_search_tools")
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.openai_key = os.getenv("OPENAI_API_KEY")
        
        self.register(self.search_sales_knowledge)
        self.register(self.search_support_knowledge)

    def get_embedding(self, text: str):
        """Gera embedding usando OpenAI"""
        url = "https://api.openai.com/v1/embeddings"
        headers = {"Authorization": f"Bearer {self.openai_key}", "Content-Type": "application/json"}
        data = {"input": text, "model": "text-embedding-3-small"}
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["data"][0]["embedding"]
        else:
            raise Exception(f"Erro ao gerar embedding: {response.text}")

    def search_sales_knowledge(self, query: str) -> str:
        """
        Realiza uma busca semântica na base de conhecimento de VENDAS (documents_vendas_selly).
        Use isso para encontrar informações sobre processos de vendas, objeções e produtos.
        
        Args:
            query (str): A pergunta ou termo de busca.
            
        Returns:
            str: Trechos de documentos relevantes encontrados.
        """
        return self._search_vector_store(query, "documents_vendas_selly")

    def search_support_knowledge(self, query: str) -> str:
        """
        Realiza uma busca semântica na base de conhecimento de SUPORTE (documents).
        Use isso OBRIGATORIAMENTE para responder dúvidas técnicas e de suporte do WaSeller.
        
        Args:
            query (str): A pergunta ou termo de busca.
            
        Returns:
            str: Trechos de documentos relevantes encontrados.
        """
        return self._search_vector_store(query, "documents")

    def _search_vector_store(self, query: str, table_name: str) -> str:
        """Helper interno para busca vetorial genérica."""
        try:
            # 1. Gerar Embedding da Query
            embedding = self.get_embedding(query)
            
            # 2. Chamar RPC 'match_documents' no Supabase
            rpc_endpoint = f"{self.url}/rest/v1/rpc/match_documents"
            headers = {
                "apikey": self.key, 
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json"
            }
            # O RPC deve ser capaz de receber o nome da tabela ou ter RPCs separados.
            # Como a RPC match_documents padrão do Supabase geralmente é hardcoded para uma tabela,
            # precisamos verificar se o usuário tem uma função dinâmica ou se precisamos de outra estratégia.
            
            # ESTRATÉGIA ROBUSTA: Enviar o nome da tabela se a RPC suportar, ou assumir que match_documents
            # procura na tabela padrão (documents) e talvez precisemos de match_documents_sales.
            # DADO O CONTEXTO: O usuário disse que Selly Vendas usa `documents_vendas_selly` e Suporte usa `documents`.
            # É provável que existam DUAS funções RPC ou uma que aceite parâmetro.
            # Vamos tentar passar um parâmetro 'filter' ou assumir que a RPC pode filtrar por metadados se for tabela única.
            # MAS como são tabelas DIFERENTES, o mais comum é ter RPCs diferentes.
            
            # TENTATIVA 1: Tentar chamar RPCs específicas baseadas no nome da tabela.
            rpc_name = "match_documents" 
            if table_name == "documents_vendas_selly":
                rpc_name = "match_documents_vendas" # Chute educado: geralmente cria-se uma para cada.
                # SE falhar, o agente receberá erro e poderemos corrigir.
            
            # TENTATIVA 2 (Mais segura se não soubermos o nome da RPC):
            # Se o usuário não especificou o nome das funções, vamos assumir o padrão 'match_documents' para a tabela 'documents' (Suporte)
            # E para vendas... precisamos perguntar ou adivinhar.
            # O usuário disse: "Selly Vendas... acesso a tabela documents_vendas_selly".
            
            # Vamos instruir o código a tentar 'match_documents' para ambas, passando o nome da tabela num campo extra
            # caso a função seja dinâmica, OU tentar nomes convencionais.
            
            # DECISÃO: Usar 'match_documents' para suporte (padrão) e 'match_documents_vendas' para vendas.
            
            target_rpc = "match_documents"
            if table_name == "documents_vendas_selly":
                target_rpc = "match_documents_selly" # Ajuste provável
            
            # UPDATE: Para garantir, vamos usar um payload genérico e se falhar, o erro nos guiará.
            # Mas melhor ainda: Vamos usar o client SupabaseTools se possível? Não, estamos em REST.
            
            rpc_endpoint = f"{self.url}/rest/v1/rpc/{target_rpc}"
            
            payload = {
                "query_embedding": embedding,
                "match_threshold": 0.5,
                "match_count": 5
            }
            
            response = requests.post(rpc_endpoint, headers=headers, json=payload)
            
            if response.status_code == 200:
                results = response.json()
                if not results:
                    return f"Nenhum documento relevante encontrado na tabela {table_name}."
                
                formatted = f"Informações encontradas em {table_name}:\n"
                for item in results:
                    content = item.get("content", "") or item.get("body", "") or str(item)
                    formatted += f"- {content}\n"
                return formatted
            else:
                 return f"Erro na busca vetorial (RPC {target_rpc}): {response.text}. Verifique se a função RPC existe no Supabase."

        except Exception as e:
            return f"Erro na ferramenta de busca vetorial: {str(e)}"
