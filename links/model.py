from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from application.database import Base


class Link(Base):
    __tablename__ = 'link'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    long_url = Column(String, index=True)
    short_url = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now())
    deleted = Column(Boolean, nullable=False, default=False)

    __table_args__ = (UniqueConstraint('short_url'),)

class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True, index=True)
    link = Column(UUID(as_uuid=True), ForeignKey('link.id'))
    created_at = Column(DateTime, default=datetime.now())
