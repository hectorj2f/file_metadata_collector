
""" 
File_Metadata_Collector logger: It is totally independent of the general logger

@author: fernandez

""" 

import logging

logging_level = logging.ERROR
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
_inited = False

def _register_logger(logger):
  for h in handlers:
    logger.addHandler(h)

def create_logger(name):
  logger = logging.getLogger(name)
  logger.setLevel(logging_level)
  if not _inited: return logger
  _register_logger(logger)
  loggers.append(logger)
  return logger

def init(log_file):
  global _inited
  if _inited: return
  _inited = True
  global handlers, loggers
  handlers = []
  loggers = []
  file_handler = logging.FileHandler(log_file)
  file_handler.setFormatter(log_formatter)
  handlers.append(file_handler)
  