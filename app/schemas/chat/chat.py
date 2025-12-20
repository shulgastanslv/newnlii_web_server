from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.user import UserOut


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    chat_id: int


class MessageOut(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    created_at: datetime
    is_read: int
    sender: Optional[UserOut] = None
    
    model_config = {
        "from_attributes": True
    }


class ChatBase(BaseModel):
    user1_id: int
    user2_id: int


class ChatCreate(ChatBase):
    pass


class ChatOut(ChatBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user1: Optional[UserOut] = None
    user2: Optional[UserOut] = None
    messages: Optional[List[MessageOut]] = None
    
    model_config = {
        "from_attributes": True
    }


class ChatListOut(BaseModel):
    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_message: Optional[MessageOut] = None
    unread_count: int = 0
    other_user: Optional[UserOut] = None
    
    model_config = {
        "from_attributes": True
    }


class WebSocketMessage(BaseModel):
    type: str
    chat_id: int
    sender_id: int
    content: Optional[str] = None
    message_id: Optional[int] = None

