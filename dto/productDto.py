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
    
    def deleteProduct(self,product_id):
        with Session(self.engine) as session:
            product = session.query(Product).get(product_id)
            if not product:
                raise Exception('Product Not Found')
            session.delete(product)
            session.commit()

    def updateProduct(self,product_id, name,price,category,stock,imgurl,description):
        with Session(self.engine) as session:
            product = session.query(Product).get(product_id)
            if not product:
                raise Exception('Product Not Found')
            product.name=name
            product.price=price
            product.category=category
            product.stock=stock
            product.imgurl=imgurl
            product.description=description
            session.commit()
    


    def searchProduct(self,name):
        ret = []
        with Session(self.engine) as session:
            result = session.query(Product).filter(Product.name.ilike(f'%{name}%')).all()
            for row in result:
                ret.append({'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description})
            return ret
    
    def getAllProductByCategory(self,category):
        ret = []
        with Session(self.engine) as session:
            result = session.query(Product).filter_by(category=category).all()
            for row in result:
                ret.append({'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description})
            return ret
    
    def getAllProduct(self):
        ret = []
        with Session(self.engine) as session:
            result = session.query(Product).all()
            for row in result:
                ret.append({'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description})
            return ret
    
    def getProductById(self,id):
        with Session(self.engine) as session:
            row = session.query(Product).get(id)
            if row:
                return {'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description}
            else:
                raise Exception
    
    def getAllRank(self):
        ret = []
        with Session(self.engine) as session:
            result = session.query(Product).order_by(Product.sale.desc()).all()
            for row in result:
                ret.append({'id':row.id,'name':row.name,'price':row.price,'category':row.category,'stock':row.stock,'imgurl':row.imgurl,'description':row.description, 'sale':row.sale})
            return ret


from model.model import createEngineWithCreateAll, Base

productDto = ProductDto(createEngineWithCreateAll(Base))