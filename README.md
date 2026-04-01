# PolyTrader — Prediction Market Arbitrage Bot

Automated trading bot for prediction markets (Polymarket) with real-time arbitrage detection, risk management, and circuit breaker systems.

## Architecture

```
main.py              # Bot orchestrator: scan → evaluate → execute → manage risk
config.py            # Centralized configuration from environment variables
market_scanner.py    # Market discovery and data fetching
data_layer.py        # Order book analysis and price data
execution_engine.py  # Order placement and lifecycle management
risk_manager.py      # Circuit breakers, exposure limits, position guards
state_store.py       # SQLite persistence for positions and trades
strategies/
  base.py            # Abstract strategy interface
  arbitrage.py       # YES+NO spread arbitrage scanner
```

## Features

- **Arbitrage Detection**: Scans for YES+NO spread opportunities where total cost < $1.00
- **Half-Kelly Position Sizing**: Mathematically optimal bet sizing with conservative cap
- **Circuit Breakers**: Auto-stop trading on daily loss limit breach
- **Position Guards**: Per-market exposure caps prevent concentration risk
- **Paper Trading**: Full simulation mode for strategy validation
- **State Persistence**: SQLite-backed position tracking and trade history
- **Graceful Shutdown**: SIGINT/SIGTERM handlers for clean exit

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/AbinashBalaraman/Polymarket-Bot.git
cd Polymarket-Bot
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Fill in your wallet credentials

# 3. Run in paper mode (default)
python main.py

# 4. Run with real orders
python main.py --live
```

## Configuration

All settings loaded from `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `PRIVATE_KEY` | — | Polygon wallet private key |
| `WALLET_ADDRESS` | — | Your wallet address |
| `PAPER_MODE` | `true` | Paper trading mode |
| `MAX_DAILY_LOSS` | `50.0` | Daily loss circuit breaker (USD) |
| `MAX_POSITION_PER_MARKET` | `100.0` | Max position per market (USD) |
| `MIN_EDGE_THRESHOLD` | `0.03` | Minimum edge to enter (3%) |

## Tech Stack

Python 3.10+ · py-clob-client · SQLite · Docker

## License

MIT
