#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#
#  Based on : https://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import time
import logging

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

logger = logging.getLogger(__name__)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        rs = method(*args, **kwargs)
        te = time.time()

        logger.debug('{0!r} ({1!r}, {2!r}) :: {3:2.5f}'.format(method.__name__, args, kwargs, te - ts))

        return rs

    return timed