import asyncio

from discord_webhook import AsyncDiscordWebhook


async def send_webhook(message):
    webhook = AsyncDiscordWebhook(url="your webhook url", content=message)
    await webhook.execute()


async def main():
    await asyncio.gather(
        send_webhook("Async webhook message 1"),
        send_webhook("Async webhook message 2"),
    )  # sends both messages asynchronously


if __name__ == "__main__":
    asyncio.run(main())
