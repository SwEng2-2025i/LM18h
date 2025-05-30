from abc import ABC, abstractmethod
import logging
import random

logger = logging.getLogger(__name__)


class Channel(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        pass

class EmailChannel(Channel):
    def send(self, message: str) -> bool:
        success = random.choice([True, False])
        logger.info(f"Email send {'success' if success else 'fail'}: {message}")
        return success

class SMSChannel(Channel):
    def send(self, message: str) -> bool:
        success = random.choice([True, False])
        logger.info(f"SMS send {'success' if success else 'fail'}: {message}")
        return success

class ConsoleChannel(Channel):
    def send(self, message: str) -> bool:
        success = random.choice([True, False])
        logger.info(f"Console send {'success' if success else 'fail'}: {message}")
        return success
