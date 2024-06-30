from pydantic import BaseModel
from typing import List, Optional

# Book
class RequestBook(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int  # Change the type to int
    
class ResponseBook(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year_published: int
    summary: str
              
# Review      
class RequestReview(BaseModel):
    review_text: str
    rating: int
 
class ResponseReview(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_text: str
    rating: int
