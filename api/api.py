import uuid
from fastapi import Request, FastAPI, File, UploadFile
from fastapi.responses import FileResponse

from pydantic import BaseModel
from dto.cartDto import cartDto

# from model.model import createEngineWithCreateAll, Base
from dto.dto import Dto, dto
from dto.picDto import picDto

from fastapi.middleware.cors import CORSMiddleware

from dto.productDto import productDto
from dto.visitDto import visitDto
from dto.orderDto import orderDto

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# dto = Dto(createEngineWithCreateAll(Base))

data_dir = './data'

i = 0

dto.addUser('xjy','123','qq769711153@hotmail.com','common')
productDto.addProduct('神奇药水',44,'药水',10,'http://e.hiphotos.baidu.com/image/pic/item/a1ec08fa513d2697e542494057fbb2fb4316d81e.jpg','很神奇的药水')
cartDto.addCartItem(1,1,4)
visitDto.addVisit(1,1)
orderDto.createOrder(1,'USA','JoeBiden','911')

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
    return {"item_id": item_id}


class Item(BaseModel):
    '''测试用的自定义破类'''
    fname: str


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    '''上传图片文件API'''
    try:
        originalName = file.filename
        postfix = originalName.split('.')[-1]
        uuidName = f'{str(uuid.uuid4())}.{postfix}'
        contents = file.file.read()
        # str(uuid.uuid4()) + '-' +
        with open(getFileDir(uuidName), 'wb') as f:
            f.write(contents)
        picDto.addPic(uuidName=uuidName, originalName=originalName)
        print(picDto.getAllPics())
    except Exception as e:
        return {"message": "There was an error uploading the file" + repr(e)}
    finally:
        file.file.close()

    return {
        "message": f"Successfully uploaded {file.filename}",
        "uuidName": uuidName,
        "originalName": originalName,
        }


@app.get("/pics", response_class=FileResponse, responses={
    200: {
        "content": {"image/png": {}},
        "description": "Return the JSON item or an image.",
    }
},)
async def pic(fname):
    '''获得文件API'''
    print(fname)
    print('ahaha')
    print(getFileDir(fname))
    return getFileDir(fname)

@app.get('/register')
async def register(name, password, email, role):
    try:
        # dto = Dto(createEngineWithCreateAll(Base))
        # global dto
        dto.addUser(name,password,email,role)
        # dto.testInsertAndQuery()
        # global i
        # i+=1
        return {'status':'Ok','name':name}
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}

@app.get('/login')
async def login(name, password):
    try:
        # dto = Dto(createEngineWithCreateAll(Base))
        # global dto
        # dto.addUser(name,password,email,role)
        ret =  dto.getAllUsers()
        user = (dto.getUserByName(name))
        print(ret)
        if not user:
            return {'status':'Fail','reason':'user not found'}
        elif user.password == password:
            return {'status':'Ok','name':name,'user_id':user.id}
        else:
            return {'status':'Fail'}
        return ret
        dto.testInsertAndQuery()
        # global i
        # i+=1
        return {'status':'Ok','name':name}
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}


@app.get('/product/add')
async def productAdd(name,price:float,category,stock:int,imgurl,description):
    try:
        productDto.addProduct(name,price,category,stock,imgurl,description)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

@app.get('/product')
async def productFindById(id:int):
    try:
        d = productDto.getProductById(id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok','detail':d}

@app.get('/product/all')
async def productGetAll():
    try:
        d = productDto.getAllProduct()
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok','products':d}

@app.get('/product/search')
async def productSearch(name):
    try:
        a = productDto.searchProduct(name)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok', 'products':a}

@app.get('/cart')
async def getCart(user_id:int):
    try:
        a = cartDto.getAllCartItemsByUserId(user_id=user_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok', 'cartItems':a}

@app.get('/cart/add')
async def addCartItem(user_id:int, product_id:int, count:int):
    try:
        a = cartDto.addCartItem(user_id=user_id, product_id=product_id, count=count)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok', 'cartItems':a}

@app.get('/cart/remove')
async def addCartItem(user_id:int, product_id:int):
    try:
        a = cartDto.removeCartItem(user_id=user_id, product_id=product_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok', 'cartItems':a}

@app.get('/visit/add')
async def visitAdd(user_id:int,product_id:int):
    try:
        return visitDto.addVisit(user_id,product_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}


@app.get('/visit/all')
async def visitAll():
    try:
        return visitDto.getAllVisits()
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

@app.get('/order/create')
async def orderCreate(user_id, addr, name, phone):
    try:
        return orderDto.createOrder(user_id, addr, name, phone)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

@app.get('/order/finish')
async def orderFinish(order_id:int):
    try:
        return orderDto.finishOrder(order_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

@app.get('/order/all')
async def orderAll():
    try:
        return orderDto.getAllOrder()
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

@app.get('/order/userid')
async def orderByUserId(user_id:int):
    try:
        return orderDto.getOrderDetailByUserId(user_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}