import pytest

from discord_webhook import DiscordComponentButton, DiscordComponentActionRow
from discord_webhook.webhook_exceptions import ComponentException


def test__action_row_in_action_row():
    action_row_1 = DiscordComponentActionRow()
    action_row_2 = DiscordComponentActionRow()

    with pytest.raises(ComponentException) as excinfo:
        action_row_1.add_component(action_row_2)

    assert str(excinfo.value) == "An action row can't contain another action row."
    assert len(action_row_1.components) == 0


def test__max_buttons():
    action_row = DiscordComponentActionRow()
    button = DiscordComponentButton(custom_id="test")
    for _ in range(0, 5):
        action_row.add_component(button)

    with pytest.raises(ComponentException) as excinfo:
        action_row.add_component(button)

    assert str(excinfo.value) == "An Action Row can contain up to 5 buttons."
    assert len(action_row.components) == 5
