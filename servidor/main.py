from fastapi import FastAPI
from ariadne.asgi import GraphQL
from resolvers import query,mutation
from banco import init_db
from ariadne import make_executable_schema
from ariadne import gql

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#Definindo as origens permitidas pelo CORS
origins =[
    "http://localhost",
    "http://localhost:8000",#se o frontend estiver na porta 8000
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

#Inicializar o banco de dados
init_db()

type_defs = gql("""
    type Author{
        id:ID!
        name:String!   
    }
            
    type Book{
        id:ID!
        title:String!
        authors:[Author!]!       
    }  

    type Query{
        authors:[Author!]!
        books:[Book!]!
    }

    type Mutation{
        createAuthor(name:String!):Author!            
        updateAuthor(id:Int!,name:String!):Author!
        deleteAuthor(id:Int!): Boolean!
                
        createBook(title:String!,authorIds:[Int!]!):Book!
        updateBook(id:Int!,title:String!,authorIds:[Int!]!):Book!
        deleteBook(id:Int!):Boolean!               
    }
""")
schema = make_executable_schema(type_defs, query, mutation)

graphql_app = GraphQL(schema,debug=True)

#configura o endpoint GraphQl
app.add_route("/graphql",graphql_app)

@app.get("/")
def read_root():
    return {"message":"Servidor GraphQl!"}
