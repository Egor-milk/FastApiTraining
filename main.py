from symtable import Class

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

books = [
    {
        'id': 1,
        'title': 'Асинхронность в python',
        'author': 'Mattew'
    },
    {
        'id': 2,
        'title': 'backend разработка в python',
        'author': 'Артём'
    },
]

@app.get(
    "/books",
    tags=["книжки ебучие"],
    summary='Получить все книги'
)
def read_books():
    return books

@app.get("/books/{book_id}",
         tags=["книжки ебучие"],
         summary='Получить конкретную книгу'
         )
def get_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=404, detail="book not found")

class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(new_book: NewBook):
    books.append({
        'id': len(books) + 1,
        'title': new_book.title,
        'author': new_book.author
    })
    return {'success': True}

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)