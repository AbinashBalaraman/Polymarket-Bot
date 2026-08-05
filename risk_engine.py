import logging
from config import config

logger = logging.getLogger("RiskEngine")

class RiskEngine:
    def __init__(self, bankroll: float = None):
        self.bankroll = bankroll or config.bankroll_usd
        self.daily_pnl = 0.0
        self.active_exposure = 0.0
        self.circuit_breaker_tripped = False

    def calculate_kelly_size(self, probability: float, price: float, win_odds: float = 1.0) -> float:
        """
        Calculate position size using Half-Kelly Criterion.
        f* = (bp - q) / b
        where b = odds, p = probability of winning, q = 1 - p
        """
        if price <= 0 or price >= 1.0:
            return 0.0

        p = probability
        q = 1.0 - p
        b = (1.0 - price) / price if price > 0 else win_odds

        kelly_full = (b * p - q) / b if b > 0 else 0.0
        if kelly_full <= 0:
            return 0.0

        # Fractional Kelly
        fractional_kelly = kelly_full * config.kelly_fraction
        
        # Max position cap
        size_usd = min(self.bankroll * fractional_kelly, config.max_position_size_usd)
        return max(size_usd, 0.0)

    def validate_trade(self, requested_size_usd: float) -> bool:
        """
        Check circuit breaker, daily loss limit, and exposure caps before placing order.
        """
        if self.circuit_breaker_tripped:
            logger.warning("Trade rejected: Circuit breaker is TRIPPED due to daily loss limit.")
            return False

        if self.daily_pnl <= -config.max_daily_loss_usd:
            self.circuit_breaker_tripped = True
            logger.error(f"Circuit breaker TRIPPED! Daily loss ${abs(self.daily_pnl):.2f} exceeded limit ${config.max_daily_loss_usd:.2f}")
            return False

        if self.active_exposure + requested_size_usd > self.bankroll:
            logger.warning(f"Trade rejected: Insufficient bankroll capacity. Active: ${self.active_exposure:.2f}, Requested: ${requested_size_usd:.2f}")
            return False

        return True

    def record_pnl(self, pnl_usd: float):
        self.daily_pnl += pnl_usd
        logger.info(f"Updated Daily PnL: ${self.daily_pnl:+.2f}")
        if self.daily_pnl <= -config.max_daily_loss_usd:
            self.circuit_breaker_tripped = True
            logger.error("Circuit breaker TRIPPED after trade recording!")
