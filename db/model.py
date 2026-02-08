from typing import List
from sqlalchemy import ForeignKey, Text, Integer, Enum as SqlEnum, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from enums.status_enum import StatusEnum
from enums.message_enum import MessageType


class Base(DeclarativeBase):
    pass

class Chat(Base):
    __tablename__ = "chats"
    
    chat_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
    phone: Mapped[str] = mapped_column(Text)
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="chat")
    
class Message(Base):
    __tablename__ = "messages"
    
    message_id = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[MessageType] = mapped_column(SqlEnum(MessageType))
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[StatusEnum] = mapped_column(SqlEnum(StatusEnum))
    date: Mapped[str] = mapped_column(Text, nullable=True)
    from_me: Mapped[bool] = mapped_column(Boolean)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.chat_id"))
    time_stamp: Mapped[str] = mapped_column(Text, nullable=True)
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
