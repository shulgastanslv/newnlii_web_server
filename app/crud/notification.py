from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.post import Notification, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationUpdate


def create_notification(db: Session, notification_in: NotificationCreate) -> Notification:
    try:
        db_notification = Notification(
            user_id=notification_in.user_id,
            actor_id=notification_in.actor_id,
            post_id=notification_in.post_id,
            type=notification_in.type,
            status=notification_in.status,
            title=notification_in.title,
            content=notification_in.content,
            expires_at=notification_in.expires_at,
            created_at=datetime.utcnow()
        )
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_user_notifications(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    include_status: Optional[List[NotificationStatus]] = None
) -> List[Notification]:
    try:
        query = db.query(Notification).options(
            joinedload(Notification.actor),
            joinedload(Notification.post)
        ).filter(Notification.user_id == user_id)

        if include_status:
            query = query.filter(Notification.status.in_(include_status))

        notifications = query.order_by(Notification.created_at.desc()) \
            .offset(skip).limit(limit).all()
        return notifications
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching notifications: {str(e)}")


def get_notification_by_id(db: Session, notification_id: int) -> Notification:
    notification = db.get(Notification, notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


def mark_notification_as_read(db: Session, notification_id: int, user_id: int) -> Notification:
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found or access denied")

        if notification.status != NotificationStatus.READ:
            notification.status = NotificationStatus.READ
            notification.read_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(notification)
        return notification
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking notification as read: {str(e)}")


def mark_all_notifications_as_read(db: Session, user_id: int) -> int:
    try:
        result = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.status == NotificationStatus.UNREAD
        ).update({
            Notification.status: NotificationStatus.READ,
            Notification.read_at: datetime.now(timezone.utc)
        }, synchronize_session=False)
        db.commit()
        return result
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking all as read: {str(e)}")


def archive_notification(db: Session, notification_id: int, user_id: int) -> Notification:
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found or access denied")

        notification.status = NotificationStatus.ARCHIVED
        db.commit()
        db.refresh(notification)
        return notification
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error archiving notification: {str(e)}")


def delete_notification(db: Session, notification_id: int, user_id: int) -> None:
    try:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found or access denied")

        db.delete(notification)
        db.commit()
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting notification: {str(e)}")


def get_unread_count(db: Session, user_id: int) -> int:
    try:
        count = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.status == NotificationStatus.UNREAD
        ).count()
        return count
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error counting unread notifications: {str(e)}")