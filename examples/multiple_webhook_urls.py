from discord_webhook import DiscordWebhook

webhook_urls = ["webhook url 1", "webhook url 2"]
webhook = DiscordWebhook(url=webhook_urls, content="Webhook Message")
response = webhook.execute()
