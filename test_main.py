from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_book(test_user):
    response = client.post("/books/", 
                           json={"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre":"FICTION", "year_published":2014},
                           headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json()["id"] is not None

def test_books_bad_auth():
    response = client.get("/books/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

@pytest.mark.asyncio
async def test_get_book(book, user, test_user):
    book = book
    response = await client.get(f"/books/{book.id}", headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json()["title"] == "The Great Gatsby"

def test_book_not_found(user, test_user):
    response = client.get("/books/9999/", headers={"Authorization": test_user})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    
def test_get_all_books(book, user, test_user):
    response = client.get(f"/books/", headers={"Authorization": test_user})
    assert response.status_code == 200
    assert len(response.json()) >=1

def test_update_book(book, user, test_user):
    response = client.put(f"/books/{book.id}", 
                           json={"title": "The Great Gatsby",
                                 "author": "F. Scott Fitzgerald",
                                 "genre":"FICTION",
                                 "year_published":2016
                                 },
                           headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json()["year_published"] == 2016


def test_delete_book(book, user,test_user):
    response = client.put(f"/books/{book.id}",
                           headers={"Authorization": test_user})
    assert response.status_code == 200
    
def test_delete_book_not_found(user, test_user):
    response = client.delete("/books/9999/", headers={"Authorization": test_user})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    
def test_add_book_review(book, user,test_user):
    response = client.post(f"/books/{book.id}/review/", 
                           json={"review_text": "Great Book", "rating":4},
                           headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json()["review_text"] == "Great Book"
    assert response.json()["rating"] == 4
    assert response.json()["id"] is not None
    
def test_get_summary(book, user, review, test_user):
    response = client.get(f"/books/{book.id}", headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json() == {"summary": "Sample Summary","average_rating": 4.0}

def test_get_summary_not_found(user, test_user):
    response = client.get("/books/9999/summary", headers={"Authorization": test_user})
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}
    
def test_recommendations(book, user, test_user):
    response = client.get("/recommendations/", headers={"Authorization": test_user})
    assert response.status_code == 200
    assert len(response.json()) >=1
    
def test_generate_summary(book, user, test_user):
    response = client.post("/generate-summary/", 
                           json={"content": "Sample Content"},
                           headers={"Authorization": test_user})
    assert response.status_code == 200
    assert response.json()["generated_summary"] is not None