from app.models.enums import Status, Priority, Category
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base



class Ticket(Base):
    __tablename__ = "tickets"
        
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[Status] = mapped_column(Enum(Status, native_enum=False), default=Status.OPEN)
    priority: Mapped[Priority] = mapped_column(Enum(Priority, native_enum=False),default=Priority.MEDIUM)
    category: Mapped[Category] = mapped_column(Enum(Category, native_enum=False),default=Category.OTHER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id', ondelete='RESTRICT'))
    customer: Mapped['Customer'] = relationship(back_populates='tickets')

    assigned_agent_id: Mapped[int] = mapped_column(ForeignKey('agents.id', ondelete='RESTRICT'))
    agent: Mapped['Agent'] = relationship(back_populates='tickets')

    comments: Mapped[list['Comment']] = relationship(back_populates="ticket", cascade="all, delete-orphan")
