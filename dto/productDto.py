from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, Picture

from sqlalchemy.orm import Session

from sqlalchemy import text

class ProductDto:
    def __init__(self,engine) -> None:
        self.engine = engine

    def addProduct(self,name,price,category,stock,imgurl,description):
        product = Product(name=name,price=price,category=category,stock=stock,imgurl=imgurl,description=description)
        with Session(self.engine) as session:
            session.add(product)
            session.commit()

    def searchProduct(self,name):
        ret = []
        with Session(self.engine) as session:
            result = session.query(Product).filter(Product.name.ilike(f'%{name}%')).all()
            for row in result:
                ret.append({'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description})
            return ret
    
    def getProductById(self,id):
        with Session(self.engine) as session:
            row = session.query(Product).get(id)
            if row:
                return {'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description}
            else:
                return None

from model.model import createEngineWithCreateAll, Base

productDto = ProductDto(createEngineWithCreateAll(Base))