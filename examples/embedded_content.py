from discord_webhook import DiscordEmbed, DiscordWebhook

webhook = DiscordWebhook(url="your webhook url")

# create embed object for webhook
embed = DiscordEmbed(
    title="Your Title", description="Lorem ipsum dolor sit", color=242424
)

# set author
embed.set_author(name="Author Name", url="author url", icon_url="author icon url")

# set image
embed.set_image(url="your image url")

# set thumbnail
embed.set_thumbnail(url="your thumbnail url")

# set footer
embed.set_footer(text="Embed Footer Text")

# set timestamp (default is now)
embed.set_timestamp()

# add fields to embed
embed.add_embed_field(name="Field 1", value="Lorem ipsum")
embed.add_embed_field(name="Field 2", value="dolor sit")

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()
