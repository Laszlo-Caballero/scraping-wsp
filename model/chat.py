from dataclasses import dataclass
from enums.message_enum import MessageType
from enums.status_enum import StatusEnum


@dataclass
class ChatDto:
    name: str
    phone: str
    
@dataclass
class MessageDto:
    type: MessageType
    text: str
    status: StatusEnum
    date: str
    from_me: bool = True
    time_stamp: str = None