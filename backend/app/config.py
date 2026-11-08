from enum import Enum
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class TradingMode(str, Enum):
    DEMO = "DEMO"
    BACKTEST = "BACKTEST"
    PAPER_FORWARD = "PAPER_FORWARD"


REAL_TRADING_HOST_BLOCKLIST = frozenset(
    {
        "api.binance.com",
        "api.coinbase.com",
        "api.interactivebrokers.com",
        "api.tdameritrade.com",
        "api.alpaca.markets",  # live — paper uses paper-api
    }
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    trading_mode: TradingMode = Field(alias="TRADING_MODE", default=TradingMode.DEMO)
    app_version: str = Field(alias="APP_VERSION", default="0.1.0-dev")
    git_commit: str = Field(alias="GIT_COMMIT", default="local")
    secret_key: str = Field(alias="SECRET_KEY", default="dev-secret-change-me")
    database_url: str = Field(
        alias="DATABASE_URL",
        default="postgresql+psycopg://lab:lab@localhost:5432/llm_trading_lab",
    )
    redis_url: str = Field(alias="REDIS_URL", default="redis://localhost:6379/0")
    worker_enabled: bool = Field(alias="WORKER_ENABLED", default=True)
    execution_engine: str = Field(alias="EXECUTION_ENGINE", default="local_canonical")
    execution_commission_bps: float = Field(alias="EXECUTION_COMMISSION_BPS", default=0.1)
    execution_spread_bps: float = Field(alias="EXECUTION_SPREAD_BPS", default=1.0)
    execution_slippage_bps: float = Field(alias="EXECUTION_SLIPPAGE_BPS", default=2.0)
    allowed_order_hosts: str = Field(
        alias="ALLOWED_ORDER_HOSTS", default="paper-api.alpaca.markets"
    )
    allowed_data_hosts: str = Field(alias="ALLOWED_DATA_HOSTS", default="")
    block_real_trading: bool = Field(alias="BLOCK_REAL_TRADING", default=True)
    cors_origins: str = Field(
        alias="CORS_ORIGINS", default="http://localhost:5180,http://localhost:3000"
    )
    demo_username: str = Field(alias="DEMO_USERNAME", default="demo")
    demo_password: str = Field(alias="DEMO_PASSWORD", default="demo")
    alpaca_paper_base_url: str = Field(
        alias="ALPACA_PAPER_BASE_URL", default="https://paper-api.alpaca.markets"
    )

    @field_validator("trading_mode", mode="before")
    @classmethod
    def normalize_mode(cls, v: str | TradingMode) -> TradingMode:
        if isinstance(v, TradingMode):
            return v
        return TradingMode(v.strip().upper())

    def order_hosts(self) -> list[str]:
        return [h.strip() for h in self.allowed_order_hosts.split(",") if h.strip()]

    def data_hosts(self) -> list[str]:
        return [h.strip() for h in self.allowed_data_hosts.split(",") if h.strip()]

    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
