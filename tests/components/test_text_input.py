import pytest
from pytest import mark

from discord_webhook import DiscordComponentTextInput, constants
from discord_webhook.webhook_exceptions import ComponentException


def test__text_input__defaults():
    text_input = DiscordComponentTextInput(custom_id="test", label="Your name")

    assert text_input.to_dict() == {
        "type": constants.DISCORD_COMPONENT_TYPE_TEXT_INPUT,
        "custom_id": "test",
        "label": "Your name",
        "style": constants.DISCORD_COMPONENT_TEXT_INPUT_STYLE_SHORT,
        "required": True,
    }


def test__text_input__paragraph():
    text_input = DiscordComponentTextInput(
        custom_id="test",
        label="Your feedback",
        style=constants.DISCORD_COMPONENT_TEXT_INPUT_STYLE_PARAGRAPH,
        placeholder="Tell us more",
        min_length=10,
        max_length=1000,
        required=False,
    )
    data = text_input.to_dict()

    assert data["style"] == constants.DISCORD_COMPONENT_TEXT_INPUT_STYLE_PARAGRAPH
    assert data["min_length"] == 10
    assert data["max_length"] == 1000
    assert data["placeholder"] == "Tell us more"
    assert data["required"] is False


@mark.parametrize("invalid_style", [0, 3, "a", True, None])
def test__text_input__invalid_style(invalid_style):
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentTextInput(custom_id="test", label="test", style=invalid_style)

    assert (
        str(excinfo.value)
        == "The provided text input style is invalid. A valid text input style is an"
        " integer between 1 and 2."
    )


@mark.parametrize(
    "kwargs, error_message",
    [
        ({"label": "a" * 46}, "label can be a maximum of 45 characters."),
        (
            {"placeholder": "a" * 101},
            "placeholder can be a maximum of 100 characters.",
        ),
        ({"value": "a" * 4001}, "value can be a maximum of 4000 characters."),
    ],
)
def test__text_input__max_lengths(kwargs, error_message):
    input_kwargs = {"custom_id": "test", "label": "test"}
    input_kwargs.update(kwargs)

    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentTextInput(**input_kwargs)

    assert str(excinfo.value) == error_message
