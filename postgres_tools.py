import os
import json
from agno.tools import Toolkit
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

class PostgresTools(Toolkit):
    def __init__(self):
        super().__init__(name="postgres_tools")
        self.db_url: str = os.getenv("SUPABASE_DB_URL")
        
        if not self.db_url:
            raise ValueError("SUPABASE_DB_URL deve estar definido no arquivo .env (ex: postgresql://user:pass@host:5432/postgres)")
        
        # O SQLAlchemy precisa do prefixo 'postgresql://', se tiver 'postgres://' vamos corrigir para compatibilidade
        if self.db_url.startswith("postgres://"):
            self.db_url = self.db_url.replace("postgres://", "postgresql://", 1)
            
        try:
            self.engine = create_engine(self.db_url)
        except Exception as e:
            raise ValueError(f"Erro ao inicializar conexão com o banco de dados: {e}")
        
        self.register(self.list_tables_sql)
        self.register(self.run_sql_query)

    def list_tables_sql(self) -> str:
        """
        Lista todas as tabelas públicas disponíveis no banco de dados usando SQL.
        
        Returns:
            str: Lista de nomes de tabelas encontradas no schema public.
        """
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        return self.run_sql_query(query)

    def run_sql_query(self, query: str) -> str:
        """
        Executa uma consulta SQL arbitrária (SELECT, UPDATE, INSERT, DELETE) no banco de dados Supabase/PostgreSQL.
        Use esta ferramenta APENAS quando precisar fazer consultas complexas (JOINs, agregações, etc) 
        ou comandos que não são possíveis via REST API (SupabaseTools).
        
        Args:
            query (str): A string contendo o comando SQL puro a ser executado.
            
        Returns:
            str: Resultado da consulta em formato JSON, ou mensagem de sucesso/erro.
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                
                # Para comandos de modificação (INSERT/UPDATE/DELETE) que não retornam linhas
                if not result.returns_rows:
                    connection.commit()
                    return f"Comando SQL executado com sucesso. Linhas afetadas: {result.rowcount}"
                
                # Para SELECT, buscar as linhas e formatar
                rows = result.fetchall()
                column_names = list(result.keys())
                
                data = []
                for row in rows:
                    row_dict = dict(zip(column_names, row))
                    # Converter possíveis objetos de data/hora ou outros tipos não-serializáveis em string
                    for key, val in row_dict.items():
                        if not isinstance(val, (int, float, str, bool, type(None))):
                            row_dict[key] = str(val)
                    data.append(row_dict)
                
                return json.dumps(data, indent=2, ensure_ascii=False)
                
        except SQLAlchemyError as e:
            return f"Erro ao executar consulta SQL: {str(e)}"
        except Exception as e:
            return f"Erro inesperado na ferramenta PostgresTools: {str(e)}"

if __name__ == "__main__":
    # Teste rápido se executado diretamente
    try:
        tools = PostgresTools()
        print("PostgresTools inicializado com sucesso.")
        print("Tabelas encontradas:")
        print(tools.list_tables_sql())
    except Exception as e:
        print(f"Erro na inicialização ou execução: {e}")
