from typing import Any, Dict, List, Optional, Union

from . import constants
from .utils import check_max_length, is_int, to_dict
from .webhook_exceptions import ComponentException


class DiscordComponentEmoji:
    """
    Represent a partial emoji that can be used in components.
    """

    animated: Optional[bool]
    id: Optional[str]
    name: Optional[str]

    def __init__(
        self,
        name: Optional[str] = None,
        id: Optional[str] = None,
        animated: bool = False,
    ) -> None:
        """
        :param str name: name of the emoji (unicode emoji for standard emojis)
        :param str id: id of the emoji for custom emojis
        :param bool animated: whether the emoji is animated
        """
        if not name and not id:
            raise ComponentException("Either name or id needs to be provided.")

        self.name = name
        self.id = id
        self.animated = animated

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the emoji to a dict.
        :return: emoji as dict
        """
        return {key: value for key, value in self.__dict__.items() if value is not None}


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

        if not is_int(self.type) or self.type not in constants.DISCORD_COMPONENT_TYPES:
            raise ComponentException(
                "The provided component type is invalid. A valid component type is an"
                " integer between 1 and 8."
            )
        if self.custom_id and len(self.custom_id) > 100:
            raise ComponentException("custom_id can be a maximum of 100 characters.")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the component to a dict.
        :return: component as dict
        """
        data = {"type": self.type}
        for key, value in self.__dict__.items():
            if value is None or value == []:
                continue
            data[key] = to_dict(value)
        return data


class DiscordComponentButton(BaseDiscordComponent):
    """
    Represent a button that can be used in a message.
    """

    disabled: Optional[bool]
    emoji: Optional[Union[dict, DiscordComponentEmoji]]
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
        :keyword emoji: emoji that appears on the button
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
            not is_int(self.style)
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


