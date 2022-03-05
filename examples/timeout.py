from requests.exceptions import Timeout

from discord_webhook import DiscordEmbed, DiscordWebhook

# We will set ridiculously low timeout threshold for testing purposes
webhook = DiscordWebhook(url="your webhook url", timeout=0.1)

# You can also set timeout later using
# webhook.timeout = 0.1

embed = DiscordEmbed(
    title="Embed Title", description="Your Embed Description", color="03b2f8"
)

webhook.add_embed(embed)

# Handle timeout exception
try:
    response = webhook.execute()
except Timeout as err:
    print(f"Oops! Connection to Discord timed out: {err}")
