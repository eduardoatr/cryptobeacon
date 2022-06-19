import os
from dataclasses import dataclass
from importlib import resources
from typing import Dict, List, Mapping, Set

import typer
from rich import box
from rich.table import Table

_FILE_ICON = "beacon.ico"


@dataclass
class Coin:
    id: str
    name: str
    symbol: str

    price_current: float
    price_previous: float

    alarms_down: Set[float]
    alarms_up: Set[float]

    def __post_init__(self) -> None:
        """Cleans old alarms that have already been reached."""

        list_remove = []

        for alarm in self.alarms_down:
            if alarm > self.price_current:
                list_remove.append(alarm)

        for alarm in list_remove:
            self.alarms_down.remove(alarm)

        list_remove = []

        for alarm in self.alarms_up:
            if alarm < self.price_current:
                list_remove.append(alarm)

        for alarm in list_remove:
            self.alarms_up.remove(alarm)

    def update_price(self, value) -> None:

        self.price_previous = self.price_current
        self.price_current = value

    def set_alarm(self, value: float) -> None:

        if value > self.price_current:
            self.alarms_up.add(value)

        elif value < self.price_current:
            self.alarms_down.add(value)

        else:
            raise ValueError

    def remove_alarm(self, value: float) -> None:

        if value > self.price_current:
            self.alarms_up.remove(value)

        else:
            self.alarms_down.remove(value)

    def check_alarms(self) -> None:

        list_remove = []

        if self.price_current > self.price_previous:

            for alarm in self.alarms_up:
                if alarm <= self.price_current:
                    list_remove.append(alarm)

            for alarm in list_remove:
                self.alarms_up.remove(alarm)
                self.ring_alarm()

        else:

            for alarm in self.alarms_down:
                if alarm > self.price_current:
                    list_remove.append(alarm)

            for alarm in list_remove:
                self.alarms_down.remove(alarm)
                self.ring_alarm()

    def ring_alarm(self) -> None:

        os.system(
            f'notify-send "The price of {self.name} has reached {self.price_current}" -i "{resources.path("assets", _FILE_ICON)}"'
        )


def string_2_set(alarms: str) -> Set[float]:

    values = []

    if alarms:
        values = alarms.split(" ")
        values = [float(value) for value in values]

    return set(values)


def set_to_string(alarms: Set[float]) -> str:

    values = [str(value) for value in alarms]

    return " ".join(values)


def load_coins(ctx: typer.Context, coins: str) -> Dict[str, Coin]:

    coin_dict = {}
    prices = ctx.obj["API"].get_price(coins)

    if coins:
        for coin_id in coins.split(","):

            coin_info = ctx.obj["PARSER"][coin_id]
            price_previous = float(coin_info["price_current"])
            price_current = float(prices[coin_id]["usd"])

            coin_dict[coin_id] = Coin(
                id=coin_info["id"],
                name=coin_info["name"],
                symbol=coin_info["symbol"],
                price_current=price_current,
                price_previous=price_previous,
                alarms_down=string_2_set(coin_info["alarms_down"]),
                alarms_up=string_2_set(coin_info["alarms_up"]),
            )

    return coin_dict


def save_coins(ctx: typer.Context, coin_list: List[Coin]) -> None:

    for coin in coin_list:

        ctx.obj["PARSER"][coin.id] = {
            "id": coin.id,
            "name": coin.name,
            "symbol": coin.symbol,
            "price_current": str(coin.price_current),
            "price_previous": str(coin.price_previous),
            "alarms_down": set_to_string(coin.alarms_down),
            "alarms_up": set_to_string(coin.alarms_up),
        }

    with ctx.obj["FILE"].open("w") as f:
        ctx.obj["PARSER"].write(f)


def list_coins(ctx: typer.Context, coin_list: Mapping[str, Coin]) -> None:

    list_table = Table(
        title="\n🔎 [underline]WATCHLIST",
        show_header=True,
        title_style="bold",
        header_style="bold",
        show_lines=True,
        box=box.ROUNDED,
    )
    list_table.add_column("#")
    list_table.add_column("[blue]Coin")
    list_table.add_column("[magenta]Symbol")
    list_table.add_column("[yellow]$ Price")
    list_table.add_column("[green]▲ Up")
    list_table.add_column("[red]▼ Down")

    for index, key in enumerate(coin_list):

        coin = coin_list[key]
        list_table.add_row(
            str(index + 1),
            coin.name,
            coin.symbol.upper(),
            str(coin.price_current),
            set_to_string(coin.alarms_up),
            set_to_string(coin.alarms_down),
        )

    ctx.obj["CONSOLE"].print(list_table)
