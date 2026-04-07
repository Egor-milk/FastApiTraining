import uvicorn
from fastapi import FastAPI, BackgroundTasks
import time
import asyncio
app = FastAPI()

def sync_task():
    time.sleep(3)
    print("отправлен email")

async def async_task():
    await asyncio.sleep(3)
    print('Сделан запрос в сторонний API')


@app.post('/')
# async def some_route():
#     ...
#     asyncio.create_task(async_task()) #пользователю вернут статус 200
#     return {'ok': True} # и только потом задача выполнится на самом деле
async def some_route(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_task) #работает также как asyncio.create_task  но для синх ф-ии
    return {'ok': True}



if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080)