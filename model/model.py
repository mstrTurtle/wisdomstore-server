from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=True)

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())


from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    '''
    1. User表.
    User -> Visit
    User -> CartItem
    User -> Order
    '''
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    # 一名用户有许多购物车物品
    cartItems: Mapped[list["CartItem"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    # 一名用户访问多个商品
    visits: Mapped[list["Visit"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    # 一名用户可以下多个订单
    orders: Mapped[list["Order"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# 购物车
class CartItem(Base):
    '''
    2. CartItem表
    CartItem <- User
    '''
    __tablename__ = "cart_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    stock: Mapped[str] = mapped_column(String(30))
    imgurl: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped['User'] = relationship(back_populates="cartItems")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# 物品, 如一个图书的信息
class Product(Base):
    '''
    3. Product表.
    Product -> Visit
    Product -> OrderItem
    '''
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    price: Mapped[str] = mapped_column(String(30))
    category: Mapped[str] = mapped_column(String(30))
    stock: Mapped[str] = mapped_column(String(30))
    imgurl: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    visits: Mapped[list["Visit"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    orderItems: Mapped[list["OrderItem"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

# 一次下单的信息. 包括订单进度.
class Order(Base):
    '''
    4. Order表
    Order <- User
    Order -> OrderItem
    '''
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True)
    receiverAddress: Mapped[str] = mapped_column(String(30))
    receiverName: Mapped[str] = mapped_column(String(30))
    receiverPhone: Mapped[str] = mapped_column(String(30))
    payExpressState: Mapped[str] = mapped_column(String(30))
    createTime: Mapped[str] = mapped_column(String(30))
    finishTime: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))

    user: Mapped['User'] = relationship(back_populates="orders")

    orderItems: Mapped[list["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


# 一次下单的包括的东西
class OrderItem(Base):
    '''
    5. OrderItem表
    OrderItem <- Order
    OrderItem <- Product
    '''
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    orderId: Mapped[str] = mapped_column(String(30))
    productId: Mapped[str] = mapped_column(String(30))
    buyNum: Mapped[Optional[str]]
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    order: Mapped['Order'] = relationship(back_populates="orderItems") 
    product: Mapped['Product'] = relationship(back_populates="orderItems")
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Visit(Base):
    '''
    6. Visit表
    Visit <- User
    Visit <- Product
    '''
    __tablename__ = "visit"

    id: Mapped[int] = mapped_column(primary_key=True)
    productId: Mapped[str] = mapped_column(String(30))
    visitTime: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"))

    user: Mapped['User'] = relationship(back_populates="visits") 
    product: Mapped['Product'] = relationship(back_populates="visits")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

def createAll():
    Base.metadata.create_all(engine)
