from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///jobs.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True, nullable=False)
    applied = Column(Boolean, default=False)
    
    
Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    Base.metadata.create_all(engine)
    
def insert_job(job_url):
    job = Job(url=job_url)
    session.add(job)
    try:
        session.commit()
    except:
        session.rollback()  #Rollback if job is already in the DB
        
def get_unapplied_jobs():
    return session.query(Job).filter_by(applied=False).all()

def mark_job_as_applied(job_url):
    job = session.query(Job).filter_by(url=job_url).first()
    if job:
        job.applied = True
        session.commit()

