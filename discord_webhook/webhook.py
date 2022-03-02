import logging
import json
import time
import datetime
import requests
from discord_webhook.webhook_exceptions import *

logger = logging.getLogger(__name__)


class DiscordWebhook:
    """
    Webhook for Discord
    """

    def __init__(self, url=None, content=None, username=None, avatar_url=None, **kwargs):
        """
        Init Webhook for Discord
        ---------
        :param ``url``: your discord webhook url (type: str, list)\n
        :keyword ``content:`` the message contents (type: str)\n
        :keyword ``username:`` override the default username of the webhook\n
        :keyword ``avatar_url:`` override the default avatar of the webhook\n
        :keyword ``tts:`` true if this is a TTS message\n
        :keyword ``file``: to apply file(s) with message 
        (For example: file=f.read() (here, f = variable that contain attachement path as "rb" mode))\n
        :keyword ``filename:`` apply custom file name on attached file content(s)\n
        :keyword ``embeds:`` list of embedded rich content\n
        :keyword ``allowed_mentions:`` allowed mentions for the message\n
        :keyword ``proxies:`` dict of proxies\n
        :keyword ``timeout:`` (optional) amount of seconds to wait for a response from Discord
        """
        self.url = url
        self.content = content
        self.username = username
        self.avatar_url = avatar_url
        self.tts = kwargs.get("tts", False)
        self.files = kwargs.get("files", dict())
        self.embeds = kwargs.get("embeds", [])
        self.proxies = kwargs.get("proxies")
        self.allowed_mentions = kwargs.get("allowed_mentions")
        self.timeout = kwargs.get("timeout")
        self.rate_limit_retry = kwargs.get("rate_limit_retry")

    def add_file(self, file, filename):
        """
        adds a file to the webhook
        :param file: file content
        :param filename: filename
        :return:
        """
        self.files["_{}".format(filename)] = (filename, file)

    def add_embed(self, embed):
        """
        adds an embedded rich content
        :param embed: embed object or dict
        """
        self.embeds.append(embed.__dict__ if isinstance(embed, DiscordEmbed) else embed)

    def remove_embed(self, index):
        """
        removes embedded rich content from `self.embeds`
        :param index: index of embed in `self.embeds`
        """
        self.embeds.pop(index)

    def remove_file(self, filename):
        """
        removes file from `self.files` using specified `filename` if it exists
        :param filename: filename
        """
        filename = "_{}".format(filename)
        if filename in self.files:
            del self.files[filename]

    def get_embeds(self):
        """
        gets all self.embeds as list
        :return: self.embeds
        """
        return self.embeds

    def set_proxies(self, proxies):
        """
        sets proxies
        :param proxies: dict of proxies
        :type proxies: dict
        """
        self.proxies = proxies

    def set_content(self, content):
        """
        sets content
        :param content: content string
        :type content: string
        """
        self.content = content

    @property
    def json(self):
        """
        convert webhook data to json serializable object
        :return webhook data as json serializable object:
        """
        embeds = self.embeds
        self.embeds = []
        # convert DiscordEmbed to dict
        for embed in embeds:
            self.add_embed(embed)
        data = {
            key: value
            for key, value in self.__dict__.items()
            if value and key not in {"url", "files", "filename"}
        }
        embeds_empty = not any(data["embeds"]) if "embeds" in data else True
        if embeds_empty and "content" not in data and bool(self.files) is False:
            logger.error("webhook message is empty! set content or embed data")
        return data

    def remove_embeds(self):
        """
        Sets `self.embeds` to empty `list`.
        """
        self.embeds = []

    def remove_files(self):
        """
        Sets `self.files` to empty `dict`.
        """
        self.files = {}

    def api_post_request(self, url):
        if bool(self.files) is False:
            response = requests.post(url, json=self.json, proxies=self.proxies,
                                     params={'wait': True},
                                     timeout=self.timeout)
        else:
            self.files["payload_json"] = (None, json.dumps(self.json))
            response = requests.post(url, files=self.files,
                                     proxies=self.proxies,
                                     timeout=self.timeout)

        return response

    def execute(self, remove_embeds=False, remove_files=False):
        """
        executes the Webhook
        :param remove_embeds: if set to True, calls `self.remove_embeds()` to empty `self.embeds` after webhook is executed
        :param remove_files: if set to True, calls `self.remove_files()` to empty `self.files` after webhook is executed
        :return: Webhook response
        """
        webhook_urls = self.url if isinstance(self.url, list) else [self.url]
        urls_len = len(webhook_urls)
        responses = []
        for i, url in enumerate(webhook_urls):
            response = self.api_post_request(url)
            if response.status_code in [200, 204]:
                logger.debug(
                    "[{index}/{length}] Webhook executed".format(
                        index=i + 1, length=urls_len
                    )
                )
            elif response.status_code == 429 and self.rate_limit_retry:
                while response.status_code == 429:
                    errors = json.loads(
                        response.content.decode('utf-8'))
                    wh_sleep = (int(errors['retry_after']) / 1000) + 0.15
                    time.sleep(wh_sleep)
                    logger.error(
                        "Webhook rate limited: sleeping for {wh_sleep} "
                        "seconds...".format(
                            wh_sleep=wh_sleep
                        )
                    )
                    response = self.api_post_request(url)
                    if response.status_code in [200, 204]:
                        logger.debug(
                            "[{index}/{length}] Webhook executed".format(
                                index=i + 1, length=urls_len
                            )
                        )
                        break
            else:
                logger.error(
                    "[{index}/{length}] Webhook status code {status_code}: {content}".format(
                        index=i + 1,
                        length=urls_len,
                        status_code=response.status_code,
                        content=response.content.decode("utf-8"),
                    )
                )
            responses.append(response)
        if remove_embeds:
            self.remove_embeds()
        if remove_files:
            self.remove_files()
        return responses[0] if len(responses) == 1 else responses

    def edit(self, sent_webhook, **custom_data):
        """
        edits the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :param custom_data: optional fields that will be added or override existing fields. e.g. author, attachments
        :return: Another webhook response
        """
        sent_webhook = sent_webhook if isinstance(sent_webhook, list) else [sent_webhook]
        webhook_len = len(sent_webhook)
        responses = []
        for i, webhook in enumerate(sent_webhook):
            webhook_response_content = json.loads(webhook.content.decode('utf-8'))
            webhook_message_id = webhook_response_content['id']
            url = webhook.url.split('?')[0]  # removes any query params
            if '/messages/' not in url:
                url = f'{url}/messages/{webhook_message_id}'
            json_data = self.json
            for key, value in custom_data.items():  # override or add fields that will be sent in the webhook edit request
                json_data[key] = value
            if bool(self.files) is False:
                patch_kwargs = {'json': json_data, 'proxies': self.proxies, 'params': {'wait': True}, 'timeout': self.timeout}
            else:
                self.files["payload_json"] = (None, json.dumps(json_data))
                patch_kwargs = {'files': self.files, 'proxies': self.proxies, 'timeout': self.timeout}
            response = requests.patch(url, **patch_kwargs)
            if response.status_code in [200, 204]:
                logger.debug(
                    "[{index}/{length}] Webhook edited with message id {message_id}".format(
                        index=i + 1,
                        length=webhook_len,
                        message_id=webhook_message_id
                    )
                )
            elif response.status_code == 429 and self.rate_limit_retry:
                while response.status_code == 429:
                    errors = json.loads(response.content.decode('utf-8'))
                    wh_sleep = (int(errors['retry_after']) / 1000) + 0.15
                    time.sleep(wh_sleep)
                    logger.error(
                        "Webhook rate limited for message with id {message_id}: sleeping for {wh_sleep} "
                        "seconds...".format(
                            wh_sleep=wh_sleep,
                            message_id=errors['id']
                        )
                    )
                    response = requests.patch(url, **patch_kwargs)
                    if response.status_code in [200, 204]:
                        logger.debug(
                            "[{index}/{length}] Webhook edited with message id {message_id}".format(
                                index=i + 1,
                                length=webhook_len,
                                message_id=webhook_message_id
                            )
                        )
                        break
            else:
                logger.error(
                    "[{index}/{length}] Webhook status code {status_code}: {content}".format(
                        index=i + 1,
                        length=webhook_len,
                        status_code=response.status_code,
                        content=response.content.decode("utf-8"),
                    )
                )
            responses.append(response)
        return responses[0] if len(responses) == 1 else responses

    def delete(self, sent_webhook):
        """
        deletes the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :return: Response
        """
        sent_webhook = sent_webhook if isinstance(sent_webhook, list) else [sent_webhook]
        webhook_len = len(sent_webhook)
        responses = []
        for i, webhook in enumerate(sent_webhook):
            url = webhook.url.split('?')[0]  # removes any query params
            webhook_message_id = json.loads(webhook.content.decode('utf-8'))['id']
            if '/messages/' not in url:
                url = f'{url}/messages/{webhook_message_id}'
            response = requests.delete(url, proxies=self.proxies,
                                       timeout=self.timeout)
            if response.status_code in [200, 204]:
                logger.debug(
                    "[{index}/{length}] Webhook deleted".format(
                        index=i + 1,
                        length=webhook_len,
                    )
                )
            else:
                logger.error(
                    "[{index}/{length}] Webhook status code {status_code}: {content}".format(
                        index=i + 1,
                        length=webhook_len,
                        status_code=response.status_code,
                        content=response.content.decode("utf-8"),
                    )
                )
            responses.append(response)
        return responses[0] if len(responses) == 1 else responses


