from discord_webhook import DiscordWebhook

proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}
webhook = DiscordWebhook(
    url="your webhook url", content="Webhook Message", proxies=proxies
)
response = webhook.execute()
