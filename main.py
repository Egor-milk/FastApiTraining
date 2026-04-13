from fastapi import FastAPI
import uvicorn
app = FastAPI()


@app.get("/users", tags=['Пользователи'])
async def get_users():
    return [{'id': 1, 'name': 'Egor'}]


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
