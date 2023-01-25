import logging
import time

RUN_LEVEL_DEBUG = 1
RUN_LEVEL_DEBUG2 = 2
RUN_LEVEL_PRE_RELEASE = 3
RUN_LEVEL_RELEASE = 4
RUN_LEVEL = RUN_LEVEL_DEBUG2

MAIN_LOGGER_NAME = "INDEGO_MFC"
logger = logging.getLogger(MAIN_LOGGER_NAME)
if RUN_LEVEL <= RUN_LEVEL_DEBUG2:
    logger.setLevel(logging.DEBUG)
elif RUN_LEVEL == RUN_LEVEL_PRE_RELEASE:
    logger.setLevel(logging.INFO)
elif RUN_LEVEL == RUN_LEVEL_RELEASE:
    logger.setLevel(logging.WARNING)

# add stream handler
FORMAT = "%(asctime)s - [%(levelname)s]  %(message)s (%(filename)s(%(lineno)d):%(funcName)s())"
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(stream_handler)

if RUN_LEVEL >= RUN_LEVEL_PRE_RELEASE:
    # add file_handler
    t0 = time.localtime()
    log_file_name = "../log/log_{0:04d}{1:02d}{2:02d}{3:02d}{4:02d}.log".format(
        t0.tm_year, t0.tm_mon, t0.tm_mday, t0.tm_hour, t0.tm_min)
    file_handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s | %(message)s (%(filename)s(%(lineno)d):%(funcName)s())')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

