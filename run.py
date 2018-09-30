#!/usr/env/python3
# -*- coding: UTF-8 -*-

import logging
import os
import time
from pathlib import Path
from library_monitor.config import BOT_TOKEN, LOG_FLODER, REPORT_CYCLE, SYNC_INTERVAL
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
    interval_counter = 0
    while True:
        interval_counter += 1
        monitor.run()
        if interval_counter == REPORT_CYCLE:
            monitor.report_status()
            interval_counter = 0
        logging.info(f"LibraryMonitor: Sleep for `{SYNC_INTERVAL}`s.")
        time.sleep(SYNC_INTERVAL)
    monitor.stop()
    logging.warning("LibraryMonitor: Exits.")


if __name__ == '__main__':
    main()
