import typer
from requests import RequestException
from utils.coins import load_coins, save_coins

app = typer.Typer()


@app.command()
def add(ctx: typer.Context, id_coin: str, value: float) -> None:

    try:

        coin = load_coins(ctx, id_coin)[id_coin]

        try:

            coin.set_alarm(value)
            save_coins(ctx, [coin])

            ctx.obj["CONSOLE"].print(
                f"The [green]{value}[/green] alarm was set to [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

        except ValueError:
            ctx.obj["CONSOLE"].print(
                f"The [magenta]{value}[/magenta] alarm is the current price of {id_coin.capitalize()}",
                style="bold",
            )

    except KeyError:
        ctx.obj["CONSOLE"].print(
            f"[magenta]{id_coin.capitalize()}[/magenta] is not on the watchlist",
            style="bold",
        )

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except RequestException as e:

        if e.response.status_code == 404:
            ctx.obj["CONSOLE"].print(
                f"Unable to find the coin with id [red]{id_coin}[/red]",
                style="bold",
            )

        else:
            ctx.obj["CONSOLE"].print(
                f"Request error: [red]{e}[/red]",
                style="bold",
            )


@app.command()
def remove(ctx: typer.Context, id_coin: str, value: float) -> None:

    try:

        coin = load_coins(ctx, id_coin)[id_coin]

        try:

            coin.remove_alarm(value)
            save_coins(ctx, [coin])

            ctx.obj["CONSOLE"].print(
                f"The [green]{value}[/green] alarm was removed from [blue]{id_coin.capitalize()}[/blue]",
                style="bold",
            )

        except KeyError:
            ctx.obj["CONSOLE"].print(
                f"There is no [magenta]{value}[/magenta] alarm on {id_coin.capitalize()}",
                style="bold",
            )

    except KeyError:
        ctx.obj["CONSOLE"].print(
            f"[magenta]{id_coin.capitalize()}[/magenta] is not on the watchlist",
            style="bold",
        )

    except FileNotFoundError:
        ctx.obj["CONSOLE"].print(
            "Missing the [red]configurations[/red] file", style="bold"
        )

    except RequestException as e:

        if e.response.status_code == 404:
            ctx.obj["CONSOLE"].print(
                f"Unable to find the coin with id [red]{id_coin}[/red]",
                style="bold",
            )

        else:
            ctx.obj["CONSOLE"].print(
                f"Request error: [red]{e}[/red]",
                style="bold",
            )
