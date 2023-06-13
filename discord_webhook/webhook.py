import json
import logging
import time
from datetime import datetime
from functools import partial
from http.client import HTTPException
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import requests

from .webhook_exceptions import ColorNotInRangeException

logger = logging.getLogger(__name__)


class DiscordEmbed:
    """
    Discord Embed
    """

    author: Optional[Dict[str, Optional[str]]]
    color: Optional[int]
    description: Optional[str]
    fields: List[Dict[str, Optional[Any]]]
    footer: Optional[Dict[str, Optional[str]]]
    image: Optional[Dict[str, Optional[Union[str, int]]]]
    provider: Optional[Dict[str, Any]]
    thumbnail: Optional[Union[str, Dict[str, Optional[Union[str, int]]]]]
    timestamp: Optional[str]
    title: Optional[str]
    url: Optional[str]
    video: Optional[Union[str, Dict[str, Optional[Union[str, int]]]]]

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """
        Init Discord Embed
        -----------
        :keyword ``author:`` author information\n
        :keyword ``color:`` color code of the embed as int\n
        :keyword ``description:`` description body of embed\n
        :keyword ``fields:`` fields information
        :keyword ``footer:`` footer texts\n
        :keyword ``image:`` your image url here\n
        :keyword ``provider:`` provider information\n
        :keyword ``thumbnail:`` your thumbnail url here\n
        :keyword ``timestamp:`` timestamp of embed content\n
        :keyword ``title:`` title of embed\n
        :keyword ``url:`` add an url to make your embedded title a clickable
        link\n
        :keyword ``video:``  to apply video with embedded, your video source
        url here\n
        """
        self.title = title
        self.description = description
        self.url = cast(str, kwargs.get("url"))
        self.footer = kwargs.get("footer")
        self.image = kwargs.get("image")
        self.thumbnail = kwargs.get("thumbnail")
        self.video = kwargs.get("video")
        self.provider = kwargs.get("provider")
        self.author = kwargs.get("author")
        self.fields = kwargs.get("fields", [])
        self.set_color(kwargs.get("color"))
        if timestamp := kwargs.get("timestamp"):
            self.set_timestamp(timestamp)

    def set_title(self, title: str) -> None:
        """
        set title of embed
        :param title: title of embed
        """
        self.title = title

    def set_description(self, description: str) -> None:
        """
        set description of embed
        :param description: description of embed
        """
        self.description = description

    def set_url(self, url: str) -> None:
        """
        set url of embed
        :param url: url of embed
        """
        self.url = url

    def set_timestamp(
        self, timestamp: Optional[Union[float, int, datetime]] = None
    ) -> None:
        """
        set timestamp of embed content
        :param timestamp: (optional) timestamp of embed content
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        elif isinstance(timestamp, float) or isinstance(timestamp, int):
            timestamp = datetime.utcfromtimestamp(timestamp)

        self.timestamp = timestamp.isoformat()

    def set_color(self, color: Union[str, int]) -> None:
        """
        set color code of the embed as decimal(int) or hex(string)
        :param color: color code of the embed as decimal(int) or hex(string)
        """
        self.color = int(color, 16) if isinstance(color, str) else color
        if self.color is not None and self.color not in range(16777216):
            raise ColorNotInRangeException(color)

    def set_footer(self, **kwargs: str) -> None:
        """
        set footer information of embed
        :keyword text: footer text
        :keyword icon_url: url of footer icon (only supports http(s) and
        attachments)
        :keyword proxy_icon_url: a proxied url of footer icon
        """
        self.footer = {
            "text": kwargs.get("text"),
            "icon_url": kwargs.get("icon_url"),
            "proxy_icon_url": kwargs.get("proxy_icon_url"),
        }

    def set_image(self, url: str, **kwargs: Union[str, int]) -> None:
        """
        set image of embed
        :param url: source url of image (only supports http(s) and attachments)
        :keyword proxy_url: a proxied url of the image
        :keyword height: height of image
        :keyword width: width of image
        """
        self.image = {
            "url": url,
            "proxy_url": cast(Optional[str], kwargs.get("proxy_url")),
            "height": cast(Optional[int], kwargs.get("height")),
            "width": cast(Optional[int], kwargs.get("width")),
        }

    def set_thumbnail(self, url: str, **kwargs: Union[str, int]) -> None:
        """
        set thumbnail of embed
        :param url: source url of thumbnail (only supports http(s) and
        attachments)
        :keyword proxy_url: a proxied thumbnail of the image
        :keyword height: height of thumbnail
        :keyword width: width of thumbnail
        """
        self.thumbnail = {
            "url": url,
            "proxy_url": cast(Optional[str], kwargs.get("proxy_url")),
            "height": cast(Optional[int], kwargs.get("height")),
            "width": cast(Optional[str], kwargs.get("width")),
        }

    def set_video(self, **kwargs: Union[str, int]) -> None:
        """
        set video of embed
        :keyword url: source url of video
        :keyword height: height of video
        :keyword width: width of video
        """
        self.video = {
            "url": cast(Optional[str], kwargs.get("url")),
            "height": cast(Optional[int], kwargs.get("height")),
            "width": cast(Optional[int], kwargs.get("width")),
        }

    def set_provider(self, **kwargs: str) -> None:
        """
        set provider of embed
        :keyword name: name of provider
        :keyword url: url of provider
        """
        self.provider = {
            "name": kwargs.get("name"),
            "url": kwargs.get("url"),
        }

    def set_author(self, name: str, **kwargs: str) -> None:
        """
        set author of embed
        :param name: name of author
        :keyword url: url of author
        :keyword icon_url: url of author icon (only supports http(s) and
        attachments)
        :keyword proxy_icon_url: a proxied url of author icon
        """
        self.author = {
            "name": name,
            "url": kwargs.get("url"),
            "icon_url": kwargs.get("icon_url"),
            "proxy_icon_url": kwargs.get("proxy_icon_url"),
        }

    def add_embed_field(self, name: str, value: str, inline: bool = True) -> None:
        """
        set field of embed
        :param name: name of the field
        :param value: value of the field
        :param inline: (optional) whether this field should display inline
        """
        self.fields.append(
            {
                "name": name,
                "value": value,
                "inline": inline,
            }
        )

    def delete_embed_field(self, index: int) -> None:
        """
        remove field from `self.fields`
        :param index: index of field in `self.fields`
        """
        self.fields.pop(index)

    def get_embed_fields(self) -> List[Dict[str, Optional[Any]]]:
        """
        get all `self.fields` as list
        :return: `self.fields`
        """
        return self.fields


class DiscordWebhook:
    """
    Webhook for Discord
    """

    allowed_mentions: List[str]
    attachments: Optional[List[Dict[str, Any]]]
    avatar_url: Optional[str]
    components: Optional[list]
    content: Optional[Union[str, bytes]]
    embeds: List[Dict[str, Any]]
    files: Dict[str, Tuple[Optional[str], Union[bytes, str]]]
    id: Optional[str]
    proxies: Optional[Dict[str, str]]
    rate_limit_retry: bool = False
    timeout: Optional[float]
    tts: bool
    url: str
    username: Optional[str]

    def __init__(
        self,
        url: str,
        id: Optional[str] = None,
        content: Optional[str] = None,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        tts: bool = False,
        attachments: Optional[List[Dict[str, Any]]] = None,
        files: Optional[Dict[str, Tuple[Optional[str], Union[bytes, str]]]] = None,
        embeds: Optional[List[Dict[str, Any]]] = None,
        proxies: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
        rate_limit_retry: bool = False,
        allowed_mentions: Optional[List[str]] = None,
    ) -> None:
        """
        Init Webhook for Discord.
        ---------
        :param ``url``: your discord webhook url (type: str)\n
        :keyword ``id:`` webhook id (type: str)\n
        :keyword ``content:`` the message contents (type: str)\n
        :keyword ``username:`` override the default username of the webhook\n
        :keyword ``avatar_url:`` override the default avatar of the webhook\n
        :keyword ``tts:`` true if this is a TTS message\n
        :keyword ``attachments`` optional dict of attachments.
        Will be set after executing a webhook\n
        :keyword ``files``: to apply file(s) with message
        (For example: file=f.read() (here, f = variable that contains the
        attachment path as "rb" mode))\n
        :keyword ``embeds:`` list of embedded rich content\n
        :keyword ``allowed_mentions:`` allowed mentions for the message\n
        :keyword ``proxies:`` dict of proxies\n
        :keyword ``timeout:`` (optional) amount of seconds to wait for a
        response from Discord
        """
        if allowed_mentions is None:
            allowed_mentions = []
        if attachments is None:
            attachments = []
        if embeds is None:
            embeds = []
        if files is None:
            files = {}

        self.allowed_mentions = allowed_mentions
        self.attachments = attachments
        self.avatar_url = avatar_url
        self.content = content
        self.embeds = embeds
        self.files = files
        self.id = id
        self.proxies = proxies
        self.rate_limit_retry = rate_limit_retry
        self.timeout = timeout
        self.tts = tts
        self.url = url
        self.username = username

    def add_embed(self, embed: Union[DiscordEmbed, Dict[str, Any]]) -> None:
        """
        Add an embedded rich content.
        :param embed: embed object or dict
        """
        self.embeds.append(embed.__dict__ if isinstance(embed, DiscordEmbed) else embed)

    def get_embeds(self) -> List[Dict[str, Any]]:
        """
        Get all embeds as a list.
        :return: self.embeds
        """
        return self.embeds

    def remove_embed(self, index: int) -> None:
        """
        Remove embedded rich content from `self.embeds`.
        :param index: index of embed in `self.embeds`
        """
        self.embeds.pop(index)

    def remove_embeds(self) -> None:
        """
        Remove all embeds.
        :return: None
        """
        self.embeds = []

    def add_file(self, file: bytes, filename: str) -> None:
        """
        Add a file to the webhook.
        :param file: file content
        :param filename: filename
        :return:
        """
        self.files[f"_{filename}"] = (filename, file)

    def remove_file(self, filename: str) -> None:
        """
        Remove file by given `filename` if it exists.
        :param filename: filename
        """
        self.files.pop(f"_{filename}", None)
        if self.attachments:
            index = next(
                (
                    i
                    for i, item in enumerate(self.attachments)
                    if item.get("filename") == filename
                ),
                None,
            )
            if index is not None:
                self.attachments.pop(index)

    def remove_files(self, clear_attachments: bool = True) -> None:
        """
        Remove all files and optionally clear the attachments.
        :keyword clear_attachments: Clear the attachments.
        :type clear_attachments: bool
        :return: None
        """
        self.files = {}
        if clear_attachments:
            self.clear_attachments()

    def clear_attachments(self) -> None:
        """
        Remove all attachments.
        :return: None
        """
        self.attachments = []

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        Set proxies.
        :param proxies: dict of proxies
        :type proxies: dict
        """
        self.proxies = proxies

    def set_content(self, content: str) -> None:
        """
        Set content.
        :param content: content string
        :type content: string
        """
        self.content = content

    @property
    def json(self) -> Dict[str, Any]:
        """
        Convert webhook data to json.
        :return webhook data as json:
        """
        embeds = self.embeds
        self.embeds = []
        # convert DiscordEmbed to dict
        for embed in embeds:
            self.add_embed(embed)
        data = {
            key: value
            for key, value in self.__dict__.items()
            if value and key not in ["url", "files"] or key in ["embeds", "attachments"]
        }
        embeds_empty = not any(data["embeds"]) if "embeds" in data else True
        if embeds_empty and "content" not in data and bool(self.files) is False:
            logger.error("webhook message is empty! set content or embed data")
        return data

    def api_post_request(self) -> requests.post:
        if bool(self.files) is False:
            return requests.post(
                self.url,
                json=self.json,
                proxies=self.proxies,
                params={"wait": True},
                timeout=self.timeout,
            )

        self.files["payload_json"] = (None, json.dumps(self.json))
        return requests.post(
            self.url,
            files=self.files,
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def handle_rate_limit(self, response, request):
        """
        Handle the rate limit.
        :param response: Response
        :param request: request function
        :return: Response
        """
        while response.status_code == 429:
            errors = json.loads(response.content.decode("utf-8"))
            if not response.headers.get("Via"):
                raise HTTPException(errors)
            wh_sleep = (int(errors["retry_after"]) / 1000) + 0.15
            logger.error(f"Webhook rate limited: sleeping for {wh_sleep} seconds...")
            time.sleep(wh_sleep)
            response = request()
            if response.status_code in [200, 204]:
                return response

    def execute(
        self,
        remove_embeds: bool = False,
    ) -> requests.Response:
        """
        Execute the Webhook.
        :param remove_embeds: if set to True, calls `self.remove_embeds()`
        to empty `self.embeds` after webhook is executed
        :return: Webhook response
        """
        response = self.api_post_request()
        if response.status_code in [200, 204]:
            logger.debug("Webhook executed")
        elif response.status_code == 429 and self.rate_limit_retry:
            response = self.handle_rate_limit(response, self.api_post_request)
            logger.debug("Webhook executed")
        else:
            logger.error(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status_code,
                    content=response.content.decode("utf-8"),
                )
            )
        if remove_embeds:
            self.remove_embeds()
        self.remove_files(clear_attachments=False)
        response_content = json.loads(response.content.decode("utf-8"))
        if webhook_id := response_content.get("id"):
            self.id = webhook_id
        if attachments := response_content.get("attachments"):
            self.attachments = attachments
        return response

    def edit(self) -> requests.Response:
        """
        Edit the given webhook.
        :return: webhook response
        """
        assert isinstance(
            self.id, str
        ), "Webhook ID needs to be set in order to edit the webhook."
        assert isinstance(
            self.url, str
        ), "Webhook URL needs to be set in order to edit the webhook."
        url = f"{self.url}/messages/{self.id}"
        if bool(self.files) is False:
            request = partial(
                requests.patch,
                url,
                json=self.json,
                proxies=self.proxies,
                params={"wait": True},
                timeout=self.timeout,
            )
        else:
            self.files["payload_json"] = (None, json.dumps(self.json))
            request = partial(
                requests.patch,
                url,
                files=self.files,
                proxies=self.proxies,
                timeout=self.timeout,
            )
        response = request()
        if response.status_code in [200, 204]:
            logger.debug("Webhook with id {id} edited".format(id=self.id))
        elif response.status_code == 429 and self.rate_limit_retry:
            response = self.handle_rate_limit(response, request)
            logger.debug("Webhook edited")
        else:
            logger.error(
                "Webhook status code {status_code}: {content}".format(
                    status_code=response.status_code,
                    content=response.content.decode("utf-8"),
                )
            )
        return response

    def delete(self) -> requests.Response:
        """
        Delete the given webhook.
        :return: webhook response
        """
        assert isinstance(
            self.id, str
        ), "Webhook ID needs to be set in order to delete the webhook."
        assert isinstance(
            self.url, str
        ), "Webhook URL needs to be set in order to delete the webhook."
        url = f"{self.url}/messages/{self.id}"
        request = partial(
            requests.delete, url, proxies=self.proxies, timeout=self.timeout
        )
        response = request()
        if response.status_code in [200, 204]:
            logger.debug("Webhook deleted")
        elif response.status_code == 429 and self.rate_limit_retry:
            response = self.handle_rate_limit(response, request)
            logger.debug("Webhook edited")
        return response

    @classmethod
    def create_batch(cls, urls: List[str], **kwargs) -> Tuple["DiscordWebhook", ...]:
        """
        Create multiple instances of webhook.
        :param urls: list of webhook URLs.
        :return: tuple of webhook instances
        """
        if "url" in kwargs:
            raise TypeError("'url' can't be used as a keyword argument.")
        return tuple([cls(url, **kwargs) for url in urls])
