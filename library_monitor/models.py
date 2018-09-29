from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from .config import NOTICE_COUNTER


Base = declarative_base()


class Location(Base):
    """
    Table `location`"""
    __tablename__ = 'location'
    name = Column(String(32), primary_key=True)

    def __repr__(self):
        return f"<Location(id='{self.id}', name='{self.name}')>"


class Chat(Base):
    """
    Table `chat`"""
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return f"<Chat(id='{self.id}')>"


class Book(Base):
    """
    Table `book`"""
    __tablename__ = 'book'
    id = Column(String(20), primary_key=True)
    name = Column(String(32))
    location = Column(String(32), ForeignKey('location.name'), primary_key=True)
    chat_id = Column(Integer, ForeignKey('chat.id'), primary_key=True)
    notice_counter = Column(Integer, default=NOTICE_COUNTER)

    def __repr__(self):
        return f"<Book(id='{self.id}', name='{self.name}', " \
            + f"location='{self.location}', chat='{self.chat_id}', notice_counter='{self.notice_counter}')>"
