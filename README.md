# python-discord-webhook

execute discord webhooks

## Examples

execute basic webhook
```python
from discord_webhook.webhook import DiscordWebhook

webhook = DiscordWebhook(url='your webhook url', content='Webhook Message')
webhook.execute()
```

execute webhook with embedded content
```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# add embed object to webhook
webhook.add_embed(embed)

webhook.execute()
```

add some data to embedded content
```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# set author
embed.set_author(name='Author Name', url='author url', icon_url='author icon url')

# set image
embed.set_image(url='your image url')

# set thumbnail
embed.set_thumbnail(url='your thumbnail url')

# set footer
embed.set_footer(text='Embed Footer Text')

# set timestamp (default is now)
embed.set_timestamp()

# add embed object to webhook
webhook.add_embed(embed)

# add fields to embed
embed.add_embed_field(name='Field 1', value='Lorem ipsum')
embed.add_embed_field(name='Field 2', value='dolor sit')

webhook.execute()
```

This is another example with the result as a screenshot
```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

url = "https://discordapp.com/api/webhooks/480440103915880451/RF96yIqrbp10HZRJEYRdjwn4iQYhlk1eNtsKB-FGTFMPg09fcoPqGIBwSI_kzXqzi9GY"
webhook = DiscordWebhook(url=url, username="New Webhook Username")

embed = DiscordEmbed(title='Embed Title', description='Your Embed Description', color=242424)
embed.set_author(name='Author Name', url='https://github.com/lovvskillz', icon_url='https://avatars0.githubusercontent.com/u/14542790')
embed.set_footer(text='Embed Footer Text')
embed.set_timestamp()
embed.add_embed_field(name='Field 1', value='Lorem ipsum')
embed.add_embed_field(name='Field 2', value='dolor sit')
embed.add_embed_field(name='Field 3', value='amet consetetur')
embed.add_embed_field(name='Field 4', value='sadipscing elitr')

webhook.add_embed(embed)
webhook.execute()

```

![Image](https://cdn.discordapp.com/attachments/480439896478187550/480751239806582785/unknown.png "Example Result")