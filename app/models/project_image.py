from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ProjectImage(Base):
    __tablename__ = "project_images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    image_url = Column(String, nullable=False)
    alt_text = Column(String, nullable=True)  # Альтернативный текст для изображения
    order = Column(Integer, default=0, nullable=False)  # Порядок отображения изображений
    is_primary = Column(Boolean, default=False, nullable=False)  # Основное изображение проекта
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    project = relationship("Project", back_populates="images")

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

