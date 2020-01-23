# python-discord-webhook

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/lovvskillz/python-discord-webhook/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/discord-webhook.svg)](https://badge.fury.io/py/discord-webhook)
[![Downloads](https://pepy.tech/badge/discord-webhook)](https://pepy.tech/project/discord-webhook)

execute discord webhooks

## Install

install via pip: `pip install discord-webhook`

## Examples

* [Basic Webhook](#basic-webhook)
* [Multiple Webhook Urls](#multiple-webhook-urls)
* [Embedded Content](#webhook-with-embedded-content)
* [Send Files](#send-files)
* [Use Proxies](#use-proxies)

### basic webhook
```python
from discord_webhook import DiscordWebhook

webhook = DiscordWebhook(url='your webhook url', content='Webhook Message')
response = webhook.execute()
```

![Image](img/basic_webhook.png "Basic Example Result")

### multiple webhook urls
```python
from discord_webhook import DiscordWebhook

webhook_urls = ['webhook url 1', 'webhook url 2']
webhook = DiscordWebhook(url=webhook_urls, content='Webhook Message')
response = webhook.execute()
```

![Image](img/multiple_urls.png "Multiple Urls Result")


### webhook with embedded content
```python
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url')

# create embed object for webhook
embed = DiscordEmbed(title='Your Title', description='Lorem ipsum dolor sit', color=242424)

# add embed object to webhook
webhook.add_embed(embed)

response = webhook.execute()
```

![Image](img/simple_embed.png "Basic Embed Example Result")

```python
from discord_webhook import DiscordWebhook, DiscordEmbed

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

response = webhook.execute()
```
![Image](img/extended_embed.png "Basic Embed Example Result")

This is another example with embedded content
```python
from discord_webhook import DiscordWebhook, DiscordEmbed

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
response = webhook.execute()
```

![Image](img/extended_embed2.png "Example Embed Result")

### send files

```python
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url', username="Webhook with files")

# send two images
with open("path/to/first/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example.jpg')
with open("path/to/second/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example2.jpg')

response = webhook.execute()
```
![Image](img/webhook_files.png "Example Files Result")

You can use uploaded attachments in embeds:
```python
from discord_webhook import DiscordWebhook, DiscordEmbed

webhook = DiscordWebhook(url='your webhook url')

with open("path/to/image.jpg", "rb") as f:
    webhook.add_file(file=f.read(), filename='example.jpg')

embed = DiscordEmbed(title='Embed Title', description='Your Embed Description', color=242424)
embed.set_thumbnail(url='attachment://example.jpg')

webhook.add_embed(embed)
response = webhook.execute()
```

### use proxies

```python
from discord_webhook import DiscordWebhook

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
webhook = DiscordWebhook(url='your webhook url', content='Webhook Message', proxies=proxies)
response = webhook.execute()
```
or
```python
from discord_webhook import DiscordWebhook

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
webhook = DiscordWebhook(url='your webhook url', content='Webhook Message')
webhook.set_proxies(proxies)
response = webhook.execute()
```

### use cli

```
usage: discord_webhook [-h] -u URL [URL ...] -c CONTENT [--username USERNAME]
                       [--avatar_url AVATAR_URL]

Trigger discord webhook(s).

optional arguments:
  -h, --help            show this help message and exit
  -u URL [URL ...], --url URL [URL ...]
                        Webhook(s) url(s)
  -c CONTENT, --content CONTENT
                        Message content
  --username USERNAME
  --avatar_url AVATAR_URL
```
