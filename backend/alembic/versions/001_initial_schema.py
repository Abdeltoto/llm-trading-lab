"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-11-08
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "campaigns",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("mode", sa.String(32), nullable=False),
        sa.Column("status", sa.String(32), server_default="active"),
        sa.Column("initial_capital", sa.Numeric(18, 2)),
        sa.Column("ai_budget_usd", sa.Numeric(10, 2)),
        sa.Column("execution_engine", sa.String(64)),
        sa.Column("config", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "competitors",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("campaign_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("campaigns.id")),
        sa.Column("name", sa.String(200)),
        sa.Column("provider", sa.String(64)),
        sa.Column("model_id", sa.String(128)),
        sa.Column("architecture", sa.String(32)),
        sa.Column("prompt_version", sa.String(64)),
        sa.Column("prompt_hash", sa.String(64)),
        sa.Column("cash", sa.Numeric(18, 2)),
        sa.Column("ai_cost_usd", sa.Numeric(10, 4)),
    )
    op.create_table(
        "decision_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("competitors.id")),
        sa.Column("as_of", sa.DateTime(timezone=True)),
        sa.Column("contract", sa.JSON()),
        sa.Column("validation_ok", sa.Boolean()),
        sa.Column("rejection_reason", sa.Text()),
        sa.Column("data_snapshot_hash", sa.String(64)),
        sa.Column("latency_ms", sa.Integer()),
        sa.Column("tokens_in", sa.Integer()),
        sa.Column("tokens_out", sa.Integer()),
        sa.Column("cost_usd", sa.Numeric(10, 6)),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("competitors.id")),
        sa.Column("symbol", sa.String(16)),
        sa.Column("quantity", sa.Integer()),
        sa.Column("avg_cost", sa.Numeric(18, 6)),
        sa.UniqueConstraint("competitor_id", "symbol", name="uq_competitor_symbol"),
    )
    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("competitors.id")),
        sa.Column("decision_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("decision_logs.id"), nullable=True),
        sa.Column("idempotency_key", sa.String(128), unique=True),
        sa.Column("symbol", sa.String(16)),
        sa.Column("side", sa.String(8)),
        sa.Column("quantity", sa.Integer()),
        sa.Column("status", sa.String(32)),
        sa.Column("execution_date", sa.Date()),
        sa.Column("assumptions_label", sa.String(64)),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "fills",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id")),
        sa.Column("price", sa.Numeric(18, 6)),
        sa.Column("commission", sa.Numeric(18, 6)),
        sa.Column("slippage_cost", sa.Numeric(18, 6)),
        sa.Column("filled_at", sa.DateTime(timezone=True)),
    )
    op.create_table(
        "equity_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("competitor_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("competitors.id")),
        sa.Column("as_of", sa.DateTime(timezone=True)),
        sa.Column("equity", sa.Numeric(18, 2)),
        sa.Column("cash", sa.Numeric(18, 2)),
        sa.Column("pnl_unrealized", sa.Numeric(18, 2)),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("event_type", sa.String(64)),
        sa.Column("payload", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True)),
    )


def downgrade() -> None:
    for t in (
        "audit_events",
        "equity_snapshots",
        "fills",
        "orders",
        "positions",
        "decision_logs",
        "competitors",
        "campaigns",
    ):
        op.drop_table(t)
