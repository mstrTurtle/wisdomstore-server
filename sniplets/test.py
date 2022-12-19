from fastapi import FastAPI
import uvicorn
from dto.dto import Dto, dto

app = FastAPI()

@app.get('/register')
async def register(name, password, email, role):
    try:
        # dto = Dto(createEngineWithCreateAll(Base))
        # global dto
        dto.addUser(name,password,email,role)
        dto.testInsertAndQuery()
        # global i
        # i+=1
        return {'status':'Ok','name':name}
    except Exception as e:
        raise e
        return {'status':'Fail','reason':repr(e)}

# 入口
if __name__ == '__main__':
    uvicorn.run("test:app", port=8000, reload=True, access_log=True)
