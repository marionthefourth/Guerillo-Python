class TimeoutException(Exception):  # Custom exception class
    @staticmethod
    def handle(signum, frame):  # Custom signal handler
        raise TimeoutException



