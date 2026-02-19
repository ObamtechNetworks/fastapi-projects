from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# format => postgresql://<username>:<password>@<ip-address/hostname>/<database_name>
SQL_DATABASE_URL = "postgresql://postgres:root@localhost/fastapi"

# create an engine instance
engine = create_engine(SQL_DATABASE_URL)

# create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a Base class for our models to inherit from
Base = declarative_base()
