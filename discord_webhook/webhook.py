import datetime
import json
import logging
import time
from functools import partial
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import requests
from .webhook_exceptions import ColorNotInRangeException

logger = logging.getLogger(__name__)


class DiscordEmbed:
    """
    Discord Embed
    """

    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[str]
    color: Optional[int]
    footer: Optional[Dict[str, Optional[str]]]
    image: Optional[Dict[str, Optional[Union[str, int]]]]
    thumbnail: Optional[Union[str, Dict[str, Optional[Union[str, int]]]]]
    video: Optional[Union[str, Dict[str, Optional[Union[str, int]]]]]
    provider: Optional[Dict[str, Any]]
    author: Optional[Dict[str, Optional[str]]]
    fields: List[Dict[str, Optional[Any]]]

    def __init__(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """
        Init Discord Embed
        -----------
        :keyword ``title:`` title of embed\n
        :keyword ``description:`` description body of embed\n
        :keyword ``url:`` add an url to make your embedded title a clickable
        link\n
        :keyword ``timestamp:`` timestamp of embed content\n
        :keyword ``color:`` color code of the embed as int\n
        :keyword ``footer:`` footer texts\n
        :keyword ``image:`` your image url here\n
        :keyword ``thumbnail:`` your thumbnail url here\n
        :keyword ``video:``  to apply video with embedded, your video source
        url here\n
        :keyword ``provider:`` provider information\n
        :keyword ``author:`` author information\n
        :keyword ``fields:`` fields information
        """
        self.title = title
        self.description = description
        self.url = cast(str, kwargs.get("url"))
        self.timestamp = cast(str, kwargs.get("timestamp"))
        self.footer = kwargs.get("footer")
        self.image = kwargs.get("image")
        self.thumbnail = kwargs.get("thumbnail")
        self.video = kwargs.get("video")
        self.provider = kwargs.get("provider")
        self.author = kwargs.get("author")
        self.fields = kwargs.get("fields", [])
        self.set_color(kwargs.get("color"))

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

    def set_timestamp(self, timestamp: Optional[float] = None) -> None:
        """
        set timestamp of embed content
        :param timestamp: (optional) timestamp of embed content
        """
        if timestamp is None:
            timestamp = time.time()
        self.timestamp = str(datetime.datetime.utcfromtimestamp(timestamp))

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

    def add_embed_field(self, name: str, value: str,
                        inline: bool = True) -> None:
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

    def del_embed_field(self, index: int) -> None:
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

    url: Optional[Union[str, List[str]]]
    content: Optional[Union[str, bytes]]
    username: Optional[str]
    avatar_url: Optional[str]
    tts: bool
    files: Dict[str, Tuple[Optional[str], Union[bytes, str]]]
    embeds: List[Dict[str, Any]]
    proxies: Optional[Dict[str, str]]
    allowed_mentions: List[str]
    timeout: Optional[float]
    rate_limit_retry: bool = False

    def __init__(
            self,
            url: Optional[Union[str, List[str]]] = None,
            *,
            content: Optional[str] = None,
            username: Optional[str] = None,
            avatar_url: Optional[str] = None,
            tts: bool = False,
            files: Optional[
                Dict[str, Tuple[Optional[str], Union[bytes, str]]]] = None,
            embeds: Optional[List[Dict[str, Any]]] = None,
            proxies: Optional[Dict[str, str]] = None,
            timeout: Optional[float] = None,
            rate_limit_retry: bool = False,
            allowed_mentions: Optional[List[str]] = None,
    ) -> None:
        """
        Init Webhook for Discord
        ---------
        :param ``url``: your discord webhook url (type: str, list)\n
        :keyword ``content:`` the message contents (type: str)\n
        :keyword ``username:`` override the default username of the webhook\n
        :keyword ``avatar_url:`` override the default avatar of the webhook\n
        :keyword ``tts:`` true if this is a TTS message\n
        :keyword ``file``: to apply file(s) with message
        (For example: file=f.read() (here, f = variable that contain
        attachement path as "rb" mode))\n
        :keyword ``filename:`` apply custom file name on attached file
        content(s)\n
        :keyword ``embeds:`` list of embedded rich content\n
        :keyword ``allowed_mentions:`` allowed mentions for the message\n
        :keyword ``proxies:`` dict of proxies\n
        :keyword ``timeout:`` (optional) amount of seconds to wait for a
        response from Discord
        """
        if embeds is None:
            embeds = []
        if files is None:
            files = {}
        if allowed_mentions is None:
            allowed_mentions = []
        self.url = url
        self.content = content
        self.username = username
        self.avatar_url = avatar_url
        self.tts = tts
        self.files = files
        self.embeds = embeds
        self.proxies = proxies
        self.allowed_mentions = allowed_mentions
        self.timeout = timeout
        self.rate_limit_retry = rate_limit_retry

    def add_file(self, file: bytes, filename: str) -> None:
        """
        adds a file to the webhook
        :param file: file content
        :param filename: filename
        :return:
        """
        self.files[f"_{filename}"] = (filename, file)

    def add_embed(self, embed: Union[DiscordEmbed, Dict[str, Any]]) -> None:
        """
        adds an embedded rich content
        :param embed: embed object or dict
        """
        self.embeds.append(
            embed.__dict__ if isinstance(embed, DiscordEmbed) else embed)

    def remove_embed(self, index: int) -> None:
        """
        removes embedded rich content from `self.embeds`
        :param index: index of embed in `self.embeds`
        """
        self.embeds.pop(index)

    def remove_file(self, filename: str) -> None:
        """
        removes file from `self.files` using specified `filename` if it exists
        :param filename: filename
        """
        filename = f"_{filename}"
        if filename in self.files:
            del self.files[filename]

    def get_embeds(self) -> List[Dict[str, Any]]:
        """
        gets all self.embeds as list
        :return: self.embeds
        """
        return self.embeds

    def set_proxies(self, proxies: Dict[str, str]) -> None:
        """
        sets proxies
        :param proxies: dict of proxies
        :type proxies: dict
        """
        self.proxies = proxies

    def set_content(self, content: str) -> None:
        """
        sets content
        :param content: content string
        :type content: string
        """
        self.content = content

    @property
    def json(self) -> Dict[str, Any]:
        """
        convert webhook data to json
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
            if value and key not in {"url", "files", "filename"}
        }
        embeds_empty = not any(data["embeds"]) if "embeds" in data else True
        if embeds_empty and "content" not in data and bool(self.files) is False:
            logger.error("webhook message is empty! set content or embed data")
        return data

    def remove_embeds(self) -> None:
        """
        Sets `self.embeds` to empty `list`.
        """
        self.embeds = []

    def remove_files(self) -> None:
        """
        Sets `self.files` to empty `dict`.
        """
        self.files = {}

    def api_post_request(self, url: str) -> requests.Response:
        if bool(self.files) is False:
            response = requests.post(
                url,
                json=self.json,
                proxies=self.proxies,
                params={"wait": True},
                timeout=self.timeout,
            )
        else:
            self.files["payload_json"] = (None, json.dumps(self.json))
            response = requests.post(
                url,
                files=self.files,
                proxies=self.proxies,
                timeout=self.timeout,
            )
        return response

    def execute(
            self,
            remove_embeds: bool = False,
            remove_files: bool = False,
    ) -> Union[List[requests.Response], requests.Response]:
        """
        executes the Webhook
        :param remove_embeds: if set to True, calls `self.remove_embeds()`
        to empty `self.embeds` after webhook is executed
        :param remove_files: if set to True, calls `self.remove_files()`
        to empty `self.files` after webhook is executed
        :return: Webhook response
        """
        webhook_urls = self.url
        if isinstance(self.url, str):
            webhook_urls = [self.url]
        urls_len = len(webhook_urls)
        responses = []
        for i, url in enumerate(webhook_urls):
            response = self.api_post_request(url)
            if response.status_code in [200, 204]:
                logger.debug(f"[{i + 1}/{urls_len}] Webhook executed")
            elif response.status_code == 429 and self.rate_limit_retry:
                while response.status_code == 429:
                    errors = json.loads(response.content.decode("utf-8"))
                    wh_sleep = (int(errors["retry_after"]) / 1000) + 0.15
                    time.sleep(wh_sleep)
                    logger.error(
                        f"Webhook rate limited: sleeping for {wh_sleep} " 
                        "seconds..."
                    )
                    response = self.api_post_request(url)
                    if response.status_code in [200, 204]:
                        logger.debug(f"[{i + 1}/{urls_len}] Webhook executed")
                        break
            else:
                logger.error(
                    f"[{i + 1}/{urls_len}] Webhook status code "
                    f"{response.status_code}: "
                    f"{response.content.decode('utf-8')}"
                )
            responses.append(response)
        if remove_embeds:
            self.remove_embeds()
        if remove_files:
            self.remove_files()
        return responses[0] if len(responses) == 1 else responses

    def edit(
            self,
            sent_webhook: Union[List[requests.Response], requests.Response],
    ) -> Union[List[requests.Response], requests.Response]:
        """
        edits the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :return: Another webhook response
        """
        if not isinstance(sent_webhook, list):
            sent_webhook = cast(List[requests.Response], [sent_webhook])
        responses: List[requests.Response] = []
        for i, webhook in enumerate(sent_webhook):
            assert isinstance(webhook.content, bytes)
            previous_sent_message_id = json.loads(
                webhook.content.decode("utf-8")
            )["id"]
            url = (
                    webhook.url.split("?")[0] + "/messages/" + str(
                previous_sent_message_id)
            )
            # removes any query params
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
                logger.debug(f"[{i + 1}/{len(sent_webhook)}] Webhook edited")
            elif response.status_code == 429 and self.rate_limit_retry:
                while response.status_code == 429:
                    errors = json.loads(response.content.decode("utf-8"))
                    wh_sleep = (int(errors["retry_after"]) / 1000) + 0.15
                    time.sleep(wh_sleep)
                    logger.error(
                        f"Webhook rate limited: sleeping for {wh_sleep} "
                        f"seconds..."
                    )
                    response = request()
                    if response.status_code in [200, 204]:
                        logger.debug(
                            f"[{i + 1}/{len(sent_webhook)}] Webhook edited")
                        break
            else:
                logger.error(
                    f"[{i + 1}/{len(sent_webhook)}] Webhook status code "
                    f"{response.status_code}: "
                    f"{response.content.decode('utf-8')}"
                )
            responses.append(response)
        return responses[0] if len(responses) == 1 else responses

    def delete(
            self, sent_webhook: Union[List["DiscordWebhook"], "DiscordWebhook"]
    ) -> Union[List[requests.Response], requests.Response]:
        """
        deletes the webhook passed as a response
        :param sent_webhook: webhook.execute() response
        :return: Response
        """
        if not isinstance(sent_webhook, list):
            sent_webhook = cast(List[DiscordWebhook], [sent_webhook])
        responses: List[requests.Response] = []
        for i, webhook in enumerate(sent_webhook):
            assert isinstance(webhook.content, bytes)
            url = webhook.url.split("?")[0]  # removes any query params
            previous_sent_message_id = json.loads(
                webhook.content.decode("utf-8")
            )["id"]
            response = requests.delete(
                url + "/messages/" + str(previous_sent_message_id),
                proxies=self.proxies,
                timeout=self.timeout,
            )
            if response.status_code in [200, 204]:
                logger.debug(f"[{i + 1}/{len(sent_webhook)}] Webhook deleted")
            else:
                logger.error(
                    f"[{i + 1}/{len(sent_webhook)}] Webhook status code "
                    f"{response.status_code}: {response.content.decode('utf-8')}"
                )
            responses.append(response)
        return responses[0] if len(responses) == 1 else responses
