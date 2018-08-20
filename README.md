# python-discord-webhook

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/lovvskillz/python-discord-webhook/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/discord-webhook.svg)](https://badge.fury.io/py/discord-webhook)

execute discord webhooks

## Install

install via pip: `pip install discord-webhook`

## Examples

### basic webhook
```python
from discord_webhook.webhook import DiscordWebhook

webhook = DiscordWebhook(url='your webhook url', content='Webhook Message')
webhook.execute()
```

![Image](https://cdn.discordapp.com/attachments/480439896478187550/481042601307537409/unknown.png "Basic Example Result")

### webhook with embedded content
```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# add embed object to webhook
webhook.add_embed(embed)

webhook.execute()
```

![Image](https://cdn.discordapp.com/attachments/480439896478187550/481044061428514816/unknown.png "Basic Embed Example Result")

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

# add fields to embed
embed.add_embed_field(name='Field 1', value='Lorem ipsum')
embed.add_embed_field(name='Field 2', value='dolor sit')

# add embed object to webhook
webhook.add_embed(embed)

webhook.execute()
```
![Image](https://cdn.discordapp.com/attachments/480439896478187550/480751239806582785/unknown.png "Example Embed Result")

This is another example with embedded content
```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url', username="New Webhook Username")

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

![Image](https://cdn.discordapp.com/attachments/480439896478187550/480751239806582785/unknown.png "Example Embed Result")

### send files

```python
from discord_webhook.webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url', username="Webhook with files")

# send two images
with open("path/to/first/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example.jpg')
with open("path/to/second/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example2.jpg')

webhook.execute()
```
![Image](https://cdn.discordapp.com/attachments/480439896478187550/481041687020306432/unknown.png "Example Files Result")
