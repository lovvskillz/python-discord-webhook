from discord_webhook import DiscordEmbed, DiscordWebhook

webhook = DiscordWebhook(url="your webhook url")

with open("path/to/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename="example.jpg")

embed = DiscordEmbed(
    title="Embed Title", description="Your Embed Description", color=242424
)
embed.set_thumbnail(url="attachment://example.jpg")

webhook.add_embed(embed)
response = webhook.execute()
