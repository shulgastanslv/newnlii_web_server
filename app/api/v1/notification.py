from typing import List, Optional
from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import notification as crud_notification
from app.models.notification import NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationOut, UnreadCountOut, NotificationUpdate

router = APIRouter()

@router.get("/", response_model=List[NotificationOut])
def get_my_notifications(
    user_id: str = Query(..., description="ID пользователя, чьи уведомления получить"),
    skip: int = Query(0, ge=0, description="Пропустить N уведомлений"),
    limit: int = Query(100, ge=1, le=500, description="Лимит записей"),
    status: Optional[List[NotificationStatus]] = Query(None, description="Фильтр по статусам"),
    db: Session = Depends(get_db)
):
    return crud_notification.get_user_notifications(db, user_id, skip, limit, status)


@router.get("/unread-count", response_model=UnreadCountOut)
def get_unread_notifications_count(
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    count = crud_notification.get_unread_count(db, user_id)
    return {"user_id": user_id, "unread_count": count}


@router.patch("/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(
    notification_id: int = Path(..., description="ID уведомления", ge=1),
    user_id: str = Query(..., description="ID пользователя (владельца)"),
    db: Session = Depends(get_db)
):
    return crud_notification.mark_notification_as_read(db, notification_id, user_id)


@router.post("/read-all", status_code=status.HTTP_200_OK)
def mark_all_notifications_read(
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    updated = crud_notification.mark_all_notifications_as_read(db, user_id)
    return {"message": f"Marked {updated} notifications as read"}


@router.patch("/{notification_id}/archive", response_model=NotificationOut)
def archive_notification(
    notification_id: int = Path(..., description="ID уведомления", ge=1),
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    return crud_notification.archive_notification(db, notification_id, user_id)

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int = Path(..., description="ID уведомления", ge=1),
    user_id: str = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    crud_notification.delete_notification(db, notification_id, user_id)
    return None

@router.post("/", response_model=NotificationOut, status_code=status.HTTP_201_CREATED)
def create_notification_endpoint(
    notification_in: NotificationCreate,
    db: Session = Depends(get_db)
):
    return crud_notification.create_notification(db, notification_in)