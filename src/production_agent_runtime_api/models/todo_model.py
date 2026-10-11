from sqlalchemy import ForeignKey
import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, func, Boolean, UUID
from datetime import datetime
from production_agent_runtime_api.core.db import Base


class TodoModel(Base):
    __tablename__ = "todos"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    title : Mapped[str] = mapped_column(Text, nullable = False)
    description : Mapped[str | None] = mapped_column(Text, nullable = False, default = "Todo description")
    is_completed : Mapped[bool | None] = mapped_column(Boolean, nullable = False, default = False)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable = False, server_default = func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)
