# 🤖 PolyTrader — Quantitative Polymarket Prediction Market Bot

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Mode](https://img.shields.io/badge/Paper%20Trading-Supported-emerald.svg)]()
[![Risk Engine](https://img.shields.io/badge/Kelly%20Criterion-Half%20Kelly-amber.svg)]()

**PolyTrader** is a high-performance, automated quantitative trading engine designed for prediction markets on **Polymarket**. It performs real-time market scanning, outcome token mispricing detection, bid-ask spread market making, and momentum trading while adhering to rigorous risk management controls (Half-Kelly sizing and daily loss circuit breakers).

---

## 🌟 Key Features

- ⚡ **Asynchronous Market Scanner**: Scans high-liquidity Polymarket orderbooks for mispricings.
- 🎯 **YES/NO Riskless Arbitrage Engine**: Automatically identifies and acts on mispriced outcome pairs where `YES_ask + NO_ask < 1.00`.
- 📊 **Bid-Ask Market Making**: Quotes liquidity on wide prediction spreads while managing inventory skew.
- 📈 **Probability Momentum Strategy**: Catches high-volume breakouts on trending prediction topics.
- 🧮 **Half-Kelly Position Sizing**: Dynamically calculates optimal position sizes based on odds and edge to minimize ruin probability.
- 🚨 **Automated Circuit Breaker**: Halts trading automatically if daily drawdown or exposure limits are exceeded.
- 💾 **SQLite Trade Logging**: Comprehensive database persistence tracking filled trades, edges, and PnL.
- 🧪 **Paper Trading Simulator**: Test strategies safely without risking real capital.

---

## 📐 System Architecture

```
                                  +-----------------------------+
                                  |   Polymarket Gamma/CLOB API  |
                                  +--------------+--------------+
                                                 |
                                                 v
                                  +--------------+--------------+
                                  |     Market Scanner Engine    |
                                  +--------------+--------------+
                                                 |
                                                 v
                     +---------------------------+---------------------------+
                     |                           |                           |
                     v                           v                           v
          +----------+----------+     +----------+----------+     +----------+----------+
          |  Arbitrage Strategy |     |   Market Maker Strat|     |  Momentum Strategy  |
          +----------+----------+     +----------+----------+     +----------+----------+
                     |                           |                           |
                     +---------------------------+---------------------------+
                                                 |
                                                 v
                                  +--------------+--------------+
                                  |     Risk Engine & Sizing    |
                                  |    (Half-Kelly & Breaker)   |
                                  +--------------+--------------+
                                                 |
                                                 v
                                  +--------------+--------------+
                                  |   Execution / Paper Sim     |
                                  +--------------+--------------+
                                                 |
                                                 v
                                  +--------------+--------------+
                                  |     SQLite Trade Logger     |
                                  +-----------------------------+
```

---

## ⚙️ Quick Start

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AbinashBalaraman/Polymarket-Bot.git
   cd Polymarket-Bot
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment (`.env`):**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to configure paper trading, bankroll, and risk limits:
   ```env
   PAPER_MODE=true
   BANKROLL_USD=10000.0
   KELLY_FRACTION=0.5
   MAX_POSITION_SIZE_USD=500.0
   MAX_DAILY_LOSS_USD=200.0
   MIN_ARBITRAGE_EDGE=0.015
   ```

4. **Launch PolyTrader:**
   ```bash
   python main.py
   ```

---

## 🧮 Mathematical Basis

### Riskless YES/NO Arbitrage
In binary prediction markets, the true settlement value of outcome $YES$ plus $NO$ always equals $1.00$. If orderbook asks present:

$$\text{Cost} = P_{\text{YES, ask}} + P_{\text{NO, ask}} < 1.00$$

The guaranteed profit percentage $E$ is:

$$E = \frac{1.00 - \text{Cost}}{\text{Cost}}$$

### Half-Kelly Sizing Formula
For probabilistic signals:

$$f^* = \frac{b \cdot p - q}{b} \times 0.5$$

Where $p$ is signal probability, $q = 1 - p$, and $b = (1 - P) / P$.

---

## 📄 License
MIT License. Provided for educational and algorithmic trading demonstration purposes.