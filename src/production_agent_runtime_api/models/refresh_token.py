import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import UUID
import uuid
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import Boolean, Text, DateTime, func
from production_agent_runtime_api.core.db import Base

class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable = False)
    refresh_token : Mapped[str] = mapped_column(Text, nullable = False)
    refresh_token_expiry : Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)