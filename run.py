#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
import os
from pathlib import Path
from library_monitor.config import BOT_TOKEN, LOG_FLODER, TARGET_BOOKS
from library_monitor.mess import set_logger
from library_monitor.monitor import LibraryMonitor


def main():
    """
    Main process."""
    log_path = Path(LOG_FLODER, str(os.getpid()))
    if not log_path.exists():
        log_path.mkdir(parents=True)
    set_logger(Path(log_path, 'LibraryMonitor.log'))
    monitor = LibraryMonitor(bot_token=BOT_TOKEN, target_books=TARGET_BOOKS)
    monitor.run()
    monitor.stop()
    logging.warning("LibraryMonitor: Exits.")


if __name__ == '__main__':
    main()
