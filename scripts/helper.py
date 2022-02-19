import logging
import os

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

xlog = logging.getLogger()


def execute_or_fatal(cmd):
    xlog.debug('execute: {}'.format(cmd))
    ret = os.system(cmd)
    if ret != 0:
        xlog.error('result is {}'.format(ret))
        exit(ret)