class DiscordEmbed:
    """
    Discord Embed
    """

    def __init__(self, title=None, description=None, hex_color='33ccff', **kwargs):
        """
        Init Discord Embed
        -----------
        :keyword ``title:`` title of embed\n
        :keyword ``description:`` description body of embed\n
        :keyword ``url:`` add an url to make your embeded title a clickable link\n
        :keyword ``timestamp:`` timestamp of embed content\n
        :keyword ``color:`` color code of the embed as int\n
        :keyword ``hex_color:`` color code of the embed as a hex string\n
        :keyword ``footer:`` footer texts\n
        :keyword ``image:`` your image url here\n
        :keyword ``thumbnail:`` your thumbnail url here\n
        :keyword ``video:``  to apply video with embeded, your video source url here\n
        :keyword ``provider:`` provider information\n
        :keyword ``author:`` author information\n
        :keyword ``fields:`` fields information
        """
        self.title = title
        self.description = description
        self.url = kwargs.get("url")
        self.timestamp = kwargs.get("timestamp")
        self.color = kwargs.get("color")
        if self.color:
            self.set_color(self.color)
        self.hex_color = hex_color
        self.footer = kwargs.get("footer")
        self.image = kwargs.get("image")
        self.thumbnail = kwargs.get("thumbnail")
        self.video = kwargs.get("video")
        self.provider = kwargs.get("provider")
        self.author = kwargs.get("author")
        self.fields = kwargs.get("fields", [])

    def set_title(self, title):
        """
        set title of embed
        :param title: title of embed
        """
        self.title = title

    def set_description(self, description):
        """
        set description of embed
        :param description: description of embed
        """
        self.description = description

    def set_url(self, url):
        """
        set url of embed
        :param url: url of embed
        """
        self.url = url

    def set_timestamp(self, timestamp=None):
        """
        set timestamp of embed content
        :param timestamp: (optional) timestamp of embed content
        """
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = str(datetime.datetime.utcfromtimestamp(timestamp))

    def set_color(self, color):
        """
        set color code of the embed as decimal(int) or hex(string)
        :param color: color code of the embed as decimal(int) or hex(string)
        """
        self.color = int(color, 16) if isinstance(color, str) else color
        if self.color not in range(16777216):
            raise ColorNotInRangeException(color)

    def set_footer(self, **kwargs):
        """
        set footer information of embed
        :keyword text: footer text
        :keyword icon_url: url of footer icon (only supports http(s) and attachments)
        :keyword proxy_icon_url: a proxied url of footer icon
        """
        self.footer = {
            "text": kwargs.get("text"),
            "icon_url": kwargs.get("icon_url"),
            "proxy_icon_url": kwargs.get("proxy_icon_url"),
        }

    def set_image(self, **kwargs):
        """
        set image of embed
        :keyword url: source url of image (only supports http(s) and attachments)
        :keyword proxy_url: a proxied url of the image
        :keyword height: height of image
        :keyword width: width of image
        """
        self.image = {
            "url": kwargs.get("url"),
            "proxy_url": kwargs.get("proxy_url"),
            "height": kwargs.get("height"),
            "width": kwargs.get("width"),
        }

    def set_thumbnail(self, **kwargs):
        """
        set thumbnail of embed
        :keyword url: source url of thumbnail (only supports http(s) and attachments)
        :keyword proxy_url: a proxied thumbnail of the image
        :keyword height: height of thumbnail
        :keyword width: width of thumbnail
        """
        self.thumbnail = {
            "url": kwargs.get("url"),
            "proxy_url": kwargs.get("proxy_url"),
            "height": kwargs.get("height"),
            "width": kwargs.get("width"),
        }

    def set_video(self, **kwargs):
        """
        set video of embed
        :keyword url: source url of video
        :keyword height: height of video
        :keyword width: width of video
        """
        self.video = {
            "url": kwargs.get("url"),
            "height": kwargs.get("height"),
            "width": kwargs.get("width"),
        }

    def set_provider(self, **kwargs):
        """
        set provider of embed
        :keyword name: name of provider
        :keyword url: url of provider
        """
        self.provider = {
            "name": kwargs.get("name"),
            "url": kwargs.get("url"),
        }

    def set_author(self, **kwargs):
        """
        set author of embed
        :keyword name: name of author
        :keyword url: url of author
        :keyword icon_url: url of author icon (only supports http(s) and attachments)
        :keyword proxy_icon_url: a proxied url of author icon
        """
        self.author = {
            "name": kwargs.get("name"),
            "url": kwargs.get("url"),
            "icon_url": kwargs.get("icon_url"),
            "proxy_icon_url": kwargs.get("proxy_icon_url"),
        }

    def add_embed_field(self, **kwargs):
        """
        set field of embed
        :keyword name: name of the field
        :keyword value: value of the field
        :keyword inline: (optional) whether or not this field should display inline
        """
        self.fields.append(
            {
                "name": kwargs.get("name"),
                "value": kwargs.get("value"),
                "inline": kwargs.get("inline", True),
            }
        )

    def del_embed_field(self, index):
        """
        remove field from `self.fields`
        :param index: index of field in `self.fields`
        """
        self.fields.pop(index)

    def get_embed_fields(self):
        """
        get all `self.fields` as list
        :return: `self.fields`
        """
        return self.fields
