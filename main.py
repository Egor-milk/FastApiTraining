from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel


from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session # держит сессию открытой, пока не вернется ответ пользователю


SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class BookModel(Base): # в sqlalchemy всегда наследование от base класса
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]


@app.post('/setup_database')
async def setup_database(): # создаёт таблицу books
    async with engine.begin() as conn: #открыть соединение с бд
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) #в мета дата записываются все данные
    return {'ok': True}

class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id: int

@app.post('/books')
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {'ok': True}

@app.get('/books')
async def get_books(session: SessionDep):
    query = select(BookModel)
    await session.execute(query)
    result = await session.execute(query)
    return result.scalars().all()

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True)