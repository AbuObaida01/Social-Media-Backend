from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

class Post(Base):
    __tablename__ = 'posts'

    # Old method of defining columns

    # id=Column(Integer, primary_key=True, nullable=False)
    # title=Column(String, nullable=False)
    # content=Column(String, nullable=False)
    # published=Column(Boolean, default=True)

    #new method of defining columns

    id: Mapped[int]=mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str]=mapped_column(String, nullable=False)
    content: Mapped[str]=mapped_column(String, nullable=False)
    published: Mapped[bool]=mapped_column(Boolean, server_default='TRUE')
    created_at: Mapped[TIMESTAMP]=mapped_column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id: Mapped[int]=mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner=relationship("User")

class User(Base):
    __tablename__='users'
    id: Mapped[int]=mapped_column(Integer, primary_key=True, nullable=False)
    email: Mapped[str]=mapped_column(String,nullable=False, unique=True)
    password: Mapped[str]=mapped_column(String, nullable=False)
    created_at: Mapped[TIMESTAMP]=mapped_column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    phone_no: Mapped[str]=mapped_column(String,nullable=False,unique=True)

class Votes(Base):
    __tablename__='votes'
    user_id : Mapped[int]=mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id : Mapped[int]=mapped_column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)