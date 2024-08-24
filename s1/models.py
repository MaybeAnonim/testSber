from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, JSON, DateTime, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()


class QueueRequest(Base):
    __tablename__ = 'queue_requests'

    id = Column(Integer, primary_key=True)
    uri = Column(String, nullable=False)
    method = Column(String, nullable=False)
    params = Column(JSON, nullable=True)
    headers = Column(JSON, nullable=True)
    status = Column(String, default="Незаконченный")
    processed = Column(Boolean, default=False)
    is_new = Column(Boolean, default=True)


class QueueResponse(Base):
    __tablename__ = 'queue_responses'

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, ForeignKey('queue_requests.id'))
    status_code = Column(Integer, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


def setup_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)