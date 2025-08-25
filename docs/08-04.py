# set up models and add to alembic and set up alembic

# create models.py in tasks folder
"""
# core/core/models.py
from sqlalchemy import Column, Integer, String, Text, Boolean, func, DateTime
from core.db import Base


class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title= Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    
    create_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
"""


# how to connect model to alembic
# remove value of sqlalchemy.url in alambic.ini

# add enviroment variable SQLALCHEMY_DATABASE_URL from core/.env to core/migrations/env.py
"""
from core.db import Base
from tasks.models import *

import os
from dotenv import load_dotenv
from pathlib import Path


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")


if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)
else:
    raise ValueError("DATABASE is not in the enviroment variables")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata
"""

# now command for create model version in alembic
# command : core> alembiv revision --autogenerate -m "create Task table"

# command to implemen creation table
# command : core>alembic upgrade heads


# finally commanc > core\uv run fastapi dev main.py

