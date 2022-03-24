from discord_webhook import DiscordEmbed, DiscordWebhook

webhook = DiscordWebhook(url="your webhook url", username="Webhook with files")

# send two images
with open("path/to/first/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename="example.jpg")
with open("path/to/second/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename="example2.jpg")

response = webhook.execute()
