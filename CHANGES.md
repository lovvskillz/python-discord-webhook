# python-discord-webhook Changes

## 2020-01-23 0.7.0

- add an entry point for a minimal cli

## 2019-12-13 0.6.0

- send webhook to multiple urls if urls are provided as `list`

## 2019-11-21 0.5.0

- `.execute()` now returns the webhook response

## 2018-11-29 0.4.1

### Fixes
- convert `DiscordEmbed` to `dict` because `DiscordEmbed` is not JSON serializable

## 2018-11-02 0.4.0

- import from package instead of sumbodule

### Features
- send files and message/embed simultaneously

## 2018-11-02 0.3.0

### Features
If you have to use a proxy, you can now add your proxies with the `proxies` parameter
```python
from discord_webhook.webhook import DiscordWebhook

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
DiscordWebhook(url="webhook URL", proxies=proxies)
```
or with the `set_proxies()` function
```python
from discord_webhook.webhook import DiscordWebhook

proxies = {
  'http': 'http://10.10.1.10:3128',
  'https': 'http://10.10.1.10:1080',
}
webhook = DiscordWebhook(url="webhook URL")
webhook.set_proxies(proxies)
```

## 2018-08-20 0.2.0

### Features
- send webhook with files

## 2018-08-19 0.1.0

### Features
- send basic webhook
- send webhook with embedded content

