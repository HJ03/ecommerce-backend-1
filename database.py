import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Replace with your PostgreSQL credentials
# DATABASE_URL = "postgresql://postgres:billi007@localhost:5432/ecommerce_db"
# DATABASE_URL = "postgresql://postgres:vnfCfvqRusHQdSFtYunNZjtEpyKobuzy@hopper.proxy.rlwy.net:30756/railway"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:vnfCfvqRusHQdSFtYunNZjtEpyKobuzy@hopper.proxy.rlwy.net:30756/railway")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
