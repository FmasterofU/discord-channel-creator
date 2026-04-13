#!/usr/bin/env python3
"""
Discord Channel Creator
Creates multiple channels under a specified category on a Discord server.
"""

import argparse
import asyncio
import os
import sys

import discord
from dotenv import load_dotenv

load_dotenv()


async def create_channels(
    token: str,
    guild_id: int,
    category_name: str,
    channel_names: list[str],
    channel_type: str = "text",
) -> None:
    """
    Connect to Discord and create channels under the specified category.

    Args:
        token: Discord bot token.
        guild_id: ID of the target guild (server).
        category_name: Name of the category to place channels under.
                       The category is created if it does not exist.
        channel_names: List of channel names to create.
        channel_type: Type of channels to create – 'text' or 'voice'.
    """
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    async with client:
        await client.login(token)

        try:
            guild: discord.Guild = await client.fetch_guild(guild_id)
        except discord.NotFound:
            print(
                f"Error: Guild with ID {guild_id} not found (Discord error 10004).\n"
                "Common causes:\n"
                "  • The bot has not been added to the server. Invite it at:\n"
                "    https://discord.com/oauth2/authorize?client_id=<YOUR_CLIENT_ID>&scope=bot&permissions=16\n"
                "  • The Guild ID is incorrect. Right-click the server icon in Discord "
                "(with Developer Mode enabled) and choose 'Copy Server ID'.",
                file=sys.stderr,
            )
            return
        except discord.Forbidden:
            print(
                f"Error: The bot does not have permission to access guild {guild_id}.",
                file=sys.stderr,
            )
            return

        # Find or create the category
        category: discord.CategoryChannel | None = discord.utils.get(
            await guild.fetch_channels(), name=category_name, type=discord.ChannelType.category
        )

        if category is None:
            print(f"Category '{category_name}' not found. Creating it…")
            category = await guild.create_category(category_name)
            print(f"Created category '{category_name}' (ID: {category.id})")
        else:
            print(f"Found existing category '{category_name}' (ID: {category.id})")

        # Create each channel under the category
        for name in channel_names:
            try:
                if channel_type == "voice":
                    channel = await guild.create_voice_channel(name, category=category)
                else:
                    channel = await guild.create_text_channel(name, category=category)
                print(f"  ✓ Created {channel_type} channel '{channel.name}' (ID: {channel.id})")
            except discord.HTTPException as exc:
                print(f"  ✗ Failed to create channel '{name}': {exc}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create multiple Discord channels under a category.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 create_channels.py --guild 123456789 --category "My Category" \\
      --channels general announcements off-topic

  python3 create_channels.py --guild 123456789 --category "Voice Rooms" \\
      --channels "Room 1" "Room 2" --type voice

Environment variables (can be set in a .env file):
  DISCORD_TOKEN   Bot token (required if --token is not provided)
  GUILD_ID        Guild/server ID (required if --guild is not provided)
        """,
    )
    parser.add_argument(
        "--token",
        default=os.getenv("DISCORD_TOKEN"),
        help="Discord bot token (or set DISCORD_TOKEN env var).",
    )
    parser.add_argument(
        "--guild",
        type=int,
        default=int(val) if (val := os.getenv("GUILD_ID")) else None,
        help="Discord guild (server) ID (or set GUILD_ID env var).",
    )
    parser.add_argument(
        "--category",
        required=True,
        help="Name of the category to create channels under.",
    )
    parser.add_argument(
        "--channels",
        nargs="+",
        required=True,
        metavar="CHANNEL",
        help="One or more channel names to create.",
    )
    parser.add_argument(
        "--type",
        dest="channel_type",
        choices=["text", "voice"],
        default="text",
        help="Type of channels to create (default: text).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.token:
        print(
            "Error: Discord bot token is required. "
            "Provide it via --token or the DISCORD_TOKEN environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.guild:
        print(
            "Error: Guild ID is required. "
            "Provide it via --guild or the GUILD_ID environment variable.",
            file=sys.stderr,
        )
        sys.exit(1)

    asyncio.run(
        create_channels(
            token=args.token,
            guild_id=args.guild,
            category_name=args.category,
            channel_names=args.channels,
            channel_type=args.channel_type,
        )
    )


if __name__ == "__main__":
    main()
