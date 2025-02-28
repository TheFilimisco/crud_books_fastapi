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

@app.post("/create_book", status_code=status.HTTP_201_CREATED)
def crete_book(book: BookInput):
    new_id = len(list_books) + 1
    new_book = {"id": new_id}
    new_book.update(book)
    list_books.append(new_book)
    return new_book

@app.put("/books/{id_book}")
def update(id_book: int, book: BookInput) ->BookOutput:
    for item_book in list_books:
        if item_book["id"]  == id_book:
            item_book.update(book)
            return item_book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.delete("/delete/{id_book}", status_code=status.HTTP_200_OK)
def delete_book(id_book: int):
    for book in list_books:
        if book["id"] == id_book:
            list_books.remove(book)
            return {"message": "Book deleted", "deleted_book": book}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


