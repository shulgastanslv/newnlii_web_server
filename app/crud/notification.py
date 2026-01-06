from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.notification import Notification
from app.schemas.notification import (
    NotificationCreate,
    NotificationOut,
)

def create_notification(db: Session, data: NotificationCreate) -> NotificationOut:
    db_obj = Notification(
        user_id=data.user_id,
        project_id=data.project_id,
        title=data.title,
        message=data.message,
        type=data.type,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return NotificationOut.model_validate(db_obj)

def get_notification_by_id(db: Session, notif_id: int) -> NotificationOut:
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    return NotificationOut.model_validate(notif)

def get_notifications_for_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    only_unread: bool = False,
) -> List[NotificationOut]:
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if only_unread:
        query = query.filter(Notification.is_read == False)

    notifications = (
        query.order_by(Notification.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [NotificationOut.model_validate(n) for n in notifications]

def mark_notification_read(
    db: Session,
    notif_id: int,
    is_read: bool = True,
) -> NotificationOut:
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    notif.is_read = is_read
    db.commit()
    db.refresh(notif)
    return NotificationOut.model_validate(notif)


def mark_all_user_notifications_read(db: Session, user_id: int) -> int:
    query = db.query(Notification).filter(
        Notification.user_id == user_id,
        Notification.is_read == False,
    )
    updated = query.update({"is_read": True}, synchronize_session=False)
    db.commit()
    return updated


def delete_notification(db: Session, notif_id: int) -> None:
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if not notif:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )
    db.delete(notif)
    db.commit()
