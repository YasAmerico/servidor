from typing import List


class Author:
    def __init__(self,id:int,name:str):
        self.id = id
        self.name = name 


class Book:
    def __init__(self,id:int, title:str,author_ids:List[int]):
        self.id = id
        self.title = title 
        self.author_ids = author_ids    
