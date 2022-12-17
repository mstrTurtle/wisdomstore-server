from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, Picture

from sqlalchemy.orm import Session

from sqlalchemy import text

from datetime import datetime

class VisitDto:
    def __init__(self,engine) -> None:
        self.engine = engine

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

visitDto = VisitDto(createEngineWithCreateAll(Base))