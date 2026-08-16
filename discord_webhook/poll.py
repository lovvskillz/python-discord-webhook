from typing import Any

from . import constants
from .components import DiscordComponentEmoji
from .utils import check_max_length, is_int, to_dict
from .webhook_exceptions import PollException


class DiscordPollMedia:
    """
    Represent the common object that is used by the question and the answers of a poll.
    """

    emoji: dict | DiscordComponentEmoji | None
    text: str | None

    def __init__(
        self,
        text: str | None = None,
        emoji: dict | DiscordComponentEmoji | None = None,
        max_text_length: int = constants.DISCORD_POLL_MAX_QUESTION_LENGTH,
    ) -> None:
        """
        :param str text: text of the media object
        :param emoji: emoji of the media object
        :param int max_text_length: maximum amount of characters of the text
        """
        if text is None and emoji is None:
            raise PollException("Either text or emoji needs to be provided.")

        self.text = text
        self.emoji = emoji

        check_max_length(self.text, max_text_length, "text", PollException)

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the media object to a dict.
        :return: media object as dict
        """
        return {
            key: to_dict(value)
            for key, value in self.__dict__.items()
            if value is not None
        }


class DiscordPollAnswer(DiscordPollMedia):
    """
    Represent an answer of a poll.
    """

    def __init__(
        self,
        text: str | None = None,
        emoji: dict | DiscordComponentEmoji | None = None,
    ) -> None:
        """
        :param str text: text of the answer
        :param emoji: emoji of the answer
        """
        super().__init__(
            text=text,
            emoji=emoji,
            max_text_length=constants.DISCORD_POLL_MAX_ANSWER_LENGTH,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the answer to a dict.
        :return: answer as dict
        """
        return {"poll_media": super().to_dict()}


class DiscordPoll:
    """
    Represent a poll object for the use in webhooks.
    """

    allow_multiselect: bool
    answers: list[dict | DiscordPollAnswer]
    duration: int
    layout_type: int
    question: dict | DiscordPollMedia | str

    def __init__(
        self,
        question: dict | DiscordPollMedia | str,
        answers: list[dict | DiscordPollAnswer | str] | None = None,
        **kwargs,
    ) -> None:
        """
        :param question: question of the poll (only text is supported by Discord)
        :param list answers: answers of the poll (up to 10)
        :keyword bool allow_multiselect: whether multiple answers can be selected
        :keyword int duration: hours the poll is open for (1 - 768, defaults to 24)
        :keyword int layout_type: layout of the poll (defaults to 1)
        """
        self.question = (
            DiscordPollMedia(text=question) if isinstance(question, str) else question
        )
        self.answers = []
        self.allow_multiselect = kwargs.get("allow_multiselect", False)
        self.duration = kwargs.get("duration", constants.DISCORD_POLL_DEFAULT_DURATION)
        self.layout_type = kwargs.get(
            "layout_type", constants.DISCORD_POLL_LAYOUT_TYPE_DEFAULT
        )

        if (
            not is_int(self.duration)
            or not 1 <= self.duration <= constants.DISCORD_POLL_MAX_DURATION
        ):
            raise PollException(
                "duration needs to be an integer between 1 and"
                f" {constants.DISCORD_POLL_MAX_DURATION}."
            )
        if self.layout_type not in constants.DISCORD_POLL_LAYOUT_TYPES:
            raise PollException("The provided layout type is invalid.")

        for answer in answers or []:
            self.add_answer(answer)

    def add_answer(self, answer: dict | DiscordPollAnswer | str) -> None:
        """
        Add an answer to the poll.
        :param answer: answer instance, dict or the text of the answer
        """
        if len(self.answers) >= constants.DISCORD_POLL_MAX_ANSWERS:
            raise PollException(
                f"A poll can contain up to {constants.DISCORD_POLL_MAX_ANSWERS} answers."
            )
        self.answers.append(
            DiscordPollAnswer(text=answer) if isinstance(answer, str) else answer
        )

    def remove_answer(self, index: int) -> None:
        """
        Remove an answer from the already added answers.
        :param int index: index of the answer
        """
        self.answers.pop(index)

    def get_answers(self) -> list[dict | DiscordPollAnswer]:
        """
        Get all answers of the poll as a list.
        :return: answers of the poll
        """
        return self.answers

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the poll to a dict.
        :return: poll as dict
        """
        if not self.answers:
            raise PollException("A poll needs at least one answer.")

        return {
            "question": to_dict(self.question),
            "answers": to_dict(self.answers),
            "allow_multiselect": self.allow_multiselect,
            "duration": self.duration,
            "layout_type": self.layout_type,
        }
