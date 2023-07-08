from typing import List
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(50))
    post: Mapped[List["Post"]] = relationship(back_populates="user", lazy=True)

    def __init__(self, name=None, password=None):
        self.name = name
        self.password = password

    def __repr__(self):
        return f'<User {self.name!r}>'
    
class Post(Base):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    created = Column(DateTime)
    title = Column(String(25))
    body = Column(String(200))
    autor_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="post")

    def __init__(self, autor_id=None, created=None, title=None, body=None):
        self.autor_id = autor_id
        self.created = created
        self.title = title
        self.body = body