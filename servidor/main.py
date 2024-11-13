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

#configura o endpoint GraphQl
app.add_route("/graphql",GraphQL(schema,debug=True))

@app.get("/")
def read_root():
    return {"message":"Servidor GraphQl!"}
