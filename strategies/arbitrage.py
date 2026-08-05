from typing import Optional
from strategies.base import BaseStrategy, Signal
from market_scanner import Market
from config import config

class ArbitrageStrategy(BaseStrategy):
    """
    Arbitrage Strategy:
    Scans for mispriced outcome tokens where YES_ask + NO_ask < 1.0.
    In a complete market, YES + NO must resolve to exactly 1.0.
    If YES_ask + NO_ask = 0.985, buying 1 unit of YES and 1 unit of NO costs 0.985
    and guarantees a $1.00 payout regardless of outcome -> 1.5% risk-free edge!
    """

    @property
    def name(self) -> str:
        return "arbitrage"

    def evaluate(self, market: Market) -> Optional[Signal]:
        yes_ask = market.yes_best_ask
        no_ask = market.no_best_ask

        combined_cost = yes_ask + no_ask
        raw_edge = 1.0 - combined_cost

        if raw_edge >= config.min_arbitrage_edge:
            # Riskless arbitrage opportunity detected
            return Signal(
                market=market,
                action="BUY_ARBITRAGE_PAIR",
                token_id=market.token_yes_id,
                price=yes_ask,
                size_usd=config.max_position_size_usd,
                edge=raw_edge,
                confidence=1.0,
                reason=f"Riskless Arbitrage: YES_ask({yes_ask:.3f}) + NO_ask({no_ask:.3f}) = {combined_cost:.3f} < 1.0 (Edge: {raw_edge*100:.2f}%)",
                strategy=self.name
            )

        return None

    def should_cancel(self, order_age_seconds: float, current_edge: float) -> bool:
        return order_age_seconds > 10.0 or current_edge < config.min_arbitrage_edge
