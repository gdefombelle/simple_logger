import logging
import os
import sys
import datetime
import re
import unicodedata
from typing import Optional
from logging.handlers import TimedRotatingFileHandler
from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

SUCCESS_LEVEL = 25
logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

LOG_DIR = os.getenv("LOG_DIR", "/var/log/pytune")
_loggers = {}

# ────────────── SLUGIFY ────────────── #

def slugify(value: str) -> str:
    value = unicodedata.normalize('NFKD', value)
    value = value.encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s\-]+", "_", value)

def get_log_file_path(name: Optional[str], log_file: Optional[str]) -> str:
    logger_name = slugify(name or "default")
    base_name = slugify(log_file or logger_name)
    log_dir = os.path.join(LOG_DIR, logger_name)
    os.makedirs(log_dir, exist_ok=True)
    return os.path.join(log_dir, f"{base_name}.log")  # sans date → rotation la gère

# ────────────── LOGGER ────────────── #

class SimpleLogger:
    def __init__(self, name: Optional[str] = None, log_file: Optional[str] = None):
        self.name = name or "default"
        self.log_file = log_file
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.DEBUG)

        if not self._has_custom_handlers():
            self._configure_logger()

    def _has_custom_handlers(self):
        return any(
            isinstance(h, (logging.FileHandler, logging.StreamHandler))
            for h in self.logger.handlers
        )

    def _configure_logger(self):
        log_file_path = get_log_file_path(self.name, self.log_file)

        # 📁 Handler avec rotation
        file_handler = TimedRotatingFileHandler(
            filename=log_file_path,
            when="midnight",
            interval=1,
            backupCount=14,
            encoding="utf-8",
            utc=True
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(LoguruPlainFormatter(self.name))

        # 🎨 Console handler coloré
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(LoguruLikeFormatter(self.name))

        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)

        print(f"[SimpleLogger] Logging to: {log_file_path} (rotated daily, 14 backups)", flush=True)

    def log(self, level, message, **kwargs):
        self.logger.log(level, self._enrich_message(message, **kwargs))

    async def alog(self, level, message, **kwargs):
        self.log(level, message, **kwargs)

    def success(self, message, **kwargs): self.log(SUCCESS_LEVEL, message, **kwargs)
    def info(self, message, **kwargs): self.log(logging.INFO, message, **kwargs)
    def debug(self, message, **kwargs): self.log(logging.DEBUG, message, **kwargs)
    def warning(self, message, **kwargs): self.log(logging.WARNING, message, **kwargs)
    def error(self, message, **kwargs): self.log(logging.ERROR, message, **kwargs)
    def critical(self, message, **kwargs): self.log(logging.CRITICAL, message, **kwargs)

    async def asuccess(self, message, **kwargs): await self.alog(SUCCESS_LEVEL, message, **kwargs)
    async def ainfo(self, message, **kwargs): await self.alog(logging.INFO, message, **kwargs)
    async def awarning(self, message, **kwargs): await self.alog(logging.WARNING, message, **kwargs)
    async def aerror(self, message, **kwargs): await self.alog(logging.ERROR, message, **kwargs)
    async def acritical(self, message, **kwargs): await self.alog(logging.CRITICAL, message, **kwargs)

    def _enrich_message(self, message, **kwargs):
        if kwargs:
            return f"{message} | " + " ".join(f"{k}={v}" for k, v in kwargs.items())
        return message

# ────────────── FORMATTERS ────────────── #

class LoguruLikeFormatter(logging.Formatter):
    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        SUCCESS_LEVEL: Fore.CYAN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def __init__(self, logger_name):
        super().__init__()
        self.logger_name = logger_name

    def format(self, record):
        color = self.LEVEL_COLORS.get(record.levelno, Fore.WHITE)
        return self._format_message(record, color)

    def _format_message(self, record, color):
        record_file = os.path.basename(record.pathname)
        location = f"{record_file}:{record.funcName}:{record.lineno}"
        timestamp = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        level = record.levelname.ljust(8)
        message = record.getMessage()
        return f"{color}{timestamp} | {level} | {self.logger_name}:{location} - {message}{Style.RESET_ALL}"

class LoguruPlainFormatter(LoguruLikeFormatter):
    def format(self, record):
        return self._format_message(record, "")

# ────────────── ENTRYPOINT ────────────── #

def get_logger(name: Optional[str] = None, log_file: Optional[str] = None) -> SimpleLogger:
    key = (name or "default", log_file)
    if key not in _loggers:
        _loggers[key] = SimpleLogger(name, log_file)
    return _loggers[key]
