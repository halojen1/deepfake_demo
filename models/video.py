from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Video(Base):
    __tablename__ = 'videos'
    id = Column(Integer, primary_key=True)
    filename = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    result = Column(String(50))  # placeholder kết quả deepfake
    user = relationship("User")
