import functools
import logging
from contextlib import contextmanager
from typing import Callable, List
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import joinedload, relationship, scoped_session, sessionmaker
from sqlalchemy.orm.session import Session
from .config import DATABASE_URI
from .models import Base, Book, Chat, Location


class SQLManager(object):
    """Manager sessions.

    :member session_maker: Attached :obj: sessionmaker.
    :type session_maker: :obj:sessionmaker.
    """

    def __init__(self):
        Chat.books = relationship("Book")
        engine = create_engine(DATABASE_URI)
        Base.metadata.create_all(engine)
        session_factory = sessionmaker(bind=engine)
        self.session_maker = scoped_session(session_factory)

    @contextmanager
    def create_session(self):
        """Create session to talk to database, rollback and raise error if failed.
        """
        session = self.session_maker
        try:
            yield session
        except Exception as identifier:
            logging.exception(identifier)
            session.rollback()
            raise identifier
        finally:
            session.close()
            self.session_maker.remove()


def load_session(func: Callable):
    """Load new session and add session as the first argument of `func`.

    :param func: Target function.
    :type func: function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kw):
        """See `load_session`
        """
        with args[0].sql_manager.create_session() as my_session:
            return func(my_session, *args[1:], **kw)
    return wrapper


class SQLHandler(object):
    """Handler for SQL requests.
    """

    def __init__(self, sql_manager=None):
        self.sql_manager = sql_manager

    @load_session
    def get_chats(my_session: Session) -> List[Chat]:
        return my_session.query(Chat).options(joinedload('books')).all()

    @load_session
    def count_notice(my_session: Session, target_book: Book):
        """
        Decrease `notice_counter` by 1 and
        delete reocrd if `notice_counter` is 0."""
        online_book = my_session.query(Book).filter(Book.id == target_book.id).filter(
            Book.location == target_book.location).filter(Book.chat_id == target_book.chat_id).one()
        online_book.notice_counter -= 1
        if online_book.notice_counter == 0:
            logging.warning(f"LibraryMonitor: Delete book `{target_book}`")
            my_session.delete(online_book)
        my_session.commit()

    @load_session
    def add_book(my_session: Session, book_id: str, book_name: str, chat_id: int, location: str) -> bool:
        if my_session.query(exists().where(Chat.id == chat_id)).scalar() is not None and \
                my_session.query(exists().where(Location.name == location)).scalar() is not None and \
                my_session.query(Book).filter(Book.id == book_id).filter(
                        Book.location == location).filter(Book.chat_id == chat_id).scalar() is None:
            # such chat exists
            new_book = Book(name=book_name, id=book_id,
                            location=location, chat_id=chat_id)
            my_session.add(new_book)
            my_session.commit()
            return True
        else:
            return False
