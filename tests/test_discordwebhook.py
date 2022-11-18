import unittest

from discord_webhook.webhook import DiscordWebhook


class TestHermesApi(unittest.TestCase):
    """
    Webhook Tests
    """

    def test_discordwebhook_constructor(self):
        webhook = DiscordWebhook("testurl")
        self.assertEqual(webhook.url, "testurl")

    def test_set_content(self):
        test_content = "Test data"
        webhook = DiscordWebhook("testurl")
        webhook.set_content(test_content)
        self.assertEqual(webhook.content, test_content)

    def test_batch_create(self):
        urls = ["first_url", "second_url"]
        webhook1, webhook2 = DiscordWebhook.create_batch(urls, content="Test")
        self.assertTrue(isinstance(webhook1, DiscordWebhook))
        self.assertTrue(isinstance(webhook2, DiscordWebhook))
        self.assertEqual(webhook1.url, urls[0])
        self.assertEqual(webhook2.url, urls[1])
        self.assertEqual(webhook1.content, "Test")
        self.assertEqual(webhook2.content, "Test")

    def test_batch_create__url_as_kwarg(self):
        urls = ["first_url", "second_url"]
        with self.assertRaises(TypeError):
            webhook1, webhook2 = DiscordWebhook.create_batch(urls, url="wrong")
