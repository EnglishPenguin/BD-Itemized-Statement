from loguru import logger

# Create Logger file

try:
     logger.remove(0)
except:
     pass
finally:
      logger.add(
        "\\\\NT2KWB972SRV03\\SHAREDATA\\CPP-Data\\Sutherland RPA\\BD IS Printing\\Logs\\{time:YYYY-MM-DD}.log",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} - {message}",
        colorize=True, backtrace=True, diagnose=True, level='INFO', retention='90 days'
        )