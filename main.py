import sys
import os
import time
import logging

# Ensure UTF-8 output encoding on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from config import config
from polymarket_client import PolymarketClient
from risk_engine import RiskEngine
from database import Database
from strategies.arbitrage import ArbitrageStrategy
from strategies.market_maker import MarketMakerStrategy
from strategies.momentum import MomentumStrategy

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("PolyTraderMain")
console = Console(legacy_windows=False)

def render_banner():
    banner_text = """
========================================================================
   PolyTrader v2.5 — Quantitative Polymarket Arbitrage & Bot Suite
========================================================================
    """
    console.print(Panel(banner_text, border_style="cyan"))

def main():
    render_banner()

    mode_str = "[bold green]PAPER TRADING MODE[/bold green]" if config.paper_mode else "[bold red]LIVE PRODUCTION MODE[/bold red]"
    console.print(f"Running Mode: {mode_str}")
    console.print(f"Bankroll: ${config.bankroll_usd:,.2f} | Kelly Fraction: {config.kelly_fraction} | Max Single Position: ${config.max_position_size_usd:.2f}\n")

    client = PolymarketClient()
    risk = RiskEngine()
    db = Database()

    # Strategy Registry
    available_strategies = [
        ArbitrageStrategy(),
        MarketMakerStrategy(),
        MomentumStrategy()
    ]

    active_strats = [s for s in available_strategies if s.name in config.active_strategies]
    console.print(f"Active Strategies: [bold white]{', '.join([s.name for s in active_strats])}[/bold white]\n")

    # Run single audit scan
    console.rule("[bold cyan]Scan Iteration #1 Audit[/bold cyan]")
    markets = client.fetch_active_markets(limit=10)
    console.print(f"Scanned [bold yellow]{len(markets)}[/bold yellow] active prediction markets.")

    signals_found = []
    for market in markets:
        for strat in active_strats:
            signal = strat.evaluate(market)
            if signal:
                signals_found.append(signal)

    if signals_found:
        table = Table(title="Trading Signals Detected", border_style="green")
        table.add_column("Strategy", style="cyan")
        table.add_column("Market Question", style="white")
        table.add_column("Action", style="yellow")
        table.add_column("Price", style="magenta")
        table.add_column("Size ($)", style="green")
        table.add_column("Edge (%)", style="bold green")

        for sig in signals_found:
            table.add_row(
                sig.strategy,
                sig.market.question[:45] + "..." if len(sig.market.question) > 45 else sig.market.question,
                sig.action,
                f"${sig.price:.3f}",
                f"${sig.size_usd:.2f}",
                f"{sig.edge * 100:+.2f}%"
            )
            
            if risk.validate_trade(sig.size_usd):
                success = client.execute_order(sig.token_id, sig.action, sig.price, sig.size_usd)
                if success:
                    db.log_trade(
                        condition_id=sig.market.condition_id,
                        strategy=sig.strategy,
                        action=sig.action,
                        token_id=sig.token_id,
                        price=sig.price,
                        size_usd=sig.size_usd,
                        edge=sig.edge,
                        paper=config.paper_mode
                    )

        console.print(table)
    else:
        console.print("[dim]No signal edges met risk thresholds on this scan.[/dim]")

    console.print(f"Daily PnL: [bold green]${risk.daily_pnl:+.2f}[/bold green] | Circuit Breaker: {'[red]TRIPPED[/red]' if risk.circuit_breaker_tripped else '[green]NORMAL[/green]'}")

if __name__ == "__main__":
    main()
