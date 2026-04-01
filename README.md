# PolyTrader — Prediction Market Arbitrage Bot

## Overview
PolyTrader is an automated, high-frequency prediction market bot executing across the Polymarket infrastructure. The system performs real-time spread analysis and arbitrage detection with strict risk management controls, enforcing mathematically optimal position sizing frameworks such as the Half-Kelly criterion.

## Architecture & Technology Stack
*   **Backend Server**: Python 3.10+
*   **API Interoperability**: REST APIs, WebSockets
*   **Data Persistence**: SQLite Database Integration
*   **Containerization**: Docker
*   **Risk Engine**: Custom Circuit Breaker & Exposure Management modules

## Core Features
*   **Arbitrage Engine**: Asynchronous scanning of YES+NO bid limits ensuring execution spreads resolve beneath cost-basis configurations.
*   **Quantitative Sizing**: Dynamic Half-Kelly fraction application for conservative capital allocation.
*   **Circuit Breakers**: Hard daily loss limits averting systemic trading failures.
*   **State Persistence**: Complete, fault-tolerant execution mapping stored securely via local SQLite integration.

## Setup and Installation

### Prerequisites
*   Python 3.10+
*   Polygon Wallet Private Key
*   Docker (Optional)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AbinashBalaraman/Polymarket-Bot.git
   cd Polymarket-Bot
   ```
2. Install standard Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure authentication within `.env`:
   ```env
   PRIVATE_KEY=your_polygon_wallet_key
   PAPER_MODE=true
   ```
4. Initialize the execution loop:
   ```bash
   python main.py
   ```

## License
Provided for portfolio demonstration and educational purposes.