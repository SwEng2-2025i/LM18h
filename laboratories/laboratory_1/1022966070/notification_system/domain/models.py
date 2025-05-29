from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

class ChannelType(Enum):
    EMAIL = auto()
    SMS = auto()
    CONSOLE = auto()
    PUSH = auto()

class NotificationPriority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

@dataclass
class User:
    name: str
    preferred_channel: ChannelType  # Now ChannelType is defined above
    available_channels: List[ChannelType]

@dataclass
class Notification:
    user_name: str
    message: str
    priority: NotificationPriority
    status: Optional[str] = None
    delivered_via: Optional[ChannelType] = None  # Now ChannelType is defined