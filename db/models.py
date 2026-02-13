from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Enum, String, UniqueConstraint
from db.base import Base
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    mobile: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_mobile_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    companies = relationship("CompanyUser", back_populates="user", cascade="all, delete-orphan")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    cin: Mapped[str] = mapped_column(String(21), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    company_type: Mapped[str] = mapped_column(String(20), nullable=False)
    incorporation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    registered_office: Mapped[str] = mapped_column(String(255), nullable=False)

    directors = relationship("DirectorAppointments", back_populates="company")
    meetings = relationship("Meetings", back_populates="company")

    users = relationship("CompanyUser", back_populates="company", cascade="all, delete-orphan")

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "company_type IN ('public', 'private')",
            name="check_company_type"
        ),
    )

class CompanyUser(Base):
    __tablename__ = "company_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    # admin | director | cs | viewer

    company = relationship("Company", back_populates="users")
    user = relationship("User", back_populates="companies")

    __table_args__ = (
        UniqueConstraint("company_id", "user_id"),
    )

class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int] = mapped_column(primary_key=True)
    din: Mapped[str] = mapped_column(String(8), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

    companies = relationship("DirectorAppointments", back_populates="director")

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

class DirectorAppointments(Base):
    __tablename__ = "director_appointments"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id", ondelete="CASCADE"), nullable=False)
    designation: Mapped[str] = mapped_column(String(255), nullable=False)
    appointment_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    cessation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    company = relationship("Company", back_populates="directors")
    director = relationship("Director", back_populates="companies")

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "designation IN ('managing director', 'independent director', 'woman director', 'nominee director', 'casual vacancy director')",
            name="check_director_designation"
        ),
    )


    __table_args__ = (
        UniqueConstraint("company_id", "director_id", "appointment_date"),
    )


class Meetings(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    scheduled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    venue: Mapped[str] = mapped_column(String(255), nullable=False)
    at_shorter_notice: Mapped[bool] = mapped_column(Boolean, nullable=False)
    attendance_mode: Mapped[str] = mapped_column(String(255), nullable=False)
    meeting_link: Mapped[str] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "type IN ('annual general meeting', 'extraordinary general meeting', 'board meeting', 'audit committee meeting', 'corporate social responsibility meeting', 'nomination and remuneration committee meeting')",
            name="check_meeting_type"
        ),
    )


class DocumentTemplate(Base):
    __tablename__ = "document_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    template_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    template_path: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(50), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )