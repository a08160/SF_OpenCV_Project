from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 환경 변수 가져오기

user = os.getenv("DB_USER")     
passwd = os.getenv("DB_PASSWD") 
host = os.getenv("DB_HOST")     
port = os.getenv("DB_PORT", "3306")     
db = os.getenv("DB_NAME")      

# SQLAlchemy DB URL 생성
# DB_URL = f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}"
DB_URL = "mysql+pymysql://root:leedonggun6932*1@localhost:3306/test_db"

# 엔진 생성
engine = create_engine(DB_URL, echo=True)

# DB 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성
Base = declarative_base()
