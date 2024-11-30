import sqlite3
import g

DATABASE = 'stotage.db'

#Inicializar banco de dados
def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL, 
            author_id INTEGER
        )
    ''')

    db.commit()
    #close_connection()

    #conectar ao banco de dados
def get_db():
    db = getattr(g, '_database',None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#fechar conexão com o o banco de dados ao finalizar a requisição
def close_connection():
    db = getattr(g,'_database',None)
    if db is not None:
        db.close()

#Gravar Autor no banco de dados
def gravarAuthorDB(name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO AUTHOR (name) VALUES(?),'
                (name))
    db.commit()

def gravarBookDB(title:str,id_author:int):
    db= get_db()
    cursor = db.cursor()
    cursor.execute(f"INSERT INTO book(title,author_id)VALUES (?,?)",(title,id_author)) 
    db.commit()
   
   
    close_connection()
    
