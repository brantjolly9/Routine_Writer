import logging

def makeLogger(logPath):
    logging.basicConfig(
        filename=logPath,
        encoding="utf-8",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="{asctime} - {levelname} - {message}",
        style="{"
    )

logger = makeLogger("main.log")