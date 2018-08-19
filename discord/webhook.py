import requests
import json
import time
import datetime
import logging

logger = logging.getLogger(__name__)


class DiscordWebhook:
    def __init__(self, url, **kwargs):
        """
        Init Webhook for Discord
        @param url: discord webhook url
        @keyword content: the message contents
        @keyword username: override the default username of the webhook
        @keyword avatar_url: ooverride the default avatar of the webhook
        @keyword tts: true if this is a TTS message
        @keyword embeds: list of embedded rich content
        """
        self.url = url
        self.content = kwargs.get('content')
        self.username = kwargs.get('username')
        self.avatar_url = kwargs.get('avatar_url')
        self.tts = kwargs.get('tts', False)
        self.embeds = kwargs.get('embeds', [])

    def add_embed(self, embed):
        """
        add embedded rich content
        @param embed: embed object
        """
        self.embeds.append(embed.__dict__ if isinstance(embed, DiscordEmbed) else embed)

    def remove_embed(self, index):
        """
        remove embedded rich content from `self.embeds`
        @param index: index of embed in `self.embeds`
        """
        self.embeds.pop(index)

    @property
    def json(self):
        """
        convert webhook data to json
        @return webhook data as json:
        """
        data = dict()
        for key, value in self.__dict__.items():
            if value:
                data[key] = value
        embeds_empty = all(not d for d in data["embeds"]) if 'embeds' in data else True
        if embeds_empty and 'content' not in data:
            logger.error('webhook message is empty! set content or embed data')
        return json.dumps(data, indent=4)

    def execute(self):
        """
        execute Webhook
        @return:
        """
        headers = {'Content-Type': 'application/json'}
        result = requests.post(self.url, data=self.json, headers=headers)
        if result.status_code == 204:
            logger.debug("Webhook executed")
        else:
            logger.error(result.content.decode("utf-8"))


class DiscordEmbed:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.description = kwargs.get('description')
        self.url = kwargs.get('url')
        self.timestamp = kwargs.get('timestamp')
        self.color = kwargs.get('color')
        self.footer = kwargs.get('footer')
        self.image = kwargs.get('image')
        self.thumbnail = kwargs.get('thumbnail')
        self.video = kwargs.get('video')
        self.provider = kwargs.get('provider')
        self.author = kwargs.get('author')
        self.fields = kwargs.get('fields', [])

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def set_url(self, url):
        self.url = url

    def set_timestamp(self, timestamp=str(datetime.datetime.utcfromtimestamp(time.time()))):
        self.timestamp = timestamp

    def set_color(self, color):
        self.color = color

    def set_footer(self, **kwargs):
        self.footer = {
            'text': kwargs.get('text'),
            'icon_url': kwargs.get('icon_url'),
            'proxy_icon_url': kwargs.get('proxy_icon_url')
        }

    def set_image(self, **kwargs):
        self.image = {
            'url': kwargs.get('url'),
            'proxy_url': kwargs.get('proxy_url'),
            'height': kwargs.get('height'),
            'width': kwargs.get('width'),
        }

    def set_thumbnail(self, **kwargs):
        self.thumbnail = {
            'url': kwargs.get('url'),
            'proxy_url': kwargs.get('proxy_url'),
            'height': kwargs.get('height'),
            'width': kwargs.get('width'),
        }

    def set_video(self, **kwargs):
        self.video = {
            'url': kwargs.get('url'),
            'height': kwargs.get('height'),
            'width': kwargs.get('width'),
        }

    def set_provider(self, **kwargs):
        self.provider = {
            'name': kwargs.get('name'),
            'url': kwargs.get('url'),
        }

    def set_author(self, **kwargs):
        self.author = {
            'name': kwargs.get('name'),
            'url': kwargs.get('url'),
            'icon_url': kwargs.get('icon_url'),
            'proxy_icon_url': kwargs.get('proxy_icon_url'),
        }

    def add_embed_field(self, **kwargs):
        field = {
            'name': kwargs.get('name'),
            'value': kwargs.get('value'),
            'inline': kwargs.get('inline', True)
        }
        self.fields.append(field)

    def del_embed_field(self, index):
        self.fields.pop(index)
