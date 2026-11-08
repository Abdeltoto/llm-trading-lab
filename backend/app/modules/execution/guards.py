from urllib.parse import urlparse

from app.config import REAL_TRADING_HOST_BLOCKLIST, Settings


class TradingUrlGuard:
    """Bloque les hôtes d'exécution réels et impose la liste blanche ordres."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def assert_order_url_allowed(self, url: str) -> None:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if not host:
            raise PermissionError("URL d'ordre invalide")

        if self._settings.block_real_trading and host in REAL_TRADING_HOST_BLOCKLIST:
            raise PermissionError(f"Hôte de trading réel bloqué : {host}")

        allowed = set(self._settings.order_hosts())
        if host not in allowed:
            raise PermissionError(f"Hôte d'ordre non autorisé : {host}")
