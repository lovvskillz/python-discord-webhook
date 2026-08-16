import pytest
from pytest import mark

from discord_webhook import DiscordComponentButton, constants
from discord_webhook.webhook_exceptions import ComponentException


@mark.parametrize(
    "style, field, error_message",
    [
        (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_PRIMARY,
            "custom_id",
            "custom_id needs to be provided as a kwarg.",
        ),
        (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_SECONDARY,
            "custom_id",
            "custom_id needs to be provided as a kwarg.",
        ),
        (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_SUCCESS,
            "custom_id",
            "custom_id needs to be provided as a kwarg.",
        ),
        (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_DANGER,
            "custom_id",
            "custom_id needs to be provided as a kwarg.",
        ),
        (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_LINK,
            "url",
            "url needs to be provided as a kwarg.",
        ),
    ],
)
def test__styles__required_fields(style, field, error_message):
    # valid button
    DiscordComponentButton(**{"style": style, field: "test_string"})

    # required field is missing
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentButton(style=style)

    assert str(excinfo.value) == error_message


@mark.parametrize("invalid_style", [0, 6, "a", True, None])
def test__styles__invalid(invalid_style):
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentButton(style=invalid_style)

    assert (
        str(excinfo.value)
        == "The provided button style is invalid. A valid button style is an integer"
        " between 1 and 5."
    )
