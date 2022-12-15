import uvicorn
import uuid
from fastapi import Request, FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from pydantic import BaseModel

app = FastAPI()

data_dir = './data'

i = 0


def getFileDir(fname):
    '''实用函数, 传入文件名, 传出文件路径即path'''
    import os
    return os.path.join(data_dir, fname)


@app.get("/")
async def root():
    '''测试用的破烂API'''
    global i
    i += 1
    return {"message": i}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    '''递增的破API'''
    return {"item_id": "item_id"}


class Item(BaseModel):
    '''测试用的自定义破类'''
    fname: str


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    '''上传图片文件API'''
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


@app.get("/pics", response_class=FileResponse, responses={
    200: {
        "content": {"image/png": {}},
        "description": "Return the JSON item or an image.",
    }
},)
def pic(fname):
    '''获得文件API'''
    return getFileDir(fname)


# 入口
if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, reload=True, access_log=True)
