import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_DATABASE = os.getenv("DB_DATABASE")

def get_db_connection():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )
        print("Connexion réussie")
        return conn
    except pymysql.MySQLError as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def close_db_connection(conn):
    if conn:
        conn.close()
        print("Connexion fermée")
    else:
        print("Aucune connexion à fermer")

def execute_query(query, params=None):
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
            conn.commit()
            return result
        except pymysql.MySQLError as e:
            print(f"Erreur lors de l'exécution de la requête: {e}")
            return None
        finally:
            close_db_connection(conn)
    else:
        return None