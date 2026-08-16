import pytest

from discord_webhook import DiscordComponentButton, DiscordComponentEmoji
from discord_webhook.webhook_exceptions import ComponentException


def test__emoji__unicode():
    assert DiscordComponentEmoji(name="🔥").to_dict() == {
        "name": "🔥",
        "animated": False,
    }


def test__emoji__custom():
    assert DiscordComponentEmoji(name="blob", id="123", animated=True).to_dict() == {
        "name": "blob",
        "id": "123",
        "animated": True,
    }


def test__emoji__missing_name_and_id():
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentEmoji()

    assert str(excinfo.value) == "Either name or id needs to be provided."


def test__emoji__in_button():
    button = DiscordComponentButton(
        custom_id="test", label="fire", emoji=DiscordComponentEmoji(name="🔥")
    )

    assert button.to_dict()["emoji"] == {"name": "🔥", "animated": False}
