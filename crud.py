from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

books = [
    {
        "id": 1,
        "title": "Things Fall Apart",
        "author": "Chinua Achebe",
        "publish_date": "1958-06-17"
    },
    {
        "id": 2,
        "title": "Half of a Yellow Sun",
        "author": "Chimamanda Ngozi Adichie",
        "publish_date": "2006-08-12"
    },
    {
        "id": 3,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publish_date": "1925-04-10"
    },
    {
        "id": 4,
        "title": "1984",
        "author": "George Orwell",
        "publish_date": "1949-06-08"
    },
    {
        "id": 5,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publish_date": "1960-07-11"
    }
]
app = FastAPI()

@app.get("/book")
def get_book():
    return books

class Book(BaseModel):
  id: int
  title: str
  author: str
  publish_date: str

@app.get("/book/{book_id}")
def get_book(book_id: int):
  for book in books:
    if book["id"] == book_id:
       return book
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.post("/book")
def create_book(book: Book):
  new_book = book.model_dump()
  books.append(new_book)

class BookUpdate(BaseModel):
  title: str
  author: str
  publish_date: str

@app.put("/book/{book_id}")
def update_book(book_id: int, book_update: BookUpdate):
  for book in books:
    if book["id"] == book_id:
      book["title"] = book_update.title
      book["author"] = book_update.author
      book["publish_date"] = book_update.publish_date
      return book
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}")
def delete_book(book_id: int):
  for book in books:
    if book["id"] == book_id:
      books.remove(book)
      return { "Message": "Book deleted successfully" }
  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
