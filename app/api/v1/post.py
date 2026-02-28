from http.client import HTTPException
import random
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import post as crud_post
from typing import List, Optional
from app.schemas.post import PostCreate, PostOut, SavedPostOut

router = APIRouter()

@router.get("/", response_model=List[PostOut])
def get_all_posts_route(
    skip: int = Query(0, description="Skip N posts", ge=0),
    limit: int = Query(100, description="Limit results", ge=1, le=500),
    db: Session = Depends(get_db)
):
    posts = crud_post.get_posts(db)
    return posts[skip:skip + limit]


@router.get("/{post_id}", response_model=PostOut)
def get_post_by_id_route(
    post_id: int = Path(..., description="ID поста", ge=1), 
    db: Session = Depends(get_db)
):
    return crud_post.get_post_by_id(db, post_id)

@router.post("/", response_model=PostOut, status_code=201)
def create_post_route(
    post: PostCreate, 
    db: Session = Depends(get_db)
):
    try:
        print(post)
        return crud_post.create_post(post, db)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/saved/{post_id}", status_code=201)
def save_post_route(
    post_id: int = Path(..., description="ID поста для сохранения", ge=1),
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    post = crud_post.get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )
    
    return crud_post.save_post(post_id, user_id, db)


@router.delete("/saved/{post_id}", status_code=200)
def unsave_post_route(
    post_id: int = Path(..., description="ID поста для удаления из сохраненных", ge=1),
    user_id: int = Query(..., description="ID пользователя"),
    db: Session = Depends(get_db)
):
    return crud_post.delete_saved_post(post_id, user_id, db)

@router.get("/saved/user/{user_id}", response_model=List[SavedPostOut])
def get_user_saved_posts_route(
    user_id: int = Path(..., description="ID пользователя", ge=1),
    skip: int = Query(0, description="Skip N saved posts", ge=0),
    limit: int = Query(100, description="Limit results", ge=1, le=500),
    db: Session = Depends(get_db)
):
    return crud_post.get_user_saved_posts(user_id, db, skip, limit)

@router.get("/saved/check/{post_id}", response_model=dict)
def check_post_saved_route(
    post_id: int = Path(..., description="ID поста для проверки", ge=1),
    user_id: int = Query(..., description="ID пользователя"), 
    db: Session = Depends(get_db)
):
    is_saved = crud_post.is_post_saved_by_user(post_id, user_id, db)
    return {
        "post_id": post_id,
        "user_id": user_id,
        "is_saved": is_saved
    }


@router.get("/tags/popular", response_model=List[dict])
def get_popular_tags_route(
    limit: int = Query(10, description="Количество популярных тегов", ge=1, le=50),
    min_posts: int = Query(1, description="Минимальное количество постов с тегом", ge=1),
    db: Session = Depends(get_db)
):
    """
    Get popular tags based on usage count in posts
    Returns list of tags with their post count
    """
    try:
       return crud_post.get_popular_tags(limit, min_posts, db)         
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching popular tags: {str(e)}"
        )


@router.get("/daily/random", response_model=PostOut)
def get_random_post_route(
    db: Session = Depends(get_db),
    exclude_post_id: Optional[int] = Query(None, description="ID поста для исключения"),
    category: Optional[str] = Query(None, description="Фильтр по категории")
):
    """
    Get a random post for the "Post of the Day" feature
    """
    try:
        # Получаем все посты
        posts = crud_post.get_posts(db)
        
        if not posts:
            raise HTTPException(
                status_code=404,
                detail="No posts available"
            )
        
        # Фильтруем посты
        filtered_posts = posts
        
        # Исключаем конкретный пост если нужно
        if exclude_post_id:
            filtered_posts = [p for p in filtered_posts if p.id != exclude_post_id]
        
        # Фильтруем по категории
        if category:
            filtered_posts = [p for p in filtered_posts if p.category and p.category.lower() == category.lower()]
        
        if not filtered_posts:
            # Если после фильтрации нет постов, возвращаем любой
            filtered_posts = posts
        # Выбираем случайный пост
        random_post = random.choice(filtered_posts)
        
        return random_post
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching random post: {str(e)}"
        )


