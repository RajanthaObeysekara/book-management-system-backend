from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.db.database import Base
from sqlalchemy.sql import func

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    publication_date = Column(String)
    ISBN = Column(String, unique=True)
    cover_image = Column(String)
    category = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="books")