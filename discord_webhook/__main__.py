""" Entry point to trigger webhook(s). """
import argparse
import sys

from discord_webhook import DiscordWebhook


def main() -> bool:
    parser = argparse.ArgumentParser(
        prog="discord_webhook", description="Trigger discord webhook(s)."
    )
    parser.add_argument("-u", "--url", required=True, help="Webhook URL")
    parser.add_argument("-c", "--content", required=True, help="Message content")
    parser.add_argument(
        "--username", default=None, help="override the default username of the webhook"
    )
    parser.add_argument(
        "--avatar_url", default=None, help="override the default avatar of the webhook"
    )
    args = parser.parse_args()
    webhook = DiscordWebhook(
        url=args.url,
        content=args.content,
        username=args.username,
        avatar_url=args.avatar_url,
    )
    return webhook.execute() is not None


if __name__ == "__main__":
    sys.exit(main())
