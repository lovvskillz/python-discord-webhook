import unittest
from datetime import datetime

from discord_webhook import DiscordEmbed
from discord_webhook.webhook_exceptions import ColorNotInRangeException


class TestWebhookEmbed(unittest.TestCase):
    def setUp(self):
        self.embed = DiscordEmbed()

    def test_set_embed_title(self):
        embed_title = "foobar"
        self.embed.set_title(embed_title)
        self.assertEqual(self.embed.title, embed_title)

    def test_set_embed_description(self):
        embed_description = "just a short description"
        self.embed.set_description(embed_description)
        self.assertEqual(self.embed.description, embed_description)

    def test_set_embed_url(self):
        embed_url = "testurl"
        self.embed.set_url(embed_url)
        self.assertEqual(self.embed.url, embed_url)

    def test_set_embed_timestamp(self):
        embed_timestamp = 1658504418.5660195
        self.embed.set_timestamp(embed_timestamp)
        self.assertEqual(self.embed.timestamp,
                         str(datetime.utcfromtimestamp(embed_timestamp)))

    def test_set_embed_color(self):
        embed_color_as_str = "03b2f8"
        embed_color_as_int = int(embed_color_as_str, 16)
        self.embed.set_color(embed_color_as_str)
        self.assertEqual(self.embed.color, embed_color_as_int)
        self.embed.set_color(embed_color_as_int)
        self.assertEqual(self.embed.color, embed_color_as_int)

    def test_embed_color_out_of_range(self):
        embed_color = 9999999999
        with self.assertRaises(ColorNotInRangeException):
            self.embed.set_color(embed_color)

    def test_embed_set_footer(self):
        footer_text = "footer text"
        footer_icon_url = "footer icon url"
        footer_proxy_icon_url = "proxied footer icon url"
        self.embed.set_footer(text=footer_text, icon_url=footer_icon_url,
                              proxy_icon_url=footer_proxy_icon_url)
        self.assertEqual(self.embed.footer, {
            "text": footer_text,
            "icon_url": footer_icon_url,
            "proxy_icon_url": footer_proxy_icon_url
        })

    def test_embed_set_image(self):
        image_url = "image url"
        image_proxy_url = "image proxy url"
        image_height = 500
        image_width = 500
        self.embed.set_image(url=image_url, proxy_url=image_proxy_url,
                             height=image_height, width=image_width)
        self.assertEqual(self.embed.image, {
            "url": image_url,
            "proxy_url": image_proxy_url,
            "height": image_height,
            "width": image_width,
        })

    def test_embed_set_thumbnail(self):
        thumbnail_url = "thumbnail url"
        thumbnail_proxy_url = "thumbnail proxy url"
        thumbnail_height = 500
        thumbnail_width = 500
        self.embed.set_thumbnail(url=thumbnail_url,
                                 proxy_url=thumbnail_proxy_url,
                                 height=thumbnail_height, width=thumbnail_width)
        self.assertEqual(self.embed.thumbnail, {
            "url": thumbnail_url,
            "proxy_url": thumbnail_proxy_url,
            "height": thumbnail_height,
            "width": thumbnail_width,
        })

    def test_embed_set_video(self):
        video_url = "video url"
        video_height = 500
        video_width = 500
        self.embed.set_video(url=video_url, height=video_height,
                             width=video_width)
        self.assertEqual(self.embed.video, {
            "url": video_url,
            "height": video_height,
            "width": video_width,
        })

    def test_embed_set_provider(self):
        provider_name = "provider name"
        provider_url = "provider url"
        self.embed.set_provider(name=provider_name, url=provider_url)
        self.assertEqual(self.embed.provider, {
            "name": provider_name,
            "url": provider_url,
        })

    def test_embed_set_author(self):
        author_name = "author name"
        author_url = "author url"
        author_icon_url = "author icon url"
        author_proxy_icon_url = "author proxy icon url"
        self.embed.set_author(name=author_name, url=author_url,
                              icon_url=author_icon_url,
                              proxy_icon_url=author_proxy_icon_url)
        self.assertEqual(self.embed.author, {
            "name": author_name,
            "url": author_url,
            "icon_url": author_icon_url,
            "proxy_icon_url": author_proxy_icon_url,
        })

    def test_embed_set_field(self):
        field_counter = 0
        field_name = "field name"
        field_value = "field value"
        field_inline = False
        self.assertEqual(len(self.embed.fields), field_counter)
        self.embed.add_embed_field(name=field_name, value=field_value,
                                   inline=field_inline)
        self.assertEqual(len(self.embed.fields), field_counter + 1)
        self.assertEqual(self.embed.fields[0], {
                "name": field_name,
                "value": field_value,
                "inline": field_inline,
            })
