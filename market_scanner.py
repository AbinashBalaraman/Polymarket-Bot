from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class OrderbookEntry:
    price: float
    size: float

@dataclass
class Orderbook:
    bids: List[OrderbookEntry] = field(default_factory=list)
    asks: List[OrderbookEntry] = field(default_factory=list)

    @property
    def best_bid(self) -> Optional[float]:
        return self.bids[0].price if self.bids else None

    @property
    def best_ask(self) -> Optional[float]:
        return self.asks[0].price if self.asks else None

@dataclass
class Market:
    condition_id: str
    question: str
    category: str
    token_yes_id: str
    token_no_id: str
    orderbook_yes: Orderbook
    orderbook_no: Orderbook
    volume_24h_usd: float = 0.0
    liquidity_usd: float = 0.0
    active: bool = True

    @property
    def yes_best_ask(self) -> float:
        return self.orderbook_yes.best_ask or 0.99

    @property
    def yes_best_bid(self) -> float:
        return self.orderbook_yes.best_bid or 0.01

    @property
    def no_best_ask(self) -> float:
        return self.orderbook_no.best_ask or 0.99

    @property
    def no_best_bid(self) -> float:
        return self.orderbook_no.best_bid or 0.01
