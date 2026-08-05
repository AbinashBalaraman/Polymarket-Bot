import os
from dataclasses import dataclass, field
from typing import List
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    paper_mode: bool = os.getenv("PAPER_MODE", "true").lower() == "true"
    polygon_private_key: str = os.getenv("POLYGON_PRIVATE_KEY", "")
    rpc_url: str = os.getenv("RPC_URL", "https://polygon-rpc.com")
    
    bankroll_usd: float = float(os.getenv("BANKROLL_USD", "10000.0"))
    kelly_fraction: float = float(os.getenv("KELLY_FRACTION", "0.5"))
    max_position_size_usd: float = float(os.getenv("MAX_POSITION_SIZE_USD", "500.0"))
    max_daily_loss_usd: float = float(os.getenv("MAX_DAILY_LOSS_USD", "200.0"))
    min_arbitrage_edge: float = float(os.getenv("MIN_ARBITRAGE_EDGE", "0.015"))
    
    scan_interval_seconds: float = float(os.getenv("SCAN_INTERVAL_SECONDS", "5.0"))
    active_strategies: List[str] = field(default_factory=lambda: os.getenv("ACTIVE_STRATEGIES", "arbitrage,market_maker,momentum").split(","))

config = Config()
