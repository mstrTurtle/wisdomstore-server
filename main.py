import uvicorn
import uuid
from fastapi import Request, FastAPI

app = FastAPI()

data_dir='./data'

i = 0

def getFileDir(fname):
    import os
    return os.path.join(data_dir,fname)

@app.get("/")
async def root():
    global i
    i+=1
    return {"message": i}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": "item_id"}

from fastapi import File, UploadFile
from fastapi.responses import FileResponse

from pydantic import BaseModel


class Item(BaseModel):
    fname: str


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        # str(uuid.uuid4()) + '-' + 
        with open(getFileDir(file.filename), 'wb') as f:
            f.write(contents)
    except Exception as e:
        return {"message": "There was an error uploading the file" + repr(e)}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/pics",response_class=FileResponse,responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON item or an image.",
        }
    },)
def pic(fname):
    # return fastapi.responses.FileResponse(fname)
    return getFileDir(fname)

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, access_log=True)