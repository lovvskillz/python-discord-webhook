import pytest
from pytest import mark

from discord_webhook import (
    DiscordComponentChannelSelect,
    DiscordComponentMentionableSelect,
    DiscordComponentRoleSelect,
    DiscordComponentStringSelect,
    DiscordComponentUserSelect,
    DiscordSelectOption,
    constants,
)
from discord_webhook.webhook_exceptions import ComponentException

AUTO_POPULATED_SELECTS = [
    (DiscordComponentUserSelect, constants.DISCORD_COMPONENT_TYPE_USER_SELECT, "user"),
    (DiscordComponentRoleSelect, constants.DISCORD_COMPONENT_TYPE_ROLE_SELECT, "role"),
    (
        DiscordComponentMentionableSelect,
        constants.DISCORD_COMPONENT_TYPE_MENTIONABLE_SELECT,
        "user",
    ),
    (
        DiscordComponentChannelSelect,
        constants.DISCORD_COMPONENT_TYPE_CHANNEL_SELECT,
        "channel",
    ),
]


@mark.parametrize("select_class, component_type, _", AUTO_POPULATED_SELECTS)
def test__auto_populated_selects__type(select_class, component_type, _):
    assert select_class(custom_id="test").to_dict()["type"] == component_type


@mark.parametrize("select_class, _, value_type", AUTO_POPULATED_SELECTS)
def test__auto_populated_selects__default_values(select_class, _, value_type):
    select = select_class(custom_id="test")
    select.add_default_value(123456789)

    assert select.to_dict()["default_values"] == [
        {"id": "123456789", "type": value_type}
    ]


def test__default_values__invalid_type():
    select = DiscordComponentUserSelect(custom_id="test")

    with pytest.raises(ComponentException) as excinfo:
        select.add_default_value(123456789, value_type="invalid")

    assert (
        str(excinfo.value)
        == 'The type of a default value needs to be "user", "role" or "channel".'
    )


def test__string_select__options():
    select = DiscordComponentStringSelect(
        custom_id="test",
        options=[DiscordSelectOption(label="first", value="1")],
        placeholder="choose",
    )
    select.add_option({"label": "second", "value": "2"})

    assert select.to_dict() == {
        "type": constants.DISCORD_COMPONENT_TYPE_STRING_SELECT,
        "custom_id": "test",
        "placeholder": "choose",
        "disabled": False,
        "min_values": 1,
        "max_values": 1,
        "options": [
            {"label": "first", "value": "1", "default": False},
            {"label": "second", "value": "2"},
        ],
    }


def test__string_select__max_options():
    select = DiscordComponentStringSelect(custom_id="test")
    for index in range(constants.DISCORD_MAX_SELECT_OPTIONS):
        select.add_option(DiscordSelectOption(label=str(index), value=str(index)))

    with pytest.raises(ComponentException) as excinfo:
        select.add_option(DiscordSelectOption(label="too much", value="26"))

    assert str(excinfo.value) == "A select menu can contain up to 25 options."
    assert len(select.options) == constants.DISCORD_MAX_SELECT_OPTIONS


@mark.parametrize(
    "kwargs, error_message",
    [
        ({"min_values": 26}, "min_values needs to be an integer between 0 and 25."),
        ({"min_values": -1}, "min_values needs to be an integer between 0 and 25."),
        ({"max_values": 0}, "max_values needs to be an integer between 1 and 25."),
        ({"max_values": "a"}, "max_values needs to be an integer between 1 and 25."),
        (
            {"placeholder": "a" * 151},
            "placeholder can be a maximum of 150 characters.",
        ),
    ],
)
def test__select__invalid_values(kwargs, error_message):
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentStringSelect(custom_id="test", **kwargs)

    assert str(excinfo.value) == error_message


def test__select__missing_custom_id():
    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentStringSelect(custom_id="")

    assert str(excinfo.value) == "custom_id needs to be provided."


def test__channel_select__channel_types():
    select = DiscordComponentChannelSelect(
        custom_id="test", channel_types=[constants.DISCORD_CHANNEL_TYPE_GUILD_TEXT]
    )

    assert select.to_dict()["channel_types"] == [
        constants.DISCORD_CHANNEL_TYPE_GUILD_TEXT
    ]

    with pytest.raises(ComponentException) as excinfo:
        DiscordComponentChannelSelect(custom_id="test", channel_types=[99])

    assert str(excinfo.value) == "99 is not a valid channel type."


@mark.parametrize(
    "kwargs, error_message",
    [
        ({"label": "a" * 101}, "label can be a maximum of 100 characters."),
        ({"value": "a" * 101}, "value can be a maximum of 100 characters."),
        (
            {"description": "a" * 101},
            "description can be a maximum of 100 characters.",
        ),
    ],
)
def test__select_option__max_lengths(kwargs, error_message):
    option_kwargs = {"label": "test", "value": "test"}
    option_kwargs.update(kwargs)

    with pytest.raises(ComponentException) as excinfo:
        DiscordSelectOption(**option_kwargs)

    assert str(excinfo.value) == error_message
