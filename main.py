from typing import Union

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

from books import books as list_books

app = FastAPI()

class BookOutput(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: Union[str,None]

class BookInput(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: Union[str,None]


@app.get("/")
def root():
    return "This Server is running!"


@app.get("/books")
def read() -> list[BookOutput]:
    return list_books

@app.get("/books/{id_item}")
def read_book(id_item : int) -> BookOutput:
    for item in list_books:
        if item["id"] ==id_item:
            return item
    raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,detail="Books not found")


@app.post("/create_book")
def crete_book(book: BookInput):
    new_id = len(list_books) + 1
    new_book = {"id": new_id}
    new_book.update(book)
    list_books.append(new_book)
    return new_book

@app.get("/delete/{id_book}")
def delete_book(id_book: int):
    print(list_books)
    list_books.remove(id_book)
