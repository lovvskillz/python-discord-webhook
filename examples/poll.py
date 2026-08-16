from discord_webhook import (
    DiscordComponentEmoji,
    DiscordPoll,
    DiscordPollAnswer,
    DiscordWebhook,
)

# a simple poll with two answers that is open for 24 hours
poll = DiscordPoll(question="Your favourite color?", answers=["Red", "Blue"])

webhook = DiscordWebhook(url="your webhook url", poll=poll)
response = webhook.execute()

# a poll with emojis, multiple answers and a custom duration
poll = DiscordPoll(
    question="Which languages do you use?",
    answers=[
        DiscordPollAnswer(text="Python", emoji=DiscordComponentEmoji(name="🐍")),
        DiscordPollAnswer(text="Rust", emoji=DiscordComponentEmoji(name="🦀")),
    ],
    allow_multiselect=True,
    duration=72,
)
poll.add_answer("Something else")

webhook = DiscordWebhook(url="your webhook url", content="Please vote!")
webhook.set_poll(poll)
response = webhook.execute()
