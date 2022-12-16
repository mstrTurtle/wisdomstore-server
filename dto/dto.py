from model.model import Base, User, CartItem, Product, Order, OrderItem, Visit, createMemoryEngine ,createAll

from sqlalchemy.orm import Session

from sqlalchemy import text

class Dto:
    def __init__(self) -> None:
        self.engine=createMemoryEngine()
        createAll(Base = Base,engine = self.engine)

    def testInsertAndQuery(self):
        squidward = User(name="squidward", password="Squidward Tentacles", email='',role='')
        krabs = User(name="Efsadd", password="Squidward Tentacles", email='',role='')

        with Session(self.engine) as session:
            session.add(squidward)
            session.add(krabs)
            session.commit()

        with Session(self.engine) as session:
            result = session.execute(
                text("SELECT * FROM user_account"),
                [],
            )
            for row in result:
                print(f"{row.id} - name: {row.name}  passwd: {row.password}")
            session.commit()