from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    sqlite_path: str = Field(default='data/mvp.db', alias='SQLITE_PATH')
    symbol: str = Field(default='BTC-USD', alias='SYMBOL')
    trade_qty: float = Field(default=0.01, alias='TRADE_QTY')
    spread_threshold: float = Field(default=0.01, alias='SPREAD_THRESHOLD')
    starting_cash: float = Field(default=10_000, alias='STARTING_CASH')
    polymarket_use_synthetic: bool = Field(default=True, alias='POLYMARKET_USE_SYNTHETIC')
    polymarket_host: str = Field(default='https://clob.polymarket.com', alias='POLYMARKET_HOST')
    polymarket_chain_id: int = Field(default=137, alias='POLYMARKET_CHAIN_ID')
    polymarket_token_id: str | None = Field(default=None, alias='POLYMARKET_TOKEN_ID')
    polymarket_private_key: str | None = Field(default=None, alias='POLYMARKET_PRIVATE_KEY')
    polymarket_api_key: str | None = Field(default=None, alias='POLYMARKET_API_KEY')
    polymarket_api_secret: str | None = Field(default=None, alias='POLYMARKET_API_SECRET')
    polymarket_api_passphrase: str | None = Field(default=None, alias='POLYMARKET_API_PASSPHRASE')
    signal_queue_path: str = Field(default='data/signals.jsonl', alias='SIGNAL_QUEUE_PATH')
    broker_state_path: str = Field(default='data/broker_state.json', alias='BROKER_STATE_PATH')


settings = Settings()
