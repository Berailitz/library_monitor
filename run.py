#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
import os
import time
from pathlib import Path
from library_monitor.config import BOT_TOKEN, LOG_FLODER, SYNC_INTERVEL
from library_monitor.mess import set_logger
from library_monitor.monitor import LibraryMonitor


def main():
    """
    Main process."""
    log_path = Path(LOG_FLODER, f'LibraryMonitor_{os.getpid()}.log')
    if not log_path.parent.exists():
        log_path.parent.mkdir(parents=True)
    set_logger(log_path)
    monitor = LibraryMonitor(bot_token=BOT_TOKEN)
    while True:
        monitor.run()
        logging.info(f"LibraryMonitor: Sleep for `{SYNC_INTERVEL}`s.")
        time.sleep(SYNC_INTERVEL)
    monitor.stop()
    logging.warning("LibraryMonitor: Exits.")


if __name__ == '__main__':
    main()
