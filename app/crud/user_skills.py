from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app.models.skill import Skill

def add_skill_to_user(db: Session, user_id: int, skill_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    print(user)
    print(skill)
    if not user or not skill:
        raise HTTPException(status_code=404, detail="User or Skill not found")

    if skill not in user.skills:
        user.skills.append(skill)
        db.commit()
        db.refresh(user)
    return user

def remove_skill_from_user(db: Session, user_id: int, skill_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not user or not skill:
        raise HTTPException(status_code=404, detail="User or Skill not found")

    if skill in user.skills:
        user.skills.remove(skill)
        db.commit()
        db.refresh(user)
    return user

def get_user_skills(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.skills
