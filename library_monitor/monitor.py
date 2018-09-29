"""Monitor book state in BUPT's library, send notice if available."""

import json
import logging
from typing import List, Dict
import requests
from .config import BOOK_PAGE_REFERER, BOOK_STATE_API, MESSAGE_TEMPLATE, NOTICE_COUNTER, TARGET_STATE
from .models import Book
from .queued_bot import create_queued_bot
from .sql_handler import SQLHandler, SQLManager


class LibraryMonitor(object):
    """
    >>> self.target_books[0].keys()
    ['name', 'id', 'location']"""

    def __init__(self, bot_token: str):
        self.bot = create_queued_bot(bot_token)
        self.sql_handler = SQLHandler(SQLManager())

    @staticmethod
    def update_book_states(target_book: Book) -> List[Dict]:
        """
        Download and simplify book state dicts from server."""
        headers = {
            'Referer': BOOK_PAGE_REFERER.format(book_id=target_book.id)
        }
        params = {
            'rec_ctrl_id': target_book.id
        }
        books = []
        try:
            state_response = requests.post(
                BOOK_STATE_API, headers=headers, params=params)
            full_states = json.loads(state_response.text.split('@')[0])[0]['A']
            books = [
                {'state': current_book['circul_status'],
                 'location': current_book['guancang_dept'],
                 'due_date': current_book['due_date']}
                for current_book in full_states
                if target_book.location in current_book['guancang_dept']
                and current_book['circul_status'] == TARGET_STATE
            ]
        except Exception as identifier:
            logging.exception(identifier)
            logging.error(
                f'LibraryMonitor: Failed to update book state. (ID: {target_book.id})')
        return books

    def send_message(self, *, chat_id: int, text: str):
        """
        Send message to """
        logging.info(f"Send message: `{text}`")
        self.bot.send_message(chat_id=chat_id, text=text)

    def run(self) -> None:
        for chat in self.sql_handler.get_chats():
            for target_book in chat.books:
                logging.info(
                    f"LibraryMonitor: Updating book state. ({target_book})")
                book_states = self.update_book_states(target_book)
                book_counter = len(book_states)
                if book_counter > 0:
                    logging.info(
                        f"LibraryMonitor: Book found. ({target_book})")
                    self.sql_handler.count_notice(target_book)
                    self.send_message(
                        chat_id=chat.id,
                        text=MESSAGE_TEMPLATE.format(
                            book_location=book_states[0]['location'],
                            book_name=target_book.name,
                            book_id=target_book.id,
                            book_counter=book_counter,
                            notice_index=NOTICE_COUNTER - target_book.notice_counter + 1,
                            max_notice_index=NOTICE_COUNTER))
                else:
                    logging.info(
                        f"LibraryMonitor: Book NOT found. ({target_book})")

    def stop(self):
        """
        Stop bot and return."""
        self.bot.stop()
