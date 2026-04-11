from fastapi import Depends, FastAPI
import uvicorn
from src.api import main_router

app = FastAPI()
app.include_router(main_router)




if __name__ == '__main__':
    uvicorn.run('src.main:app', host='127.0.0.1', port=8080, reload=True)
