from ariadne import QueryType, MutationType, make_executable_schema, gql
from flask import Flask, jsonify, request, g
import sqlite3

# Configuração da aplicação Flask
app = Flask(__name__)
DATABASE = "library.db"

# Definição do esquema GraphQL
type_defs = gql("""
    type Author {
        id: ID!
        name: String!
    }

    type Book {
        id: ID!
        title: String!
        authorId: Int!
    }

    type Query {
        authors: [Author!]!
        books: [Book!]!
    }

    type Mutation {
        createAuthor(name: String!): Author!
        updateAuthor(id: ID!, name: String!): Author
        deleteAuthor(id: ID!): Boolean!
        createBook(title: String!, authorId: Int!): Book!
        updateBook(id: ID!, title: String!, authorId: Int!): Book
        deleteBook(id: ID!): Boolean!
    }
""")

# Resolvers para consultas e mutações
query = QueryType()
mutation = MutationType()

# Conexão com o banco de dados SQLite
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Inicializar banco de dados
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Criação das tabelas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                FOREIGN KEY(author_id) REFERENCES authors(id)
            )
        ''')
        db.commit()

# Resolver para listar autores
@query.field("authors")
def resolve_authors(_, info):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM authors")
    authors = cursor.fetchall()
    return [dict(author) for author in authors]

# Resolver para listar livros
@query.field("books")
def resolve_books(_, info):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    return [dict(book) for book in books]

# Resolver para criar autor
@mutation.field("createAuthor")
def resolve_create_author(_, info, name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    db.commit()
    return {"id": cursor.lastrowid, "name": name}

# Resolver para atualizar autor
@mutation.field("updateAuthor")
def resolve_update_author(_, info, id, name):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (name, id))
    db.commit()
    if cursor.rowcount > 0:
        return {"id": id, "name": name}
    return None

# Resolver para deletar autor
@mutation.field("deleteAuthor")
def resolve_delete_author(_, info, id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM authors WHERE id = ?", (id,))
    db.commit()
    return cursor.rowcount > 0

# Resolver para criar livro
@mutation.field("createBook")
def resolve_create_book(_, info, title, authorId):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM authors WHERE id = ?", (authorId,))
    author = cursor.fetchone()
    if not author:
        raise ValueError("Autor não encontrado.")
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, authorId))
    db.commit()
    return {"id": cursor.lastrowid, "title": title, "authorId": authorId}

# Resolver para atualizar livro
@mutation.field("updateBook")
def resolve_update_book(_, info, id, title, authorId):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE books SET title = ?, author_id = ? WHERE id = ?", (title, authorId, id))
    db.commit()
    if cursor.rowcount > 0:
        return {"id": id, "title": title, "authorId": authorId}
    return None

# Resolver para deletar livro
@mutation.field("deleteBook")
def resolve_delete_book(_, info, id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (id,))
    db.commit()
    return cursor.rowcount > 0

# Criação do schema
schema = make_executable_schema(type_defs, query, mutation)

# Inicializar banco de dados e rodar o servidor
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
