
import asyncio
from logger import get_logger

def test_sync_logging():
    logger = get_logger("test_logger")
    
    logger.info("Test INFO log", context="sync_test", step=1)
    logger.warning("Test WARNING log", context="sync_test", step=2)
    logger.error("Test ERROR log", context="sync_test", step=3)
    logger.critical("Test CRITICAL log", context="sync_test", step=4)

async def test_async_logging():
    logger = get_logger("test_logger")
    
    await logger.ainfo("Test ASYNC INFO log", context="async_test", step=1)
    await logger.awarning("Test ASYNC WARNING log", context="async_test", step=2)
    await logger.aerror("Test ASYNC ERROR log", context="async_test", step=3)
    await logger.acritical("Test ASYNC CRITICAL log", context="async_test", step=4)

def run_tests():
    print("=== Running sync logs ===")
    test_sync_logging()
    
    print("\n=== Running async logs ===")
    asyncio.run(test_async_logging())

if __name__ == "__main__":
    run_tests()
