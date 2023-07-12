from typing import Optional

from . import constants
from .webhook_exceptions import ComponentException


class BaseDiscordComponent:
    """
    A base class for discord components.
    """

    custom_id: str
    label: str
    type: int

    def __init__(self, **kwargs):
        self.custom_id = kwargs.get("custom_id")
        self.label = kwargs.get("label")

        if (
            type(self.type) is not int
            or self.type not in constants.DISCORD_COMPONENT_TYPES
        ):
            raise ComponentException(
                "The provided component type is invalid. A valid component type is an"
                " integer between 1 and 8."
            )
        if self.custom_id and len(self.custom_id) > 100:
            raise ComponentException("custom_id can be a maximum of 100 characters.")


class DiscordComponentButton(BaseDiscordComponent):
    """
    Represent a button that can be used in a message.
    """

    disabled: Optional[bool]
    emoji = None
    label: Optional[str]
    style: int
    type: int
    url: Optional[str]

    def __init__(
        self, style: int = constants.DISCORD_COMPONENT_BUTTON_STYLE_PRIMARY, **kwargs
    ):
        """
        :param style: button style (int 1 - 5)
        :keyword disabled: Whether the button is disabled (defaults to false)
        :keyword custom_id: developer-defined identifier for the button
        :keyword label: Text that appears on the button
        :keyword url: URL for DISCORD_COMPONENT_BUTTON_STYLE_LINK (int 5) buttons
        """
        self.type = constants.DISCORD_COMPONENT_TYPE_BUTTON
        self.style = style
        self.disabled = kwargs.get("disabled", False)
        self.custom_id = kwargs.get("custom_id")
        self.emoji = kwargs.get("emoji")
        self.label = kwargs.get("label")
        self.url = kwargs.get("url")

        if (
            type(self.style) is not int
            or self.style not in constants.DISCORD_COMPONENT_BUTTON_STYLES
        ):
            raise ComponentException(
                "The provided button style is invalid. A valid button style is an"
                " integer between 1 and 5."
            )
        if (
            constants.DISCORD_COMPONENT_BUTTON_STYLE_PRIMARY
            <= self.style
            <= constants.DISCORD_COMPONENT_BUTTON_STYLE_DANGER
            and not self.custom_id
        ):
            raise ComponentException("custom_id needs to be provided as a kwarg.")
        if self.style == constants.DISCORD_COMPONENT_BUTTON_STYLE_LINK and not self.url:
            raise ComponentException("url needs to be provided as a kwarg.")
        if self.label and len(self.label) > 80:
            raise ComponentException(
                "The label can be a maximum of 80 characters long."
            )

        super().__init__(**kwargs)
