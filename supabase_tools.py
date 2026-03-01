import os
import json
import requests
from agno.tools import Toolkit
from dotenv import load_dotenv

load_dotenv()

class SupabaseTools(Toolkit):
    def __init__(self):
        super().__init__(name="supabase_tools")
        self.url: str = os.getenv("SUPABASE_URL")
        self.key: str = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidos no arquivo .env")
            
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        self.register(self.list_tables)
        self.register(self.query_table)

    def list_tables(self) -> str:
        """
        Lista todas as tabelas públicas disponíveis no projeto Supabase (via API REST).
        
        Returns:
            str: Lista de nomes de tabelas ou mensagem de erro.
        """
        try:
            # Não há endpoint REST padrão público para listar tabelas sem permissões especiais.
            # Vamos tentar acessar endpoint raiz ou instruir o uso direto.
            # Mas podemos tentar inferir chamando um endpoint comum se soubermos.
            return "A listagem automática de tabelas via REST requer permissões elevate. Por favor, use 'query_table' com o nome da tabela que você deseja consultar (ex: users, products)."
        except Exception as e:
             return f"Erro ao listar tabelas: {str(e)}"

    def query_table(self, table_name: str, select: str = "*", limit: int = 10, filters: dict = None) -> str:
        """
        Executa uma consulta (SELECT) em uma tabela do Supabase via REST API.
        
        Args:
            table_name (str): Nome da tabela para consultar.
            select (str): Colunas para selecionar (padrão: "*").
            limit (int): Número máximo de resultados (padrão: 10).
            filters (dict): Dicionário de filtros (ex: {"status": "active"}). 
                            Suporta apenas igualdade simples por enquanto.

        Returns:
            str: Resultados da consulta em formato JSON.
        """
        try:
            # Construindo a URL
            # https://xyz.supabase.co/rest/v1/table_name?select=*&limit=10
            endpoint = f"{self.url}/rest/v1/{table_name}"
            params = {
                "select": select,
                "limit": limit
            }
            
            if filters:
                for col, val in filters.items():
                    # Supabase postgrest filter format: col=eq.val
                    params[col] = f"eq.{val}"
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            
            if response.status_code == 200:
                return json.dumps(response.json(), indent=2, ensure_ascii=False)
            else:
                return f"Erro na consulta Supabase ({response.status_code}): {response.text}"
                
        except Exception as e:
            return f"Erro ao consultar tabela '{table_name}': {str(e)}"

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    try:
        from dotenv import load_dotenv
        load_dotenv()
        tools = SupabaseTools()
        print("Supabase Tools (REST) inicializado com sucesso.")
    except Exception as e:
        print(f"Erro na inicialização: {e}")
