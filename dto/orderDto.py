from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, Picture

from sqlalchemy.orm import Session

from sqlalchemy import text

from datetime import datetime

class OrderDto:
    def __init__(self,engine) -> None:
        self.engine = engine

    def createOrder(self, user_id, addr, name, phone):
        with Session(self.engine) as session:
            items = session.query(CartItem).filter_by(user_id=user_id).all()
            if not items or items==[]:
                raise Exception('Empty Cart')
            order=Order(
                receiverAddress=addr,
                receiverName=name,
                receiverPhone=phone,
                createTime=datetime.now().isoformat(),
                user_id=user_id
                )
            session.add(order)
            for item in items:
                a = OrderItem(
                    name=item.product.name,
                    price = item.product.price,
                    count = item.count,
                    order_id=order.id,
                    product_id=item.product_id
                    )
                item.product.sale += 1
                session.add(a)
                session.delete(item) # 记得把购物车项目删除掉
            session.commit()

    def finishOrder(self,order_id):
        with Session(self.engine) as session:
            a = session.query(Order).get(order_id)
            if not a:
                raise Exception('Order Not Found')
            if a.finishTime:
                raise Exception('Cannot finish twice')
            a.finishTime = datetime.now().isoformat()
            session.commit()

    def getOrderDetailByUserId(self,user_id):
        with Session(self.engine) as session:
            orders = session.query(Order).filter_by(user_id=user_id).all()
            ret = []
            for order in orders:
                d = ({'addr':order.receiverAddress,
                'name':order.receiverName,
                'phone':order.receiverPhone,
                'createTime': order.createTime,
                'finishTime':order.finishTime,
                'user_id':order.user_id,
                'items':[]})
                for item in order.orderItems:
                    d['items'].append({
                        'name':item.name,
                        'price':item.price,
                        'count':item.count,
                        'product_id':item.product_id,
                    })
                ret.append(d)
            print(ret)
            return ret

    def getAllOrder(self):
        with Session(self.engine) as session:
            orders = session.query(Order).all()
            ret = []
            for order in orders:
                d = ({'addr':order.receiverAddress,
                'name':order.receiverName,
                'phone':order.receiverPhone,
                'createTime': order.createTime,
                'finishTime':order.finishTime,
                'user_id':order.user_id,
                'items':[]})
                for item in order.orderItems:
                    d['items'].append({
                        'name':item.name,
                        'price':item.price,
                        'count':item.count,
                        'product_id':item.product_id,
                    })
                ret.append(d)
            print(ret)
            return ret

    def addVisit(self,user_id, product_id):
       
        visit = Visit(product_id=product_id, user_id=user_id, visitTime=datetime.now().isoformat())
        with Session(self.engine) as session:
            session.add(visit)
            session.commit()
    
    def getAllVisits(self):
        with Session(self.engine) as session:
            result = session.query(Visit)
            ret = []
            for row in result:
                ret.append( {'id':row.id, 'user_id':row.user_id, 'product_id': row.product_id, 'visitTime':row.visitTime})
        return ret

from model.model import createEngineWithCreateAll, Base

orderDto = OrderDto(createEngineWithCreateAll(Base))