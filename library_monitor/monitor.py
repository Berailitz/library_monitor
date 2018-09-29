"""Monitor book state in BUPT's library, send notice if available."""

import json
import logging
from typing import List, Dict
import requests
from .config import BOOK_PAGE_REFERER, BOOK_STATE_API, CHAT_IDS, MESSAGE_TEMPLATE, TARGET_STATE
from .queued_bot import create_queued_bot


class LibraryMonitor(object):
    """
    >>> self.target_books[0].keys()
    ['name', 'id', 'location']"""

    def __init__(self, bot_token: str, target_books: List[Dict]):
        self.bot = create_queued_bot(bot_token)
        self.target_books = target_books

    @staticmethod
    def update_book_states(target_book: Dict) -> List[Dict]:
        """
        Download and simplify book state dicts from server."""
        headers = {
            'Referer': BOOK_PAGE_REFERER.format(book_id=target_book['id'])
        }
        params = {
            'rec_ctrl_id': target_book['id']
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
                if target_book['location'] in current_book['guancang_dept'] \
                    and current_book['circul_status'] == TARGET_STATE
            ]
        except Exception as identifier:
            logging.exception(identifier)
            logging.error(
                f'LibraryMonitor: Failed to update book state. (ID: {target_book["id"]})')
        return books

    def send_message(self, text: str):
        for chat_id in CHAT_IDS:
            self.bot.send_message(chat_id=chat_id, text=text)

    def run(self) -> None:
        for target_book in self.target_books:
            book_states = self.update_book_states(target_book)
            book_counter = len(book_states)
            if book_counter > 0:
                logging.info(f"LibraryMonitor: Book found. ({target_book})")
                self.send_message(MESSAGE_TEMPLATE.format(
                    book_location=book_states[0]['location'],
                    book_name=target_book['name'],
                    book_id=target_book['id'],
                    book_counter=book_counter))
            else:
                logging.info(
                    f"LibraryMonitor: Book NOT found. ({target_book})")

    def stop(self):
        """
        Stop bot and return."""
        self.bot.stop()
