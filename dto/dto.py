from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit

from sqlalchemy.orm import Session

from sqlalchemy import text

class Dto:
    def __init__(self,engine) -> None:
        self.engine = engine

    def addUser(self,name,password,email,role):
        with Session(self.engine) as session:
            a = session.query(User).filter_by(name=name).all()
            if a:
               raise Exception

        user = User(name=name,password=password,email=email,role=role)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    def getUserByName(self,name):
        with Session(self.engine) as session:
            return session.query(User).filter_by(name=name).first()
    
    def getAllUsers(self):
        ret = []
        with Session(self.engine) as session:
            result = session.execute(
                text("SELECT * FROM user_account"),
                [],
            )
            for row in result:
                print(row)
                ret.append({'info': f"{row.id} - name: {row.name}  passwd: {row.password}"})
            session.commit()
        return ret

    def testInsertAndQuery(self):
        squidward = User(name="squidward", password="Squidward Tentacles", email='',role='')
        krabs = User(name="Efsadd", password="Squidward Tentacles", email='',role='')

        # with Session(self.engine) as session:
        #     session.add(squidward)
        #     session.add(krabs)
        #     session.commit()

        with Session(self.engine) as session:
            result = session.execute(
                text("SELECT * FROM user_account"),
                [],
            )
            for row in result:
                print(f"{row.id} - name: {row.name}  passwd: {row.password}")
            session.commit()

from model.model import createEngineWithCreateAll, Base

dto = Dto(createEngineWithCreateAll(Base))