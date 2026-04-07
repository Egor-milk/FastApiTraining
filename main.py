import uvicorn
from fastapi import FastAPI, File, UploadFile as UF
from typing import Annotated, List
from pydantic import WithJsonSchema

app = FastAPI()

UploadFile = Annotated[UF, WithJsonSchema({"type": "string", "format": "binary"})]
@app.post('/files')
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f'1_{filename}', 'wb') as f:
        f.write(file.read())

@app.post('/multiple_files')
async def upload_files(uploaded_files: Annotated[list[UploadFile], File(...)]):
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f'1_{filename}', 'wb') as f:
            f.write(file.read())

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8080, reload=True)