from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(
    url="your webhook url",
    rate_limit_retry=True,
    content="Webhook Message",
)
response = webhook.execute()
