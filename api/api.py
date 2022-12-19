import uuid
from fastapi import Request, FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

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

dto.addUser('xjy','123','qq769711153@hotmail.com','admin')
dto.addUser('aa','bb','769711153@qq.com','common')
productDto.addProduct('神奇药水',44,'药水',10,'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fupload-images.jianshu.io%2Fupload_images%2F1265897-ba0d898c63e4c821.jpg&refer=http%3A%2F%2Fupload-images.jianshu.io&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1673947450&t=31ce12dd8d0bf22e509f7ef55b9e9c3d','很神奇的药水')
productDto.addProduct('本草纲目',30,'医书',10,'http://collection.sinaimg.cn/yjjj/20131225/U5826P1081T2D138067F6DT20131225081830.jpg','神奇的医书')
cartDto.addCartItem(1,1,4)
productDto.addProduct('神奇宝贝',20,'药水',10,'https://img0.baidu.com/it/u=4200801468,2758986524&fm=253&fmt=auto&app=138&f=JPEG?w=300&h=244','一个日本动漫卡通人物')
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
    '''注册用户的api'''
    try:
        dto.addUser(name,password,email,role)
        return {'status':'Ok','name':name}
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}

@app.get('/login')
async def login(name, password):
    '''登录的api'''
    try:
        ret =  dto.getAllUsers()
        user = (dto.getUserByName(name))
        print(ret)
        if not user:
            return {'status':'Fail','reason':'user not found'}
        elif user.password == password:
            return {'status':'Ok','name':name,'user_id':user.id}
        else:
            return {'status':'Fail'}
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

@app.get('/product/update')
async def productUpdate(product_id, name,price,category,stock,imgurl,description):
    try:
        productDto.updateProduct(product_id, name,price,category,stock,imgurl,description)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok' }

@app.get('/product/delete')
async def productDelete(product_id):
    try:
        productDto.deleteProduct(product_id)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok' }

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
        orderDto.createOrder(user_id, addr, name, phone)
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

@app.get('/order/unfinish')
async def orderFinish(order_id:int):
    try:
        return orderDto.unFinishOrder(order_id)
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

@app.get('/rank/all')
async def getAllRank():
    try:
        return productDto.getAllRank()
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok'}

import io
import csv
    
@app.get("/get_csv")
async def get_csv():
    '''下载销售排行榜的api'''
    stream = io.StringIO()

    listOfDict = productDto.getAllRank() # 从Product DTO获取排行表
    keys = listOfDict[0].keys()

    dw = csv.DictWriter(stream,keys) # 转为csv并以attachment返回
    dw.writeheader()
    dw.writerows(listOfDict)
    response = StreamingResponse(iter([stream.getvalue()]),
                        media_type="text/csv"
    )

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response
    
@app.get('/product/category')
async def productByCategory(category):
    try:
        d= productDto.getAllProductByCategory(category=category)
    except Exception as e:
        return {'status':'Fail','reason':repr(e)}
    return {'status':'Ok', 'products':d}