class DiscordSelectOption:
    """
    Represent an option of a string select menu.
    """

    default: Optional[bool]
    description: Optional[str]
    emoji: Optional[Union[dict, DiscordComponentEmoji]]
    label: str
    value: str

    def __init__(self, label: str, value: str, **kwargs) -> None:
        """
        :param str label: user-facing name of the option
        :param str value: developer-defined value of the option
        :keyword str description: additional description of the option
        :keyword emoji: emoji that appears next to the option
        :keyword bool default: whether the option is selected by default
        """
        self.label = label
        self.value = value
        self.description = kwargs.get("description")
        self.emoji = kwargs.get("emoji")
        self.default = kwargs.get("default", False)

        check_max_length(self.label, 100, "label", ComponentException)
        check_max_length(self.value, 100, "value", ComponentException)
        check_max_length(self.description, 100, "description", ComponentException)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the option to a dict.
        :return: option as dict
        """
        return {
            key: to_dict(value)
            for key, value in self.__dict__.items()
            if value is not None
        }


class BaseDiscordComponentSelect(BaseDiscordComponent):
    """
    A base class for the different select menus.
    """

    disabled: Optional[bool]
    max_values: Optional[int]
    min_values: Optional[int]
    placeholder: Optional[str]

    def __init__(self, custom_id: str, **kwargs) -> None:
        """
        :param str custom_id: developer-defined identifier for the select menu
        :keyword bool disabled: whether the select menu is disabled (defaults to false)
        :keyword int max_values: maximum amount of options that can be chosen (1 - 25)
        :keyword int min_values: minimum amount of options that have to be chosen (0 - 25)
        :keyword str placeholder: text that is shown if nothing is selected
        """
        kwargs["custom_id"] = custom_id
        self.disabled = kwargs.get("disabled", False)
        self.max_values = kwargs.get("max_values", 1)
        self.min_values = kwargs.get("min_values", 1)
        self.placeholder = kwargs.get("placeholder")

        if not custom_id:
            raise ComponentException("custom_id needs to be provided.")
        check_max_length(self.placeholder, 150, "placeholder", ComponentException)
        for name, value, minimum in [
            ("min_values", self.min_values, 0),
            ("max_values", self.max_values, 1),
        ]:
            if not is_int(value) or not minimum <= value <= 25:
                raise ComponentException(
                    f"{name} needs to be an integer between {minimum} and 25."
                )

        super().__init__(**kwargs)


class DiscordComponentStringSelect(BaseDiscordComponentSelect):
    """
    Represent a select menu with developer-defined options.
    """

    options: List[Union[dict, DiscordSelectOption]]

    def __init__(
        self,
        custom_id: str,
        options: Optional[List[Union[dict, DiscordSelectOption]]] = None,
        **kwargs,
    ) -> None:
        """
        :param str custom_id: developer-defined identifier for the select menu
        :param list options: choices of the select menu (up to 25)
        """
        self.type = constants.DISCORD_COMPONENT_TYPE_STRING_SELECT
        self.options = []

        super().__init__(custom_id, **kwargs)

        for option in options or []:
            self.add_option(option)

    def add_option(self, option: Union[dict, DiscordSelectOption]) -> None:
        """
        Add an option to the select menu.
        :param option: option instance or dict
        """
        if len(self.options) >= constants.DISCORD_MAX_SELECT_OPTIONS:
            raise ComponentException(
                "A select menu can contain up to"
                f" {constants.DISCORD_MAX_SELECT_OPTIONS} options."
            )
        self.options.append(option)


class BaseDiscordComponentAutoPopulatedSelect(BaseDiscordComponentSelect):
    """
    A base class for select menus that are populated by Discord itself.
    """

    default_values: List[Dict[str, str]]

    #: value of the ``type`` field of a default value entry
    default_value_type: str = ""

    def __init__(self, custom_id: str, **kwargs) -> None:
        """
        :param str custom_id: developer-defined identifier for the select menu
        :keyword list default_values: ids that are selected by default
        """
        self.default_values = []

        super().__init__(custom_id, **kwargs)

        for default_value in kwargs.get("default_values") or []:
            self.add_default_value(default_value)

    def add_default_value(
        self, value: Union[str, int, Dict[str, str]], value_type: Optional[str] = None
    ) -> None:
        """
        Add a default value to the select menu.
        :param value: id of the user, role or channel or a dict with id and type
        :param str value_type: type of the value ("user", "role" or "channel")
        """
        if not isinstance(value, dict):
            value = {
                "id": str(value),
                "type": value_type or self.default_value_type,
            }
        if value.get("type") not in ["user", "role", "channel"]:
            raise ComponentException(
                'The type of a default value needs to be "user", "role" or "channel".'
            )
        self.default_values.append(value)


class DiscordComponentUserSelect(BaseDiscordComponentAutoPopulatedSelect):
    """
    Represent a select menu for users.
    """

    default_value_type = "user"

    def __init__(self, custom_id: str, **kwargs) -> None:
        self.type = constants.DISCORD_COMPONENT_TYPE_USER_SELECT
        super().__init__(custom_id, **kwargs)


class DiscordComponentRoleSelect(BaseDiscordComponentAutoPopulatedSelect):
    """
    Represent a select menu for roles.
    """

    default_value_type = "role"

    def __init__(self, custom_id: str, **kwargs) -> None:
        self.type = constants.DISCORD_COMPONENT_TYPE_ROLE_SELECT
        super().__init__(custom_id, **kwargs)


class DiscordComponentMentionableSelect(BaseDiscordComponentAutoPopulatedSelect):
    """
    Represent a select menu for mentionables (users and roles).
    """

    default_value_type = "user"

    def __init__(self, custom_id: str, **kwargs) -> None:
        self.type = constants.DISCORD_COMPONENT_TYPE_MENTIONABLE_SELECT
        super().__init__(custom_id, **kwargs)


class DiscordComponentChannelSelect(BaseDiscordComponentAutoPopulatedSelect):
    """
    Represent a select menu for channels.
    """

    channel_types: List[int]
    default_value_type = "channel"

    def __init__(
        self, custom_id: str, channel_types: Optional[List[int]] = None, **kwargs
    ) -> None:
        """
        :param str custom_id: developer-defined identifier for the select menu
        :param list channel_types: channel types that should be included in the menu
        """
        self.type = constants.DISCORD_COMPONENT_TYPE_CHANNEL_SELECT
        self.channel_types = channel_types or []

        for channel_type in self.channel_types:
            if channel_type not in constants.DISCORD_CHANNEL_TYPES:
                raise ComponentException(
                    f"{channel_type!r} is not a valid channel type."
                )

        super().__init__(custom_id, **kwargs)


class DiscordComponentTextInput(BaseDiscordComponent):
    """
    Represent a text input that can be used in a modal.
    """

    max_length: Optional[int]
    min_length: Optional[int]
    placeholder: Optional[str]
    required: Optional[bool]
    style: int
    value: Optional[str]

    def __init__(
        self,
        custom_id: str,
        label: str,
        style: int = constants.DISCORD_COMPONENT_TEXT_INPUT_STYLE_SHORT,
        **kwargs,
    ) -> None:
        """
        :param str custom_id: developer-defined identifier for the text input
        :param str label: label of the text input
        :param int style: text input style (int 1 - 2)
        :keyword int max_length: maximum input length (1 - 4000)
        :keyword int min_length: minimum input length (0 - 4000)
        :keyword str placeholder: text that is shown if the input is empty
        :keyword bool required: whether the text input is required (defaults to true)
        :keyword str value: pre-filled value of the text input
        """
        kwargs["custom_id"] = custom_id
        kwargs["label"] = label
        self.type = constants.DISCORD_COMPONENT_TYPE_TEXT_INPUT
        self.style = style
        self.max_length = kwargs.get("max_length")
        self.min_length = kwargs.get("min_length")
        self.placeholder = kwargs.get("placeholder")
        self.required = kwargs.get("required", True)
        self.value = kwargs.get("value")

        if (
            not is_int(self.style)
            or self.style not in constants.DISCORD_COMPONENT_TEXT_INPUT_STYLES
        ):
            raise ComponentException(
                "The provided text input style is invalid. A valid text input style is"
                " an integer between 1 and 2."
            )
        if not custom_id:
            raise ComponentException("custom_id needs to be provided.")
        check_max_length(label, 45, "label", ComponentException)
        check_max_length(self.placeholder, 100, "placeholder", ComponentException)
        check_max_length(self.value, 4000, "value", ComponentException)

        super().__init__(**kwargs)


class DiscordComponentActionRow(BaseDiscordComponent):
    """
    Represent an action row that can be used in a message.
    """

    components: list
    type: int = constants.DISCORD_COMPONENT_TYPE_ACTION_ROW

    def __init__(
        self,
        components: Optional[List[Union[dict, BaseDiscordComponent]]] = None,
        **kwargs,
    ):
        """
        :keyword components: displayed components in an action row
        """
        self.components = []
        self.type = constants.DISCORD_COMPONENT_TYPE_ACTION_ROW

        super().__init__(**kwargs)

        for component in components or []:
            self.add_component(component)

    def _component_types(self) -> List[Optional[int]]:
        """
        Get the types of all already added components.
        :return: list of component types
        """
        return [component.get("type") for component in self.components]

    def add_component(self, component: Union[dict, BaseDiscordComponent]) -> None:
        """
        Add a component to the row
        :param component: discord component instance
        """
        if isinstance(component, DiscordComponentActionRow):
            raise ComponentException("An action row can't contain another action row.")
        if (
            isinstance(component, DiscordComponentButton)
            and sum(
                1
                for component_type in self._component_types()
                if component_type == constants.DISCORD_COMPONENT_TYPE_BUTTON
            )
            >= constants.DISCORD_MAX_BUTTONS_PER_ACTION_ROW
        ):
            raise ComponentException("An Action Row can contain up to 5 buttons.")

        if not isinstance(component, dict):
            component = component.to_dict()

        component_type = component.get("type")
        existing_types = self._component_types()
        exclusive_types = constants.DISCORD_COMPONENT_SELECT_TYPES + [
            constants.DISCORD_COMPONENT_TYPE_TEXT_INPUT
        ]
        if existing_types and (
            component_type in exclusive_types
            or any(existing_type in exclusive_types for existing_type in existing_types)
        ):
            raise ComponentException(
                "A select menu or text input has to be the only component in an action"
                " row."
            )

        self.components.append(component)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the action row and its components to a dict.
        :return: action row as dict
        """
        return {"type": self.type, "components": to_dict(self.components)}
