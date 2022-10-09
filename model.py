from datetime import datetime

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey, Table, MetaData
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

Base = declarative_base()


note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("quote", Integer, ForeignKey("quotes.id")),
    Column("tag", Integer, ForeignKey("tags.id")),
)


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    quotes = relationship("Quote", cascade="all, delete", backref="author")


class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10000), nullable=False)
    author_id = Column(Integer, ForeignKey(Author.id, ondelete="CASCADE"))
    tags = relationship("Tag", secondary=note_m2m_tag, backref="quotes")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25), nullable=False)


