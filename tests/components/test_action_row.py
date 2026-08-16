import pytest
from pytest import mark

from discord_webhook import (
    DiscordComponentActionRow,
    DiscordComponentButton,
    DiscordComponentStringSelect,
    DiscordComponentTextInput,
    DiscordSelectOption,
    constants,
)
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


def _exclusive_components():
    return [
        DiscordComponentStringSelect(
            custom_id="select", options=[DiscordSelectOption(label="a", value="a")]
        ),
        DiscordComponentTextInput(custom_id="input", label="test"),
    ]


@mark.parametrize("component", _exclusive_components())
def test__exclusive_component__with_existing_button(component):
    action_row = DiscordComponentActionRow(
        components=[DiscordComponentButton(custom_id="test")]
    )

    with pytest.raises(ComponentException) as excinfo:
        action_row.add_component(component)

    assert (
        str(excinfo.value)
        == "A select menu or text input has to be the only component in an action row."
    )
    assert len(action_row.components) == 1


@mark.parametrize("component", _exclusive_components())
def test__exclusive_component__followed_by_button(component):
    action_row = DiscordComponentActionRow(components=[component])

    with pytest.raises(ComponentException) as excinfo:
        action_row.add_component(DiscordComponentButton(custom_id="test"))

    assert (
        str(excinfo.value)
        == "A select menu or text input has to be the only component in an action row."
    )
    assert len(action_row.components) == 1


def test__action_row__to_dict():
    action_row = DiscordComponentActionRow(
        components=[
            DiscordComponentButton(custom_id="test", label="Click me", disabled=True)
        ]
    )

    assert action_row.to_dict() == {
        "type": constants.DISCORD_COMPONENT_TYPE_ACTION_ROW,
        "components": [
            {
                "type": constants.DISCORD_COMPONENT_TYPE_BUTTON,
                "style": constants.DISCORD_COMPONENT_BUTTON_STYLE_PRIMARY,
                "custom_id": "test",
                "label": "Click me",
                "disabled": True,
            }
        ],
    }
