import logging
from createLogger import makeLogger

def makeLogger(logPath):
    logger = logging.basicConfig(
        filename=logPath,
        encoding="utf-8",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="{asctime} - {levelname} - {message}",
        style="{"
    )
    return logger

logger = makeLogger("main.log")