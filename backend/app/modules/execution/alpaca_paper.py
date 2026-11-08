"""Connecteur Alpaca Paper optionnel — isolé, jamais mélangé au classement local."""

import httpx

from app.config import get_settings
from app.modules.execution.guards import TradingUrlGuard


class AlpacaPaperExecutionAdapter:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.guard = TradingUrlGuard(self.settings)
        self.base_url = self.settings.alpaca_paper_base_url.rstrip("/")

    def assert_ready(self) -> None:
        self.guard.assert_order_url_allowed(self.base_url)

    async def submit_market_order(self, symbol: str, qty: int, side: str, idempotency_key: str) -> dict:
        self.assert_ready()
        # Intégration réelle activée uniquement avec clés — V1 stub documenté
        api_key = ""  # lu via env en intégration complète
        if not api_key:
            raise RuntimeError(
                "ALPACA_PAPER_API_KEY non configuré — connecteur en validation seulement"
            )
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base_url}/v2/orders",
                headers={"APCA-API-KEY-ID": api_key},
                json={"symbol": symbol, "qty": qty, "side": side, "type": "market", "time_in_force": "day"},
            )
            resp.raise_for_status()
            return resp.json()
