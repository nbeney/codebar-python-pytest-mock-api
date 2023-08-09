import logging

logging.basicConfig(level=logging.DEBUG)


class DemoApiClient:
    logger = logging.getLogger("DemoApiClient")

    def __init__(self):
        DemoApiClient.logger.debug("__init__")

    def send(self, msg):
        DemoApiClient.logger.debug(f"send {msg}")

    def connect(self):
        DemoApiClient.logger.debug("connect")

    def close(self):
        DemoApiClient.logger.debug("close")


def send_message(msg):
    client = DemoApiClient()
    client.connect()
    client.send(msg)
    client.close()


if __name__ == "__main__":
    send_message("foo")
    send_message("bar")
