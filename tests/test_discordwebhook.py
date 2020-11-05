import unittest
from discord_webhook.webhook import DiscordWebhook


class TestHermesApi(unittest.TestCase):
    """Tests to exercise webhooks
    """

    def test_discordwebhook_constructor(self):
        """
        Discordwebhook url exists.

        Args:
            self: (todo): write your description
        """
        webhook = DiscordWebhook("testurl")
        self.assertEqual(webhook.url, "testurl")

    def test_set_content(self):
        """
        Sets the test content.

        Args:
            self: (todo): write your description
        """
        test_content = "Test data"
        webhook = DiscordWebhook("testurl")
        webhook.set_content(test_content)
        self.assertEqual(webhook.content, test_content)
