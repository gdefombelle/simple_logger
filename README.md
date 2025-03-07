# SimpleLogger

SimpleLogger is a lightweight, easy-to-use Python logging utility designed to provide:

- Colored console logs (inspired by Loguru)
- Clean and structured log files (without ANSI color codes)
- Automatic daily log file rotation (filename includes the date)
- Optional enriched logs with dynamic context (request_id, user_id, etc.)
- Full support for both **synchronous and asynchronous** logging
- Custom "SUCCESS" log level

## Key Features

- ✅ Minimal setup — works out of the box
- ✅ No external dependencies (only standard library and colorama)
- ✅ Automatic file creation with date-based naming
- ✅ Beautiful colored console output
- ✅ Simple kwargs-based enrichment for contextual information
- ✅ Async-ready for FastAPI, Celery, or other async frameworks

## Installation

To use SimpleLogger, just copy `simple_logger.py` into your project.

```bash
# Add to your project structure
my_project/
├── simple_logger.py
└── your_app.py
```

## Usage

### Basic Example

```python
from simple_logger import get_logger

logger = get_logger("my_service")

logger.info("Service started", version="1.0", env="prod")
logger.success("Connected to database", db_host="db.local")
logger.warning("Cache miss", key="user:42")
logger.error("Unhandled exception", error="ConnectionError")
```

### Async Example (FastAPI, Celery, etc.)

```python
from simple_logger import get_logger

logger = get_logger("async_service")

async def process():
    await logger.ainfo("Async task started", task_id="12345")
    await logger.asuccess("Task completed", task_id="12345")
```

### File Rotation & Naming

- Logs are stored in the directory set by the environment variable `LOG_DIR` (default: `logs`).
- Files are automatically named using this pattern:  
    `service_name_YYYY-MM-DD.log`

- Examples:
    - `logs/my_service_2025-03-06.log`
    - `logs/default_2025-03-06.log`

### Enriched Logging

You can pass any key-value pairs as **kwargs**, and they will be automatically included in the log message.

```python
logger.info("User login successful", user_id=42, ip="192.168.1.10")
# Output: User login successful | user_id=42 ip=192.168.1.10
```

### Log Levels

| Level | Method | Async Method |
|---|---|---|
| INFO | `logger.info()` | `await logger.ainfo()` |
| WARNING | `logger.warning()` | `await logger.awarning()` |
| ERROR | `logger.error()` | `await logger.aerror()` |
| CRITICAL | `logger.critical()` | `await logger.acritical()` |
| SUCCESS (custom) | `logger.success()` | `await logger.asuccess()` |

### Console Output Example

```
2025-03-06 22:15:32.123 | INFO     | my_service:app.py:main:42 - Service started | version=1.0 env=prod
2025-03-06 22:15:32.124 | SUCCESS  | my_service:app.py:main:43 - Connected to database | db_host=db.local
```

---

## License

MIT License - free to use and modify.
