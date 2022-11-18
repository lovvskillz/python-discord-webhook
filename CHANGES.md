# python-discord-webhook Changes

## 2022-11-18 1.0.0

### 🎉 Features
- `execute()` stores the webhook ID in the `.id` property
- `DiscordWebhook.create_batch()` creates multiple instances

### 🛠 Breaking Changes
- `DiscordWebhook` and `AsyncDiscordWebhook`
  - `url` parameter only excepts one url as `str`
  - `edit()` excepts no parameters
  - `delete()` excepts no parameters
- `DiscordEmbed`
  - rename `del_embed_field()` to `delete_embed_field()`

## 2022-08-23 0.17.0

### 🛠 Breaking Changes
- `ColourNotInRangeException` was renamed to `ColorNotInRangeException`

### 🩹 Fixes
- fix async file attachments

## 2022-05-14 0.16.3

### 🩹 Fixes
- only check if color is in range if color was set

## 2022-05-12 0.16.2

### 🩹 Fixes
- fix support for using a list of webhook URLs

## 2022-05-12 0.16.1

### 🩹 Fixes
- fix hex to int color conversion

## 2022-05-06 0.16.0

### 🎉 Features
- add async support

## 2022-03-02 0.15.0

### 🎉 Features
- enable `rate_limit_retry` in webhook `edit()` function
- add optional kwargs to `edit` function to specify fields that will be added or override existing fields in the webhook edit request. e.g. attachments 

## 2021-06-08 0.14.0

### 🎉 Features

- add optional `rate_limit_retry` to webhook.
  The webhook will automatically be sent once the rate limit has been lifted

## 2021-04-01 0.13.0

### 🎉 Features

- add `timeout` param to webhooks

## 2021-03-02 0.12.0

### 🎉 Features

- convert embed color to decimal if it's given as hex
- return webhook responses only as a list if multiple urls are given.
  Otherwise, just return the response object
- add `remove_embeds()`, `remove_files()` functions in order to clear `embeds` and `files` properties of webhook object
- add optional `remove_embeds` and `remove_files` args to `execute()` in order to automatically clear `embeds` and `files` properties
- add `remove_file()` function in order to remove a file in `files` given by filename

### 🛠 Breaking Changes

- return webhook responses only as a list if multiple urls are given.
  Otherwise, just return the response object

## 2020-10-31 0.11.0

- webhook responses are always returned as a list

### 🎉 Features

- `edit()` and `delete()` methods are now supporting multiple webhooks

### 🩹 Fixes

- fixed an issue where multiple webhook urls would throw an error after `.execute()` has been called

## 2020-10-27 0.10.0

### 🎉 Features

- add `edit()` and `delete()` methods to `DiscordWebhook` class

## 2020-08-17 0.9.0

- add `allowed_mentions` property to webhooks. see [Discord Docs](https://discord.com/developers/docs/resources/channel#allowed-mentions-object)

## 2020-05-14 0.8.0

- add `set_content()` function

## 2020-03-12 0.7.1

### 🩹 Fixes

- fixed an issue where the default timestamp was not updated

## 2020-01-24 0.7.0

### 🎉 Features

- add an entry point for a minimal cli

## 2019-12-13 0.6.0

### 🎉 Features

- send webhook to multiple urls if urls are provided as `list`

## 2019-11-21 0.5.0

### 🎉 Features

- `.execute()` now returns the webhook response

## 2018-11-29 0.4.1

### 🩹 Fixes

- convert `DiscordEmbed` to `dict` because `DiscordEmbed` is not JSON serializable

## 2018-11-02 0.4.0

- import from package instead of submodule

### 🎉 Features

- send files and message/embed simultaneously

## 2018-11-02 0.3.0

### 🎉 Features

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

### 🎉 Features

- send webhook with files

## 2018-08-19 0.1.0

### 🎉 Features

- send basic webhook
- send webhook with embedded content
