from datetime import datetime
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class TargetWeight(BaseModel):
    symbol: str
    target_weight: Annotated[Decimal, Field(ge=0, le=1, decimal_places=6)]
    evidence_ids: list[str] = Field(min_length=1)

    @field_validator("symbol")
    @classmethod
    def upper_symbol(cls, v: str) -> str:
        return v.strip().upper()


class DecisionContract(BaseModel):
    decision_id: UUID
    as_of: datetime
    targets: list[TargetWeight] = Field(default_factory=list)
    cash_weight: Annotated[Decimal, Field(ge=0, le=1, decimal_places=6)]
    rationale_summary: str = Field(max_length=2000)
    abstain: bool = False

    @model_validator(mode="after")
    def validate_weights(self) -> "DecisionContract":
        if self.abstain:
            return self
        total = self.cash_weight + sum(t.target_weight for t in self.targets)
        if total != Decimal("1"):
            raise ValueError(f"Les poids doivent sommer à 1, reçu {total}")
        symbols = [t.symbol for t in self.targets]
        if len(symbols) != len(set(symbols)):
            raise ValueError("Symboles dupliqués dans targets")
        return self
