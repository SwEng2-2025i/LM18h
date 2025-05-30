from .channel_factory import ChannelFactory
from .logger import Logger
import logging

logger = logging.getLogger(__name__)

class NotificationHandler:
    def __init__(self, channels: list[str]):
        self.channels = channels
        self.logger = Logger.get_instance()

    def notify(self, message: str) -> bool:
        attempts_log = []  # se guarda cada intento

        for ch_name in self.channels:
            channel = ChannelFactory.get_channel(ch_name)
            success = channel.send(message)
            status = "Success" if success else "Fail"
            log_message = f"Attempt to send via {ch_name}: {status}"

            self.logger.log(log_message)
            logger.info(log_message)  

            attempts_log.append({"channel": ch_name, "status": status})

            if success:
                break  # Salimos al primer éxito

        self.last_attempts = attempts_log  # ← Guardamos los intentos
        return any(a["status"] == "Success" for a in attempts_log)
