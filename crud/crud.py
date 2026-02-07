from db.model import Chat, Message
from sqlalchemy.orm import Session
from model.chat import ChatDto, MessageDto

class ChatCrud:
    def __init__(self, session: Session):
        self.session = session
        
    def create_chat(self, name: str, phone: str) -> Chat:
        new_chat = Chat(name=name, phone=phone)
        self.session.add(new_chat)
        self.session.commit()
        return new_chat

class MessageCrud:
    def __init__(self, session: Session):
        self.session = session
        
    def create_message(self, messageDto: MessageDto, chat: Chat) -> Message:
        new_message = Message(
            type=messageDto.type,
            text=messageDto.text,
            status=messageDto.status,
            date=messageDto.date,
            from_me=messageDto.from_me,
            chat=chat
        )
        self.session.add(new_message)
        self.session.commit()