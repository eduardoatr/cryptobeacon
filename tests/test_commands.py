from cryptobeacon.main import app
from typer.testing import CliRunner

runner = CliRunner()


def test_coin_add_non_existing_id() -> None:

    result = runner.invoke(app, ["coin", "add", "not_a_coin_id"])
    assert result.exit_code == 0
    assert result.stdout == "Unable to find the coin with id not_a_coin_id\n"


def test_coin_remove_non_existing_id() -> None:

    result = runner.invoke(app, ["coin", "remove", "not_a_coin_id"])
    assert result.exit_code == 0
    assert result.stdout == "Not_a_coin_id is not on the watchlist\n"
