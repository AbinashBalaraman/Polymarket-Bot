"""
Base strategy interface — all strategies implement this.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from market_scanner import Market


@dataclass
class Signal:
    """A trading signal from a strategy."""
    market: Market
    action: str
    token_id: str
    price: float
    size_usd: float
    edge: float
    confidence: float
    reason: str
    strategy: str


class BaseStrategy(ABC):
    """Abstract base for all trading strategies."""

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def evaluate(self, market: Market) -> Optional[Signal]:
        """Evaluate a market and return a Signal if there's an opportunity."""
        ...

    @abstractmethod
    def should_cancel(self, order_age_seconds: float, current_edge: float) -> bool:
        """Check if an existing order should be cancelled (edge decay)."""
        ...