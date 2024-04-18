import psycopg2
from sqlalchemy import create_engine
import ctypes


class Generic_DAO:

    def __init__(self, servidor=1, lanca_erro=False):
        # print("Construindo um objeto")
        self.servidor = servidor
        self.lanca_erro = lanca_erro

    def conecta_bd(self):
        conn = psycopg2.connect(database="xxx",
                                user="user_xi",
                                host='00.0.00.000',
                                password="xxxx",
                                port=5432)

        return conn

    def abre_result_set(self, sql, args=None):
        try:
            conn = self.conecta_bd()
            cur = conn.cursor()
            cur.execute(sql, args)
            result = cur.fetchall()
            conn.commit()
            cur.close()
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - Consulta não realizado", 0)
            if self.lanca_erro:
                raise TypeError(e.args[0])
            return []
        finally:
            try:
                conn.close()
            except:
                pass
            return result

    def executa_sql(self, sql, args=None):
        try:
            qtd = 0
            conn = self.conecta_bd()
            cur = conn.cursor()
            qtd = cur.execute(sql, args)
            conn.commit()
            cur.close()
            qtd = + 1
        except Exception as e:
            retorno = "Erro: {}".format(e.args)
            print(retorno)
            ctypes.windll.user32.MessageBoxW(0, retorno, "Erro - Insert não realizado", 0)
        finally:
            try:
                conn.close()
            except:
                pass
            return qtd

    def export_to_mysql(self, table, df, if_exists='replace', limpar=True):
        url = 'postgresql://user_xi:xxx@00.0.00.0000:5432/BBBI'
        sqlEngine = create_engine(url, pool_recycle=3600)
        if if_exists == "ignore":
            self.executa_sql(f"DELETE FROM {table}_temp")
            df.to_sql(f"{table}_temp", con=sqlEngine, if_exists='append')
            result = self.executa_sql(f"insert into {table} select * from {table}_temp")
            if limpar:
                self.executa_sql(f"DELETE FROM {table}_temp")
        else:
            result = df.to_sql(table, con=sqlEngine, if_exists=if_exists)
        return result
