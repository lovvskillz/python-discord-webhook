import pytest

from discord_webhook.webhook import DiscordWebhook


def test__set_content():
    test_content = "Test data"
    webhook = DiscordWebhook("testurl")

    webhook.set_content(test_content)

    assert webhook.content == test_content


def test__batch_create():
    urls = ["first_url", "second_url"]
    content = "Test"

    webhook1, webhook2 = DiscordWebhook.create_batch(urls, content=content)

    assert isinstance(webhook1, DiscordWebhook)
    assert isinstance(webhook2, DiscordWebhook)
    assert webhook1.url == urls[0]
    assert webhook2.url == urls[1]
    assert webhook1.content == content
    assert webhook2.content == content


def test__batch_create__url_as_kwarg():
    urls = ["first_url", "second_url"]

    with pytest.raises(TypeError):
        webhook1, webhook2 = DiscordWebhook.create_batch(urls, url="wrong")
