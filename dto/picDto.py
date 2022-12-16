from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, Picture

from sqlalchemy.orm import Session

from sqlalchemy import text

class PicDto:
    def __init__(self,engine) -> None:
        self.engine = engine

    def addPic(self,uuidName,originalName):
        pic = Picture(uuidName=uuidName, originalName=originalName)
        with Session(self.engine) as session:
            session.add(pic)
            session.commit()

    def addUser(self,name,password,email,role):
        user = User(name=name,password=password,email=email,role=role)
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
    
    def getAllPics(self):
        ret = []
        with Session(self.engine) as session:
            result = session.execute(
                text("SELECT * FROM picture"),
                [],
            )
            for row in result:
                print(row)
                ret.append({'info': f"{row.id} - orgName: {row.originalName}  uuidName: {row.uuidName}"})
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

picDto = PicDto(createEngineWithCreateAll(Base))