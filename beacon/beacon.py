from configparser import ConfigParser
from pathlib import Path
from time import sleep

import typer
from requests.exceptions import RequestException
from rich.console import Console

import commands.alarm as alarm
import commands.coin as coin
from utils.apis import API
from utils.coins import list_coins, load_coins, save_coins

app = typer.Typer()
app.add_typer(coin.app, name="coin")
app.add_typer(alarm.app, name="alarm")

__FILE_CONFIG = "coins.ini"


@app.command()
def clear(ctx: typer.Context) -> None:

    clear = typer.confirm("Clear the watchlist?")

    if clear:

        ctx.obj["PARSER"].clear()

        try:

            with ctx.obj["FILE"].open("w") as f:
                ctx.obj["PARSER"].write(f)

            ctx.obj["CONSOLE"].print(
                "The watchlist was [green]cleared[/green]", style="bold"
            )

        except FileNotFoundError:
            ctx.obj["CONSOLE"].print(
                "Missing the [red]configurations[/red] file", style="bold"
            )

    else:
        ctx.obj["CONSOLE"].print("Operation [red]cancelled[/red]", style="bold")


@app.command()
def show(ctx: typer.Context) -> None:

    try:

        coins = load_coins(ctx, ",".join(ctx.obj["PARSER"].sections()))
        list_coins(ctx, coins)

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except RequestException as e:
        ctx.obj["CONSOLE"].print(f"Request error: [red]{e}[/red]", style="bold")


@app.command()
def run(ctx: typer.Context, refresh: int = 45) -> None:

    try:

        coins = load_coins(ctx, ",".join(ctx.obj["PARSER"].sections()))

        while True:

            prices = ctx.obj["API"].get_price(",".join(coins.keys()))

            for coin_id in coins:
                coins[coin_id].update_price(float(prices[coin_id]["usd"]))
                coins[coin_id].check_alarms()

            ctx.obj["CONSOLE"].clear()
            list_coins(ctx, coins)
            save_coins(ctx, list(coins.values()))

            sleep(refresh)

    except RequestException as e:
        ctx.obj["CONSOLE"].print(f"Request error: [red]{e}[/red]", style="bold")


@app.callback()
def load(ctx: typer.Context) -> None:
    """TODO"""

    path_configs = typer.get_app_dir("beacon")

    ctx.obj = {
        "CONSOLE": Console(),
        "FILE": Path(f"{path_configs}/{__FILE_CONFIG}"),
        "API": API(),
        "PARSER": ConfigParser(),
    }

    if not ctx.obj["FILE"].exists():
        ctx.obj["FILE"].parent.mkdir(exist_ok=True, parents=True)

    try:

        ctx.obj["PARSER"].read(ctx.obj["FILE"].absolute())

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )


if __name__ == "__main__":
    app()
