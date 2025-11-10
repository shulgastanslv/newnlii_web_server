from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.schemas.skill import SkillCreate

def create_skill(db: Session, skill: SkillCreate):
    res = Skill(name=skill.name)
    db.add(res)
    db.commit()
    db.refresh(res)
    return res

def get_all_skills(db: Session):
    return db.query(Skill).all()