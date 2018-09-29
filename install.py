#!/usr/env/python3
# -*- coding: UTF-8 -*-

import json
import logging
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from library_monitor.config import DATABASE_FOLDER, DATABASE_PATH, DATABASE_URI, LOG_FLODER
from library_monitor.mess import get_current_time, set_logger
from library_monitor.models import Base, Book, Chat, Location


def initialize_database():
    """
    Assume database folder exists"""
    log_path = Path(LOG_FLODER, f'LibraryMonitor_{os.getpid()}.log')
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True)
    set_logger(log_path)
    if DATABASE_PATH.exists():
        backup_path = str(DATABASE_PATH) + f".{get_current_time()}"
        logging.warning(f'Rename old database to `{backup_path}`.')
        os.rename(DATABASE_PATH, backup_path)
    tables = [Book, Chat, Location]
    Chat.books = relationship("Book")
    engine = create_engine(DATABASE_URI)
    Base.metadata.create_all(engine)
    SessionMaker = sessionmaker(bind=engine)
    session = SessionMaker()
    for table in tables:
        logging.info(f'Importing table `{table.__name__}`.')
        with open(Path(DATABASE_FOLDER, f'{table.__name__}.json'), encoding="utf8") as json_file:
            for record in json.load(json_file):
                session.add(table(**record))
    session.commit()
    logging.warning(f'Import finished`.')


if __name__ == '__main__':
    initialize_database()
