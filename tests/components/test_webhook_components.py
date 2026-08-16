import pytest

from discord_webhook import (
    DiscordComponentActionRow,
    DiscordComponentButton,
    DiscordWebhook,
    constants,
)
from discord_webhook.webhook_exceptions import ComponentException


def _action_row():
    return DiscordComponentActionRow(
        components=[
            DiscordComponentButton(
                style=constants.DISCORD_COMPONENT_BUTTON_STYLE_LINK,
                label="GitHub",
                url="https://github.com/lovvskillz/python-discord-webhook",
            )
        ]
    )


def test__webhook__add_component_row():
    webhook = DiscordWebhook(url="webhook_url", content="test")
    webhook.add_component_row(_action_row())

    assert webhook.json["components"] == [
        {
            "type": constants.DISCORD_COMPONENT_TYPE_ACTION_ROW,
            "components": [
                {
                    "type": constants.DISCORD_COMPONENT_TYPE_BUTTON,
                    "style": constants.DISCORD_COMPONENT_BUTTON_STYLE_LINK,
                    "label": "GitHub",
                    "url": "https://github.com/lovvskillz/python-discord-webhook",
                    "disabled": False,
                }
            ],
        }
    ]


def test__webhook__components_kwarg():
    webhook = DiscordWebhook(
        url="webhook_url", content="test", components=[_action_row()]
    )

    assert len(webhook.get_component_rows()) == 1


def test__webhook__components_are_not_shared_between_instances():
    webhook_1 = DiscordWebhook(url="webhook_url", content="test")
    webhook_1.add_component_row(_action_row())
    webhook_2 = DiscordWebhook(url="webhook_url", content="test")

    assert webhook_2.get_component_rows() == []


def test__webhook__remove_component_rows():
    webhook = DiscordWebhook(url="webhook_url", content="test")
    webhook.add_component_row(_action_row())
    webhook.add_component_row(_action_row())

    webhook.remove_component_row(0)
    assert len(webhook.get_component_rows()) == 1

    webhook.remove_component_rows()
    assert webhook.get_component_rows() == []
    assert "components" not in webhook.json


def test__webhook__max_action_rows():
    webhook = DiscordWebhook(url="webhook_url", content="test")
    for _ in range(constants.DISCORD_MAX_ACTION_ROWS):
        webhook.add_component_row(_action_row())

    with pytest.raises(ComponentException) as excinfo:
        webhook.add_component_row(_action_row())

    assert str(excinfo.value) == "A message can contain up to 5 action rows."
    assert len(webhook.get_component_rows()) == constants.DISCORD_MAX_ACTION_ROWS
