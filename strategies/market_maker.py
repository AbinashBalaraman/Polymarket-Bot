from typing import Optional
from strategies.base import BaseStrategy, Signal
from market_scanner import Market
from config import config

class MarketMakerStrategy(BaseStrategy):
    """
    Market Making Strategy:
    Provides bid-ask liquidity on wide-spread prediction markets.
    """

    @property
    def name(self) -> str:
        return "market_maker"

    def evaluate(self, market: Market) -> Optional[Signal]:
        bid = market.yes_best_bid
        ask = market.yes_best_ask
        spread = ask - bid

        if spread >= 0.04 and market.volume_24h_usd > 50000:
            mid_price = (bid + ask) / 2
            edge = spread / 2

            return Signal(
                market=market,
                action="MAKER_BID",
                token_id=market.token_yes_id,
                price=round(bid + 0.005, 3),
                size_usd=min(200.0, config.max_position_size_usd),
                edge=edge,
                confidence=0.85,
                reason=f"Market Making: Wide spread ({spread:.3f}) on volume ${market.volume_24h_usd:,.0f}",
                strategy=self.name
            )

        return None

    def should_cancel(self, order_age_seconds: float, current_edge: float) -> bool:
        return order_age_seconds > 30.0
