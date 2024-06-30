from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Book, Review
from sqlalchemy import func
import database

# User
async def get_user(db:AsyncSession, username:str):
    result = await db.execute(select(User).filter(User.username==username))
    return result.scalar_one_or_none()

# Book
async def create_book(db:AsyncSession, book:Book):
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book

async def update_book(db:AsyncSession, book_id:int, update_data:dict):
    book = await get_book_by_id(db, book_id)
    if book:
        for key, value in update_data.items():
            setattr(book,key,value)
        await db.commit()
        await db.refresh(book)
    return book

async def get_all_books(db:AsyncSession):
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book_by_id(db:AsyncSession, book_id:int):
    result = await db.execute(select(Book).filter(Book.id==book_id))
    return result.scalar_one_or_none()

async def delete_book(db:AsyncSession, book_id:int):
    book = await get_book_by_id(db, book_id)
    if book:
        await db.delete(book)
        await db.commit()
    return book

# Summary
async def get_book_summary_and_avg_rating(db:AsyncSession, book_id:int):
    book = await get_book_by_id(db, book_id)
    if not book:
        return None
    avg_rating = await db.execute(select(func.avg(Review.rating)).filter(Review.book_id==book_id))
    avg_rating = avg_rating.scalar()
    return {"summary":book.summary, "average_rating":avg_rating}

# review
async def get_all_reviews(db:AsyncSession, book_id:int):
    result = await db.execute(select(Review).filter(Review.book_id==book_id))
    return result.scalars().all()

async def create_review(db:AsyncSession, review:Review):
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review


