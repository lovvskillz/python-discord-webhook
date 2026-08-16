import pytest
from pytest import mark

from discord_webhook import (
    DiscordComponentEmoji,
    DiscordPoll,
    DiscordPollAnswer,
    DiscordPollMedia,
    DiscordWebhook,
    constants,
)
from discord_webhook.webhook_exceptions import PollException


def test__poll__defaults():
    poll = DiscordPoll(question="Your favourite color?", answers=["Red", "Blue"])

    assert poll.to_dict() == {
        "question": {"text": "Your favourite color?"},
        "answers": [
            {"poll_media": {"text": "Red"}},
            {"poll_media": {"text": "Blue"}},
        ],
        "allow_multiselect": False,
        "duration": constants.DISCORD_POLL_DEFAULT_DURATION,
        "layout_type": constants.DISCORD_POLL_LAYOUT_TYPE_DEFAULT,
    }


def test__poll__custom_values():
    poll = DiscordPoll(
        question=DiscordPollMedia(text="Your favourite color?"),
        allow_multiselect=True,
        duration=48,
    )
    poll.add_answer(
        DiscordPollAnswer(text="Red", emoji=DiscordComponentEmoji(name="🔴"))
    )
    poll.add_answer({"poll_media": {"text": "Blue"}})

    assert poll.to_dict() == {
        "question": {"text": "Your favourite color?"},
        "answers": [
            {"poll_media": {"text": "Red", "emoji": {"name": "🔴", "animated": False}}},
            {"poll_media": {"text": "Blue"}},
        ],
        "allow_multiselect": True,
        "duration": 48,
        "layout_type": constants.DISCORD_POLL_LAYOUT_TYPE_DEFAULT,
    }


def test__poll__answer_without_text_and_emoji():
    with pytest.raises(PollException) as excinfo:
        DiscordPollAnswer()

    assert str(excinfo.value) == "Either text or emoji needs to be provided."


def test__poll__max_answers():
    poll = DiscordPoll(
        question="test",
        answers=[str(index) for index in range(constants.DISCORD_POLL_MAX_ANSWERS)],
    )

    with pytest.raises(PollException) as excinfo:
        poll.add_answer("one too many")

    assert str(excinfo.value) == "A poll can contain up to 10 answers."
    assert len(poll.get_answers()) == constants.DISCORD_POLL_MAX_ANSWERS


def test__poll__remove_answer():
    poll = DiscordPoll(question="test", answers=["Red", "Blue"])
    poll.remove_answer(0)

    assert poll.to_dict()["answers"] == [{"poll_media": {"text": "Blue"}}]


def test__poll__without_answers():
    poll = DiscordPoll(question="test")

    with pytest.raises(PollException) as excinfo:
        poll.to_dict()

    assert str(excinfo.value) == "A poll needs at least one answer."


@mark.parametrize("invalid_duration", [0, 769, "a", True, None])
def test__poll__invalid_duration(invalid_duration):
    with pytest.raises(PollException) as excinfo:
        DiscordPoll(question="test", duration=invalid_duration)

    assert str(excinfo.value) == "duration needs to be an integer between 1 and 768."


def test__poll__invalid_layout_type():
    with pytest.raises(PollException) as excinfo:
        DiscordPoll(question="test", layout_type=2)

    assert str(excinfo.value) == "The provided layout type is invalid."


@mark.parametrize(
    "poll_media_class, max_length",
    [
        (DiscordPollMedia, constants.DISCORD_POLL_MAX_QUESTION_LENGTH),
        (DiscordPollAnswer, constants.DISCORD_POLL_MAX_ANSWER_LENGTH),
    ],
)
def test__poll__max_text_length(poll_media_class, max_length):
    poll_media_class(text="a" * max_length)

    with pytest.raises(PollException) as excinfo:
        poll_media_class(text="a" * (max_length + 1))

    assert str(excinfo.value) == f"text can be a maximum of {max_length} characters."


def test__webhook__poll():
    webhook = DiscordWebhook(
        url="webhook_url",
        poll=DiscordPoll(question="Your favourite color?", answers=["Red", "Blue"]),
    )

    assert webhook.json["poll"]["question"] == {"text": "Your favourite color?"}

    webhook.remove_poll()
    assert "poll" not in webhook.json


def test__webhook__set_poll():
    webhook = DiscordWebhook(url="webhook_url")
    webhook.set_poll({"question": {"text": "test"}})

    assert webhook.json["poll"] == {"question": {"text": "test"}}
