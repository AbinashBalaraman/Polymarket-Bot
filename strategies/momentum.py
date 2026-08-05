from typing import Optional
from strategies.base import BaseStrategy, Signal
from market_scanner import Market
from config import config

class MomentumStrategy(BaseStrategy):
    """
    Volume & Probability Drift Momentum Strategy:
    Detects high-volume probability breakouts on trending prediction topics.
    """

    @property
    def name(self) -> str:
        return "momentum"

    def evaluate(self, market: Market) -> Optional[Signal]:
        yes_ask = market.yes_best_ask

        # If probability is breaking out above 0.70 with substantial liquidity
        if 0.70 <= yes_ask <= 0.85 and market.volume_24h_usd > 150000:
            return Signal(
                market=market,
                action="BUY_MOMENTUM_YES",
                token_id=market.token_yes_id,
                price=yes_ask,
                size_usd=min(250.0, config.max_position_size_usd),
                edge=0.03,
                confidence=0.78,
                reason=f"Probability Momentum Breakout: YES at {yes_ask:.2f} on 24h Vol ${market.volume_24h_usd:,.0f}",
                strategy=self.name
            )

        return None

    def should_cancel(self, order_age_seconds: float, current_edge: float) -> bool:
        return order_age_seconds > 20.0
