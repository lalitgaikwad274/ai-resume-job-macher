
from alembic.context import config
import os

from dotenv import load_dotenv

from app.database.base import Base
from app.models import (
    User,
    Resume,
    JobDescription,
    ResumeAnalysis,
    Recommendation,
)

load_dotenv()

config.set_main_option(
    "sqlalchemy.url",
    os.getenv("DATABASE_URL", "").replace("%", "%%"),
)

target_metadata = Base.metadata
