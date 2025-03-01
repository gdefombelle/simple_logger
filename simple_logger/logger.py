# simple_logger.py
import logging
import os
import sys
import datetime
from logging.handlers import TimedRotatingFileHandler
from typing import Optional

import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

LOG_DIR = os.getenv("LOG_DIR", "E:\LOG_DIR")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

os.makedirs(LOG_DIR, exist_ok=True)


def get_log_file_path():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"{today}.log")


class SimpleLogger:
    def __init__(self, name: str, level: Optional[str] = None):
        self.name = name
        self.logger = logging.getLogger(name)
        if not self.logger.hasHandlers():
            self._configure_logger(level or LOG_LEVEL)

    def _configure_logger(self, level: str):
        log_file = get_log_file_path()

        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

        file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(ColoredFormatter())

        self.logger.setLevel(level)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, level, message, **kwargs):
        context = " ".join(f"{k}={v}" for k, v in kwargs.items())
        if context:
            message = f"{message} | {context}"
        self.logger.log(level, message)

    def info(self, message, **kwargs):
        self.log(logging.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        self.log(logging.WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        self.log(logging.ERROR, message, **kwargs)

    def critical(self, message, **kwargs):
        self.log(logging.CRITICAL, message, **kwargs)

    async def alog(self, level, message, **kwargs):
        self.log(level, message, **kwargs)

    async def ainfo(self, message, **kwargs):
        await self.alog(logging.INFO, message, **kwargs)

    async def awarning(self, message, **kwargs):
        await self.alog(logging.WARNING, message, **kwargs)

    async def aerror(self, message, **kwargs):
        await self.alog(logging.ERROR, message, **kwargs)

    async def acritical(self, message, **kwargs):
        await self.alog(logging.CRITICAL, message, **kwargs)


class ColoredFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        base_message = super().format(record)
        return f"{color}{base_message}{Style.RESET_ALL}"


_loggers = {}


def get_logger(name: str, level: Optional[str] = None) -> SimpleLogger:
    if name not in _loggers:
        _loggers[name] = SimpleLogger(name, level)
    return _loggers[name]
