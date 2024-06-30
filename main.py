from fastapi import Request, FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import models, crud, database, schema
from fastapi_auth_middleware import AuthMiddleware
from typing import Annotated
import secrets
from utils import generate_sha256_hash

app = FastAPI(
    title="BookManagementSyatem",
    description="This app is used to manage books",
    summary="Help to reommand books based on review and rating",
    version="0.0.1",
)
security = HTTPBasic()

async def authenticate_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    username = credentials.username.encode("utf8")
    password = generate_sha256_hash(credentials.password).encode("utf8")

    # Get user from database
    db_session = database.SessionLocal()
    user: models.User = await crud.get_user(db_session, credentials.username)
    
    is_correct_username = secrets.compare_digest(username, str(user.username).encode("utf8"))
    is_correct_password = secrets.compare_digest(password, str(user.password).encode("utf8"))
    
    # Check if user exists in the database
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

# app.add_middleware(AuthMiddleware, verify_header=auth.authenticate_user)


@app.get("/users/me")
def read_current_user(user: Annotated[str, Depends(authenticate_user)]):
    return {"username": user}

@app.on_event('startup')
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
        
@app.post("/books")
async def create_book(book_data: schema.RequestBook,
                      db: Annotated[AsyncSession, Depends(database.get_session)],
                      user: Annotated[models.User, Depends(authenticate_user)]):
    return await crud.create_book(db, models.Book(**book_data.dict()))

@app.get("/books")
async def get_all_books(db: Annotated[AsyncSession, Depends(database.get_session)],
                      user: Annotated[models.User, Depends(authenticate_user)]):
    return await crud.get_all_books(db)

@app.get("/books/{book_id}")
async def get_book(book_id: int,
                   db: Annotated[AsyncSession, Depends(database.get_session)],
                   user: Annotated[models.User, Depends(authenticate_user)]):
    book =  await crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
    
@app.put("/books/{book_id}")
async def update_book(book_id: int,
                      book_update:schema.RequestBook,
                      db: Annotated[AsyncSession, Depends(database.get_session)],
                      user: Annotated[models.User, Depends(authenticate_user)]):
    return await crud.update_book(db, book_id, book_update.dict())

@app.delete("/books/{book_id}")
async def delete_book(book_id: int,
                      db: Annotated[AsyncSession, Depends(database.get_session)],
                      user: Annotated[models.User, Depends(authenticate_user)]):
    book = await crud.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/books/{book_id}/reviews")
async def get_book_reviews(book_id: int,
                           db: Annotated[AsyncSession, Depends(database.get_session)],
                           user: Annotated[models.User, Depends(authenticate_user)]):
    return await crud.get_all_reviews(db, book_id)

@app.post("/books/{book_id}/reviews")
async def add_book_review(book_id: int,
                          review: schema.RequestReview,
                          db: Annotated[AsyncSession, Depends(database.get_session)],
                          user: Annotated[models.User, Depends(authenticate_user)]):
    review_dict = {
        "review_text":review.review_text,
        "rating":review.rating,
        "book_id":book_id,
        "user_id":user.id
    }
    return await crud.create_review(db, models.Review(**review_dict))

@app.get("/books/{book_id}/summary")
async def get_book_summery(book_id: int, 
                           db: Annotated[AsyncSession, Depends(database.get_session)],
                           user: Annotated[models.User, Depends(authenticate_user)]):
    summary = await crud.get_book_summary_and_avg_rating(db, book_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Book not found")
    return summary

@app.get("/recommendations")
async def get_recommendations(db: Annotated[AsyncSession, Depends(database.get_session)],
                              user: Annotated[models.User, Depends(authenticate_user)]):
    # TODO - Write logic to generate-summary here
    books=  await crud.get_all_books(db)
    return {"recommendations":books}

@app.post("/generate-summary")
async def generate_summary(data: Request,
                           db: Annotated[AsyncSession, Depends(database.get_session)],
                      user: Annotated[models.User, Depends(authenticate_user)]):
    # TODO - Write logic to generate-summary here
    json_data = await data.json()
    generated_summary = "Generated summary for book content: " + json_data.get("content")
    return {'generated_summary': generated_summary}
