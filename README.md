# discord-channel-creator

A Python 3 script that creates multiple channels under a specified category on your Discord server using the Discord bot API.

## Requirements

- Python 3.10+
- A Discord bot token ([Discord Developer Portal](https://discord.com/developers/applications))
- The bot must have the **Manage Channels** permission on your server

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```
DISCORD_TOKEN=your-bot-token-here
GUILD_ID=your-guild-id-here
```

> **Tip:** Enable Developer Mode in Discord (Settings → Advanced), then right-click your server icon and choose **Copy Server ID** to get the Guild ID.

## Usage

```
python3 create_channels.py --category CATEGORY --channels CHANNEL [CHANNEL ...] [options]
```

### Arguments

| Argument | Description |
|---|---|
| `--category NAME` | Name of the category to place channels under (created automatically if missing) |
| `--channels NAME [NAME ...]` | One or more channel names to create |
| `--type text\|voice` | Channel type to create (default: `text`) |
| `--token TOKEN` | Bot token (overrides `DISCORD_TOKEN` env var) |
| `--guild ID` | Guild/server ID (overrides `GUILD_ID` env var) |

### Examples

**Create text channels under a category:**

```bash
python3 create_channels.py \
  --category "Community" \
  --channels general announcements off-topic resources
```

**Create voice channels under a category:**

```bash
python3 create_channels.py \
  --category "Voice Rooms" \
  --channels "Room 1" "Room 2" "Room 3" \
  --type voice
```

**Override credentials on the command line:**

```bash
python3 create_channels.py \
  --token YOUR_TOKEN \
  --guild 123456789012345678 \
  --category "My Category" \
  --channels channel-one channel-two
```

## GitHub Actions

You can run this script directly from GitHub without any local setup.

### 1. Add repository secrets

Go to your repository → **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name | Value |
|---|---|
| `DISCORD_TOKEN` | Your Discord bot token |
| `GUILD_ID` | Your Discord server (guild) ID |

These values are stored encrypted by GitHub and are never exposed in logs.

### 2. Trigger the workflow

Go to **Actions → Create Discord Channels → Run workflow** and fill in:

| Input | Description |
|---|---|
| `category` | Name of the category to place channels under |
| `channels` | Space-separated channel names (e.g. `general announcements off-topic`) |
| `channel_type` | `text` or `voice` (default: `text`) |

The workflow checks out the repository, installs dependencies, and runs `create_channels.py` with the secrets injected securely as environment variables. The token and guild ID are never visible in the workflow logs or inputs.

---

## Notes

- If the specified category already exists, the script uses it; otherwise it creates a new one.
- Channel names that already exist in the category will trigger an error from the Discord API (duplicate channel names are not allowed within the same category).
- The bot token and guild ID are never printed to standard output.