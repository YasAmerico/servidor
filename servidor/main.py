from fastapi import FastAPI
from ariadne.asgi import GraphQL
from resolvers import query,mutation

from ariadne import make_executable_schema
from ariadne import gql
app = FastAPI()

type_defs = gql("""
    type Author{
        id:ID!
        name:String!   
    }
            
    type Books{
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
        updateAuthor(id:ID!,name:String!):Author!
        deleteAuthor(id:ID!): Boolean!
                
        createBook(title:String!,authorIds:[ID!]!):Book!
        updateBook(id:ID!,title:String!,authorIds:[ID!]!):Book!
        deleteBook(id:ID!):Boolean!               
    }
""")
schema = make_executable_schema(type_defs, query, mutation)

#configura o endpoint GraphQl
app.add_route("/graphql",GraphQL(schema,debug=True))

@app.get("/")
def read_root():
    return {"message":"Servidor GraphQl!"}