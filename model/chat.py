from dataclasses import dataclass
from enums.message_enum import MessageType
from enums.status_enum import StatusEnum

@dataclass
class Chat:
    name: str
    phone: str
    messages: list[Message]
    
@dataclass
class Message:
    type: MessageType
    text: str
    status: StatusEnum
    date: str
    from_me: bool = True
    