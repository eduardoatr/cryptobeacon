# 🚨 Beacon

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)

Beacon is a simple command-line interface tool for cryptocurrency alerts directly into your desktop. It uses the free [CoinGecko API](https://www.coingecko.com/en/api/documentation) to obtain the current prices, sending desktop notification when alarm price targets are reached. The application is built in [Python](https://www.python.org/), with the help of [Typer](https://github.com/tiangolo/typer) and [Rich](https://github.com/Textualize/rich).

![watchlist](./imgs/watchlist.png)

## Installation

```Bash
pip install --user beacon
```

## Usage

Tracking your favorite cryptocurrencies with **Beacon** is easy. Start by **adding** them to the watchlist, as follows:

```Bash
beacon coin add bitcoin
```

Confirm the addition using the **show** command:

```Bash
beacon show
```

Next, you need to add a price target for the **alarm**:

```Bash
beacon alarm add bitcoin 21000
```

Finally, **run** the application:

```Bash
beacon run
```

> ⚠️ Additionally, there are commands to **remove** coins and alarms from the watchlist, or even to **clear** it entirely. Use the **help** commando for more specific information.
