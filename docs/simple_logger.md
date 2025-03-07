# SimpleLogger - Full Documentation

## Overview

`SimpleLogger` is a lightweight Python logging utility designed to simplify logging for small to medium projects, while providing:

- ✅ Beautiful **colored logs in the console** (inspired by Loguru).
- ✅ **Clean, plain-text logs in files**, ready for processing (no ANSI color codes).
- ✅ Automatic **daily log file rotation**, with the date embedded in the filename.
- ✅ **Synchronous and asynchronous log methods** (perfect for FastAPI, Celery, etc.).
- ✅ A custom `SUCCESS` log level to log key positive events.
- ✅ Easy **log enrichment** by passing contextual key-value pairs.

---

## Installation

No dedicated package yet. To use `SimpleLogger`, simply copy `simple_logger.py` into your project.

Example project structure:

```
my_project/
├── simple_logger.py
├── main.py
```

No external dependencies are required, except for:

- `colorama` (pre-installed in many environments)

---

## Log Storage & Rotation

### Log Directory

The directory where logs are saved is defined by the environment variable:

```
LOG_DIR
```

- If `LOG_DIR` is set, logs go there.
- If not set, logs are saved in a directory called `logs` in the current working directory.

### Daily Rotation

Each log file includes the current date in its name:

```
<logger_name>_YYYY-MM-DD.log
```

This ensures:

- Automatic daily file rotation.
- Clear separation of logs per day.

---

## Basic Usage

### Creating a Logger

```python
from simple_logger import get_logger

logger = get_logger("my_service")
```

### Logging Messages

```python
logger.info("Service started", version="1.0", env="production")
logger.success("Connected to database", host="db.local")
logger.error("Connection failed", error="Timeout")
```

---

## Supported Log Levels

| Level | Description | Sync Method | Async Method |
|---|---|---|---|
| INFO | Standard information message | `logger.info()` | `await logger.ainfo()` |
| SUCCESS | Custom positive event message | `logger.success()` | `await logger.asuccess()` |
| WARNING | Warnings | `logger.warning()` | `await logger.awarning()` |
| ERROR | Errors | `logger.error()` | `await logger.aerror()` |
| CRITICAL | Critical errors | `logger.critical()` | `await logger.acritical()` |

---

## Enriched Contextual Logging

You can pass any number of key-value pairs when logging. These will automatically be appended to the log message.

```python
logger.info("User login successful", user_id=123, ip="192.168.1.100")
```

---

## Async Logging

All log methods have async versions, making `SimpleLogger` compatible with FastAPI, Celery, and other async frameworks.

```python
await logger.ainfo("Background job started", job_id="abc123")
```

---

## Architecture

- Each logger instance is cached using `name` + `log_file` as the key.
- A logger always has **two handlers**:
    - **Console handler** (colored output).
    - **File handler** (plain output).

---

## License

MIT License - Free to use, modify, and distribute.
