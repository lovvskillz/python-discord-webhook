import pytest

from discord_webhook.components import BaseDiscordComponent
from discord_webhook import constants
from discord_webhook.webhook_exceptions import ComponentException


def test__component__types():
    for component_type in constants.DISCORD_COMPONENT_TYPES:

        class TestDiscordComponent(BaseDiscordComponent):
            type = component_type

        TestDiscordComponent()

    for component_type in [0, 9, "a", True]:

        class TestDiscordComponent(BaseDiscordComponent):
            type = component_type

        with pytest.raises(ComponentException) as excinfo:
            TestDiscordComponent()

        assert (
            str(excinfo.value)
            == "The provided component type is invalid. A valid component type is an"
            " integer between 1 and 8."
        )


def test__component__custom_id_max_length():
    class TestDiscordComponent(BaseDiscordComponent):
        type = constants.DISCORD_COMPONENT_TYPE_BUTTON

    custom_id = "".join("a" for i in range(100))

    TestDiscordComponent(custom_id=custom_id)

    # total length of 101 chars
    with pytest.raises(ComponentException) as excinfo:
        TestDiscordComponent(custom_id=f"{custom_id}a")

    assert str(excinfo.value) == "custom_id can be a maximum of 100 characters."
