

import logging
class LogWrapper(object):
    """
    Wrapper around the logger to flush() after every write because java is just
    plain weird with when it decides to flush to disk
    """
    def __init__(self):
        _logger = logging.getLogger('simple_example')
        fh = logging.FileHandler('c:\\tmp\\myapp.log')
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)

        _logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.DEBUG)
        _logger.addHandler(fh)

        self._logger = _logger
        self._fh = fh

    def flush(self):
        self._fh.flush()

    def debug(self, msg):
        self._logger.debug(msg)
        self.flush()

    def warn(self, msg):
        self._logger.warn(msg)
        self.flush()

    def info(self, msg):
        self._logger.info(msg)
        self.flush()

    def error(self, msg):
        self._logger.error(msg)
        self.flush()
