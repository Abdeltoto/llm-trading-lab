from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import pytest

from app.schemas.decision import DecisionContract, TargetWeight


def test_invalid_json_weights_rejected():
    with pytest.raises(ValueError):
        DecisionContract(
            decision_id=uuid4(),
            as_of=datetime.now(timezone.utc),
            targets=[
                TargetWeight(symbol="SPY", target_weight=Decimal("0.5"), evidence_ids=["e"]),
            ],
            cash_weight=Decimal("0.3"),
            rationale_summary="x",
        )


def test_abstain_skips_weight_sum():
    d = DecisionContract(
        decision_id=uuid4(),
        as_of=datetime.now(timezone.utc),
        targets=[],
        cash_weight=Decimal("1"),
        rationale_summary="abstention",
        abstain=True,
    )
    assert d.abstain
