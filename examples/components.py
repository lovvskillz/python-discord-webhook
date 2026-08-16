from discord_webhook import (
    DiscordComponentActionRow,
    DiscordComponentButton,
    DiscordComponentChannelSelect,
    DiscordComponentEmoji,
    DiscordComponentStringSelect,
    DiscordSelectOption,
    DiscordWebhook,
    constants,
)

webhook = DiscordWebhook(url="your webhook url", content="Webhook Message")

# a row with two buttons
buttons = DiscordComponentActionRow(
    components=[
        DiscordComponentButton(
            style=constants.DISCORD_COMPONENT_BUTTON_STYLE_LINK,
            label="Documentation",
            url="https://github.com/lovvskillz/python-discord-webhook",
        ),
        DiscordComponentButton(
            style=constants.DISCORD_COMPONENT_BUTTON_STYLE_DANGER,
            custom_id="delete_message",
            label="Delete",
            emoji=DiscordComponentEmoji(name="🗑️"),
        ),
    ]
)
webhook.add_component_row(buttons)

# a select menu needs its own action row
select = DiscordComponentStringSelect(
    custom_id="favourite_color",
    placeholder="Choose your favourite color",
    options=[
        DiscordSelectOption(label="Red", value="red", description="like a tomato"),
        DiscordSelectOption(label="Blue", value="blue", default=True),
    ],
)
webhook.add_component_row(DiscordComponentActionRow(components=[select]))

# select menus that are populated by Discord itself
channel_select = DiscordComponentChannelSelect(
    custom_id="channel",
    placeholder="Choose a channel",
    channel_types=[constants.DISCORD_CHANNEL_TYPE_GUILD_TEXT],
    max_values=3,
)
webhook.add_component_row(DiscordComponentActionRow(components=[channel_select]))

response = webhook.execute()
