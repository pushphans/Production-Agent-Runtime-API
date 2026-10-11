from pydantic import EmailStr
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Text, DateTime, func, Boolean, UUID
import uuid
from datetime import datetime
from production_agent_runtime_api.core.db import Base



class UserModel(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4, nullable = False)
    name : Mapped[str] = mapped_column(Text, nullable = False)
    email : Mapped[EmailStr] = mapped_column(Text, nullable = False, unique = True)
    password_hash : Mapped[str] = mapped_column(Text, nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)