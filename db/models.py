from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, func

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
