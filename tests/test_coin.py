from cryptobeacon.utils.coins import Coin
from pytest import fixture


@fixture
def coin() -> Coin:

    return Coin(
        id="bitcoin",
        name="Bitcoin",
        symbol="BTC",
        price_current=10.0,
        price_previous=7.0,
        alarms_down={9.0, 11.0},
        alarms_up={11.0, 9.0},
    )


def test_post_init_up_alarm_cleaning(coin: Coin) -> None:
    assert coin.alarms_up == {11.0}


def test_post_init_down_alarm_cleaning(coin: Coin) -> None:
    assert coin.alarms_down == {9.0}


def test_update_price(coin: Coin) -> None:

    coin.update_price(15.0)

    assert coin.price_current == 15.0
    assert coin.price_previous == 10.0


def test_check_alarm_up(coin: Coin) -> None:

    coin.update_price(15.0)
    coin.check_alarms(False)

    assert coin.alarms_up == set()
    assert coin.alarms_down == {9.0}


def test_check_alarm_down(coin: Coin) -> None:

    coin.update_price(6.0)
    coin.check_alarms(False)

    assert coin.alarms_up == {11.0}
    assert coin.alarms_down == set()


def test_set_alarm(coin: Coin) -> None:

    coin.set_alarm(15.0)
    coin.set_alarm(6.0)

    assert coin.alarms_up == {11.0, 15.0}
    assert coin.alarms_down == {9.0, 6.0}


def test_remove_alarm(coin: Coin) -> None:

    coin.remove_alarm(11.0)
    coin.remove_alarm(9.0)

    assert coin.alarms_up == set()
    assert coin.alarms_down == set()
