from typing import Callable
import time

from fastapi import FastAPI, Request, Response
import uvicorn

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next: Callable):
    ip_address = request.client.host
    print(f'{ip_address=}')
    # if ip_address == '127.0.0.1':
    #     return Response(status_code=429, content='Вы превысили количество запросов')
    start = time.perf_counter()
    response = await call_next(request)
    end = time.perf_counter() - start
    print(f'Время обработки запроса: {end}') #типа логи
    response.headers["X-Ip-Address"] = ip_address
    return response


@app.get("/users", tags=['Пользователи'])
async def get_users():
    time.sleep(0.5)
    return [{'id': 1, 'name': 'Egor'}]


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
