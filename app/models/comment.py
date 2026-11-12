from datetime import datetime
from sqlalchemy import Text, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ticket_id: Mapped[int] = mapped_column(ForeignKey('tickets.id', ondelete='CASCADE'))
    ticket: Mapped['Ticket'] = relationship(back_populates='comments')

    author_agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id', ondelete='RESTRICT'))
    agent: Mapped['Agent'] = relationship(back_populates='comments')