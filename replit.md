# Discord NSFW Content Moderation Bot

## Overview

This is a Discord bot designed to automatically moderate NSFW content by removing media files from non-NSFW channels. The bot monitors all messages and deletes images and videos posted in channels that aren't marked as NSFW, helping maintain server organization and safety.

**Current State:** Bot is fully configured and ready to run. User needs to enable "Message Content Intent" in Discord Developer Portal for the bot to function.

## Recent Changes

**November 7, 2025:**
- Initial project setup from GitHub import
- Created bot.py with NSFW content moderation functionality
- Added requirements.txt with discord.py dependency
- Configured Python 3.11 environment
- Set up workflow to run the bot
- Added comprehensive setup documentation
- Configured Discord bot token in Replit Secrets

## Project Architecture

### Structure
```
.
├── bot.py              # Main bot application
├── requirements.txt    # Python dependencies
├── README.md          # User-facing documentation
├── replit.md          # Project memory and documentation
└── .gitignore         # Python gitignore patterns
```

### Technology Stack
- **Language:** Python 3.11
- **Framework:** discord.py 2.6.4
- **Environment:** Replit with Nix package management

### Bot Functionality

**Core Features:**
1. Monitors all messages in Discord servers
2. Detects media attachments (.jpg, .jpeg, .png, .gif, .webp, .mp4, .mov)
3. Deletes media posted in non-NSFW channels
4. Sends temporary warning messages to users
5. Logs all moderation actions

**Commands:**
- `!ping` - Health check and latency test
- `!help_nsfw` - Display help information (admin only)

**Event Handlers:**
- `on_ready` - Confirms bot connection
- `on_message` - Main moderation logic

### Configuration

**Environment Variables:**
- `DISCORD_BOT_TOKEN` - Discord bot authentication token (stored in Replit Secrets)

**Required Discord Intents:**
- Default intents
- Message Content Intent (privileged - must be enabled in Developer Portal)
- Messages intent

**Required Bot Permissions:**
- Read Messages/View Channels
- Send Messages
- Manage Messages
- Read Message History

## Setup Requirements

### Discord Developer Portal Setup
1. Create application at https://discord.com/developers/applications
2. Create bot user and obtain token
3. **Enable "Message Content Intent" under Bot > Privileged Gateway Intents**
4. Generate invite URL with required permissions
5. Invite bot to target server

### Replit Configuration
- Python 3.11 module installed
- discord.py package installed via pip
- Workflow configured to run `python bot.py`
- Bot token stored in Secrets as DISCORD_BOT_TOKEN

## Important Notes

### Critical Setup Step
The bot **requires** the "Message Content Intent" to be enabled in the Discord Developer Portal. Without this:
- The bot will fail to start with a privileged intents error
- The error message will direct users to enable intents in the developer portal

### Deployment Considerations
- This is a long-running bot (not a web application)
- No frontend or port configuration needed
- Uses console output type in workflow
- Bot maintains persistent connection to Discord

### Security
- Bot token is stored securely in Replit Secrets
- Token is never logged or exposed in code
- Bot only has necessary permissions for moderation

## User Preferences

None specified yet.

## Next Steps

For users:
1. Enable "Message Content Intent" in Discord Developer Portal
2. Invite bot to Discord server with required permissions
3. Run the bot using the workflow
4. Mark channels as NSFW where media should be allowed

For development:
- Bot is feature-complete for basic NSFW content moderation
- Could add: custom configuration, whitelisted users, logging to database, web dashboard
