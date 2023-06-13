from datetime import datetime

import pytest

from discord_webhook import DiscordEmbed
from discord_webhook.webhook_exceptions import ColorNotInRangeException


@pytest.fixture
def embed():
    return DiscordEmbed()


def test__set_embed__title(embed):
    embed_title = "foobar"

    embed.set_title(embed_title)

    assert embed.title == embed_title


def test__set_embed__description(embed):
    embed_description = "just a short description"

    embed.set_description(embed_description)

    assert embed.description == embed_description


def test__set_embed__url(embed):
    embed_url = "testurl"

    embed.set_url(embed_url)

    assert embed.url == embed_url


@pytest.mark.parametrize(
    "timestamp",
    [
        1679610926,
        1679610926.0,
        datetime.fromisoformat("2023-03-23T22:35:26"),
        datetime.fromisoformat("2023-03-23T23:35:26+01:00"),
    ],
)
def test__set_embed__timestamp(embed, timestamp):
    compare_datetime = datetime.fromisoformat(
        "2023-03-23T22:35:26"
    )  # timestamp 1679610926
    if isinstance(timestamp, datetime):
        compare_datetime = timestamp

    embed.set_timestamp(timestamp)

    assert embed.timestamp == compare_datetime.isoformat()


@pytest.mark.parametrize(
    "color, output",
    [
        ("03b2f8", 242424),
        (333333, 333333),
    ],
)
def test__set_embed__color(embed, color, output):
    embed.set_color(color)

    assert embed.color == output


def test__set_embed__color__out_of_range(embed):
    embed_color = 9999999999

    with pytest.raises(ColorNotInRangeException):
        embed.set_color(embed_color)


def test__set_embed__footer(embed):
    footer_text = "footer text"
    footer_icon_url = "footer icon url"
    footer_proxy_icon_url = "proxied footer icon url"

    embed.set_footer(
        text=footer_text, icon_url=footer_icon_url, proxy_icon_url=footer_proxy_icon_url
    )

    assert embed.footer == {
        "text": footer_text,
        "icon_url": footer_icon_url,
        "proxy_icon_url": footer_proxy_icon_url,
    }


def test__set_embed__image(embed):
    image_url = "image url"
    image_proxy_url = "image proxy url"
    image_height = 500
    image_width = 500

    embed.set_image(
        url=image_url, proxy_url=image_proxy_url, height=image_height, width=image_width
    )

    assert embed.image == {
        "url": image_url,
        "proxy_url": image_proxy_url,
        "height": image_height,
        "width": image_width,
    }


def test__set_embed__thumbnail(embed):
    thumbnail_url = "thumbnail url"
    thumbnail_proxy_url = "thumbnail proxy url"
    thumbnail_height = 500
    thumbnail_width = 500

    embed.set_thumbnail(
        url=thumbnail_url,
        proxy_url=thumbnail_proxy_url,
        height=thumbnail_height,
        width=thumbnail_width,
    )

    assert embed.thumbnail == {
        "url": thumbnail_url,
        "proxy_url": thumbnail_proxy_url,
        "height": thumbnail_height,
        "width": thumbnail_width,
    }


def test__set_embed__video(embed):
    video_url = "video url"
    video_height = 500
    video_width = 500

    embed.set_video(url=video_url, height=video_height, width=video_width)

    assert embed.video == {
        "url": video_url,
        "height": video_height,
        "width": video_width,
    }


def test__set_embed__provider(embed):
    provider_name = "provider name"
    provider_url = "provider url"

    embed.set_provider(name=provider_name, url=provider_url)

    assert embed.provider == {
        "name": provider_name,
        "url": provider_url,
    }


def test__set_embed__author(embed):
    author_name = "author name"
    author_url = "author url"
    author_icon_url = "author icon url"
    author_proxy_icon_url = "author proxy icon url"

    embed.set_author(
        name=author_name,
        url=author_url,
        icon_url=author_icon_url,
        proxy_icon_url=author_proxy_icon_url,
    )

    assert embed.author == {
        "name": author_name,
        "url": author_url,
        "icon_url": author_icon_url,
        "proxy_icon_url": author_proxy_icon_url,
    }


def test__set_embed__field(embed):
    field_name = "field name"
    field_value = "field value"
    field_inline = False

    assert len(embed.fields) == 0

    embed.add_embed_field(name=field_name, value=field_value, inline=field_inline)

    assert len(embed.fields) == 1
    assert embed.fields[0] == {
        "name": field_name,
        "value": field_value,
        "inline": field_inline,
    }
