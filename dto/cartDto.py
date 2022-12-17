from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, Picture

from sqlalchemy.orm import Session

from sqlalchemy import text

class CartDto:
    def __init__(self,engine) -> None:
        self.engine = engine

    def addCartItem(self,user_id, product_id,count):
        with Session(self.engine) as session:
            a = session.query(Product).get(product_id)
            print(a)
            if not a:
                raise Exception('Product Doesnt Exist')
            b = session.query(User).get(user_id)
            if not b:
                raise Exception('User Doesnt Exist')
            c = session.query(CartItem).filter_by(user_id=user_id,product_id=product_id).all()
            if c:
                for fst in c:
                    fst.count = fst.count + count
                    break;
                session.commit()
                return

        cartItem = CartItem(count=count, product_id=product_id, user_id=user_id)
        with Session(self.engine) as session:
            session.add(cartItem)
            session.commit()
    
    def getAllCartItemsByUserId(self, user_id):
        with Session(self.engine) as session:
            result = session.query(CartItem).filter_by(user_id=user_id)
            ret = []
            for row in result:
                ret.append( {'id':row.id, 'product_id':row.product_id, 'count': row.count})
        return ret

from model.model import createEngineWithCreateAll, Base

cartDto = CartDto(createEngineWithCreateAll(Base))