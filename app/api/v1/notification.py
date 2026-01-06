from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.notification import (
    NotificationOut,
    NotificationCreate,
    NotificationUpdate,
)
from app.crud import notification as crud_notifications

router = APIRouter()


@router.post(
    "/",
    response_model=NotificationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
):
    return crud_notifications.create_notification(db, payload)


@router.post(
    "/{notification_id}/read",
    status_code=status.HTTP_200_OK,
)
def markAsRead(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return crud_notifications.mark_notification_read(
        db=db, notif_id=notification_id, is_read=True
)

@router.get(
    "/{notification_id}",
    response_model=NotificationOut,
)
def get_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    
    return crud_notifications.get_notification_by_id(db, notification_id)


@router.get(
    "/",
    response_model=List[NotificationOut],
)
def get_user_notifications(
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(50, le=100),
    only_unread: bool = False,
):
    
    return crud_notifications.get_notifications_for_user(
        db=db,
        user_id=user_id,
        skip=skip,
        limit=limit,
        only_unread=only_unread,
    )


@router.post(
    "/update/{notification_id}",
    response_model=NotificationOut,
)
def update_notification(
    notification_id: int,
    payload: NotificationUpdate,
    db: Session = Depends(get_db),
):
    
    notif = crud_notifications.get_notification_by_id(db, notification_id)
    if notif.user_id != payload.user_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="Not allowed")

    return crud_notifications.mark_notification_read(
        db=db,
        notif_id=notification_id,
        is_read=payload.is_read if payload.is_read is not None else True,
    )


@router.post(
    "/read-all",
    status_code=status.HTTP_200_OK,
)
def mark_all_read(
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db),
):
    updated = crud_notifications.mark_all_user_notifications_read(
        db=db,
        user_id=user_id,
    )
    return {"updated": updated}

@router.delete(
    "/{notification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_notification(
    notification_id: int,
    user_id: int = Query(..., description="ID пользователя-владельца уведомления"),
    db: Session = Depends(get_db),
):
    notif = crud_notifications.get_notification_by_id(db, notification_id)
    if notif.user_id != user_id:
        from fastapi import HTTPException

        raise HTTPException(status_code=403, detail="Not allowed")

    crud_notifications.delete_notification(db, notification_id)
    return
