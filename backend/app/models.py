import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    from datetime import timezone

    return datetime.now(timezone.utc)


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    mode: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="active")
    initial_capital: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("100000"))
    ai_budget_usd: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("50"))
    execution_engine: Mapped[str] = mapped_column(String(64), default="local_canonical")
    config: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    competitors: Mapped[list["Competitor"]] = relationship(back_populates="campaign")


class Competitor(Base):
    __tablename__ = "competitors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("campaigns.id"), index=True)
    name: Mapped[str] = mapped_column(String(200))
    provider: Mapped[str] = mapped_column(String(64))
    model_id: Mapped[str] = mapped_column(String(128))
    architecture: Mapped[str] = mapped_column(String(32), default="A")
    prompt_version: Mapped[str] = mapped_column(String(64), default="v1")
    prompt_hash: Mapped[str] = mapped_column(String(64))
    cash: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    ai_cost_usd: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=Decimal("0"))

    campaign: Mapped["Campaign"] = relationship(back_populates="competitors")
    decisions: Mapped[list["DecisionLog"]] = relationship(back_populates="competitor")
    positions: Mapped[list["PositionRow"]] = relationship(back_populates="competitor")


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    competitor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competitors.id"), index=True)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    contract: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"))
    validation_ok: Mapped[bool] = mapped_column(Boolean, default=False)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    data_snapshot_hash: Mapped[str] = mapped_column(String(64))
    latency_ms: Mapped[int] = mapped_column(default=0)
    tokens_in: Mapped[int] = mapped_column(default=0)
    tokens_out: Mapped[int] = mapped_column(default=0)
    cost_usd: Mapped[Decimal] = mapped_column(Numeric(10, 6), default=Decimal("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    competitor: Mapped["Competitor"] = relationship(back_populates="decisions")
    orders: Mapped[list["OrderRow"]] = relationship(back_populates="decision")


class PositionRow(Base):
    __tablename__ = "positions"
    __table_args__ = (UniqueConstraint("competitor_id", "symbol", name="uq_competitor_symbol"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competitor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competitors.id"), index=True)
    symbol: Mapped[str] = mapped_column(String(16))
    quantity: Mapped[int] = mapped_column()
    avg_cost: Mapped[Decimal] = mapped_column(Numeric(18, 6))

    competitor: Mapped["Competitor"] = relationship(back_populates="positions")


class OrderRow(Base):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("idempotency_key", name="uq_order_idempotency"),)

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    competitor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competitors.id"), index=True)
    decision_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("decision_logs.id"), nullable=True)
    idempotency_key: Mapped[str] = mapped_column(String(128))
    symbol: Mapped[str] = mapped_column(String(16))
    side: Mapped[str] = mapped_column(String(8))
    quantity: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column(String(32))
    execution_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    assumptions_label: Mapped[str] = mapped_column(String(64), default="estimation")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    decision: Mapped["DecisionLog | None"] = relationship(back_populates="orders")
    fills: Mapped[list["FillRow"]] = relationship(back_populates="order")


class FillRow(Base):
    __tablename__ = "fills"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("orders.id"), index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    commission: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    slippage_cost: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    filled_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    order: Mapped["OrderRow"] = relationship(back_populates="fills")


class EquitySnapshot(Base):
    __tablename__ = "equity_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    competitor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("competitors.id"), index=True)
    as_of: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    equity: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    cash: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    pnl_unrealized: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=Decimal("0"))


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(64))
    payload: Mapped[dict] = mapped_column(JSON().with_variant(JSONB, "postgresql"), default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
