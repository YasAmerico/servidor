from fastapi import FastAPI
from ariadne import QueryType,MutationType,SubscriptionType
from models import Author,Book
from banco import gravarAuthorDB,gravarBookDB
import asyncio
from asyncio import get_event_loop
from starlette.websockets import WebSocket

authors_db = []
books_db = []
subscribers =[]#temporariamente,fazer função para trazer o main

query = QueryType()
mutation = MutationType()
subscription =SubscriptionType()


@query.field("authors")
def resolve_authors(_,info):
    return authors_db

@query.field("books")
def resolve_books(_,info):
    return books_db

@mutation.field("createAuthor")
def resolve_create_author(_,info,name:str) ->dict:
    author = Author(id = len(authors_db)+1,name=name)
    authors_db.append(author)
    gravarAuthorDB
    #Notificar todos as conexões Websocket conectados(assinantes)
    for subscriber in subscribers:
        asyncio.create_task(subscriber.send_json({"type":"authorAdicionado","author_id":author.id,"nome":author.name}))
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
def resolve_update_author(_, title , author_id):
    book = Book (id=len(books_db)+ 1, title =title, author_ids=author_id)
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
    return True

@subscription.source("authorAdicionado")
async def source_author_adicionado(_,info):
    while True:
        await asyncio.sleep(1)

@subscription.field("authorAdicionado")
def resolver_author_adicionado(obj,info):
    return obj["payload"]

def setSubscribers(p_subscribers,websocket:WebSocket):
    subscribers = p_subscribers
    subscribers.append(websocket)

def  deleteSubscribers(websocket:WebSocket):
    subscribers.remove(websocket)
