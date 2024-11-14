from ariadne import QueryType,MutationType
from models import Author,Book
import sqlite3

DATABASE = 'storage.db'

authors_db = []
books_db = []

query = QueryType()
mutation = MutationType()

@query.field("authors")
def resolve_authors(_,info):
    return authors_db

@query.field("books")
def resolve_books(_,info):
    return books_db

@mutation.field("createAuthor")
def resolve_create_author(_,info,name):
    author = Author(id = len(authors_db)+1,name=name)
    authors_db.append(author)
    return author

@mutation.field("updateAuthor")
def resolve_update_author(_,info,id,name):
    author=next((a for a in authors_db if a.id == id),None)
    if author:
        author.name = name
        return author
    return None

@mutation.field("deleteAuthor")
def resolve_delete_author(_, info, id):
    global authors_db
    authors_db = [a for a in authors_db if a.id != id]
    return True

@mutation.field("createBook")
def resolve_update_author(_, title , authorIds):
    book = Book (id=len(books_db)+ 1, title =title, author_ids=authorIds)
    books_db.append(book)
    return book

@mutation.field("updateBook")
def resolve_update_author(_,id , title , authorIds):
    book = next((b for b in books_db if b.id == id),None)
    if book:
        book.title = title
        book.author_ids = authorIds
        return book
    return None

@mutation.field("deleteBook")
def resolve_delete_author(_, title , id):
    global books_db
    books_db=[b for b in books_db if b.id != id]

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

#Inicializar banco de dados
def int_db():
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
    close_connection()

#Gravar Autor no banco de dados
def gravarAuthorDB(name):
    print("grava author no banco")
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO AUTHOR (name) VALUES(?),'
                (name))
    
    db.commit()
    close_connection()
