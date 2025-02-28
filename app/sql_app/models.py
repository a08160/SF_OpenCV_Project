from sqlalchemy import Integer, String, ForeignKey, Float, Column, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .database import Base # database.py에서 생성한 Base import
from datetime import datetime


# SQLAlchemy 모델
# SQLAlchemy는 데이터베이스의 테이블 및 열 정의를 위해 사용

class Recommendations(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String(50), nullable=False)
    image_url = Column(Text, nullable=False)
    item_name = Column(String(255), nullable=False)
    brand_name = Column(String(255), nullable=False)
    personal_color = Column(String(50), nullable=False)

    def __repr__(self):
        return (
            f"<Recommendations(id={self.id}, category={self.category}, "
            f"image_url={self.image_url}, item_name={self.item_name}, "
            f"brand_name={self.brand_name}, personal_color={self.personal_color})>"
        )