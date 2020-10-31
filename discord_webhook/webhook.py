import logging
import json
import time
import datetime
import requests


logger = logging.getLogger(__name__)


class DiscordWebhook:
    """
    Webhook for Discord
    """

    def __init__(self, url, **kwargs):
        """
        Init Webhook for Discord
        :param url: discord_webhook webhook url
        :type url: str, list
        :keyword content: the message contents
        :keyword username: override the default username of the webhook
        :keyword avatar_url: override the default avatar of the webhook
        :keyword tts: true if this is a TTS message
        :keyword file: file contents
        :keyword filename: file name
        :keyword embeds: list of embedded rich content
        :keyword allowed_mentions: allowed mentions for the message
        :keyword proxies: dict of proxies
        """
        self.url = url
        self.content = kwargs.get("content")
        self.username = kwargs.get("username")
        self.avatar_url = kwargs.get("avatar_url")
        self.tts = kwargs.get("tts", False)
        self.files = kwargs.get("files", dict())
        self.embeds = kwargs.get("embeds", [])
        self.proxies = kwargs.get("proxies")
        self.allowed_mentions = kwargs.get("allowed_mentions")

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
        convert webhook data to json
        :return webhook data as json:
        """
        data = dict()
        embeds = self.embeds
        self.embeds = list()
        # convert DiscordEmbed to dict
        for embed in embeds:
            self.add_embed(embed)
        for key, value in self.__dict__.items():
            if value and key not in ["url", "files", "filename"]:
                data[key] = value
        embeds_empty = (
            all(not embed for embed in data["embeds"]) if "embeds" in data else True
        )
        if embeds_empty and "content" not in data and bool(self.files) is False:
            logger.error("webhook message is empty! set content or embed data")
        return data

    def execute(self):
        """
        executes the Webhook
        :return: Webhook response
        """
        webhook_urls = self.url if isinstance(self.url, list) else [self.url]
        urls_len = len(webhook_urls)
        responses = []
        for i, url in enumerate(webhook_urls):
            if bool(self.files) is False:
                response = requests.post(url, json=self.json, proxies=self.proxies, params={'wait':True})
            else:
                self.files["payload_json"] = (None, json.dumps(self.json))
                response = requests.post(url, files=self.files, proxies=self.proxies)
            if response.status_code in [200, 204]:
                logger.debug(
                    "[{index}/{length}] Webhook executed".format(
                        index=i+1, length=urls_len
                    )
                )
            else:
                logger.error(
                    "[{index}/{length}] Webhook status code {status_code}: {content}".format(
                        index=i+1,
                        length=urls_len,
                        status_code=response.status_code,
                        content=response.content.decode("utf-8"),
                    )
                )
            responses.append(response)
        return responses

    def edit(self, sent_webhook):
        """
        edits the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :return: Another webhook response
        """
        webhook_len = len(sent_webhook)
        responses = []
        for i, webhook in enumerate(sent_webhook):
            url = webhook.url.split('?')[0]  # removes any query params
            previous_sent_message_id = json.loads(webhook.content.decode('utf-8'))['id']
            if bool(self.files) is False:
                response = requests.patch(url+'/messages/'+str(previous_sent_message_id), json=self.json, proxies=self.proxies, params={'wait': True})
            else:
                self.files["payload_json"] = (None, json.dumps(self.json))
                response = requests.patch(url+'/messages/'+str(previous_sent_message_id), files=self.files, proxies=self.proxies)
            if response.status_code in [200, 204]:
                logger.debug(
                    "[{index}/{length}] Webhook edited".format(
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
        return responses

    def delete(self, sent_webhook):
        """
        deletes the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :return: Response
        """
        webhook_len = len(sent_webhook)
        responses = []
        for i, webhook in enumerate(sent_webhook):
            url = webhook.url.split('?')[0]  # removes any query params
            previous_sent_message_id = json.loads(webhook.content.decode('utf-8'))['id']
            response = requests.delete(url+'/messages/'+str(previous_sent_message_id), proxies=self.proxies)
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
        return responses


class DiscordEmbed:
    """
    Discord Embed
    """

    def __init__(self, **kwargs):
        """
        Init Discord Embed
        :keyword title: title of embed
        :keyword description: description of embed
        :keyword url: url of embed
        :keyword timestamp: timestamp of embed content
        :keyword color: color code of the embed as int
        :keyword footer: footer information
        :keyword image: image information
        :keyword thumbnail: thumbnail information
        :keyword video: video information
        :keyword provider: provider information
        :keyword author: author information
        :keyword fields: fields information
        """
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.url = kwargs.get("url")
        self.timestamp = kwargs.get("timestamp")
        self.color = kwargs.get("color")
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
        set color code of the embed as int
        :param color: color code of the embed as int
        """
        self.color = color

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
