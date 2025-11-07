# Discord NSFW Content Moderation Bot

A Discord bot that automatically removes media files (images, videos) from non-NSFW channels to help keep your server organized and safe.

## Features

- Automatically detects and deletes media files in non-NSFW channels
- Notifies users when their media is removed
- Supports common image and video formats: .jpg, .jpeg, .png, .gif, .webp, .mp4, .mov
- Simple commands for testing and help

## Setup Instructions

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section in the left sidebar
4. Click "Reset Token" to get your bot token (save this for step 2)

### 2. Enable Required Intents

**IMPORTANT:** You must enable the "Message Content Intent" for this bot to work:

1. In the Discord Developer Portal, go to your application
2. Click on "Bot" in the left sidebar
3. Scroll down to "Privileged Gateway Intents"
4. Enable **"MESSAGE CONTENT INTENT"** (this is required!)
5. Click "Save Changes"

### 3. Add Bot Token to Replit

The bot token has already been added to your Replit Secrets as `DISCORD_BOT_TOKEN`.

### 4. Invite Bot to Your Server

1. In Discord Developer Portal, go to "OAuth2" > "URL Generator"
2. Select scopes: `bot`
3. Select bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Manage Messages
   - Read Message History
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 5. Run the Bot

Click the "Run" button in Replit. The bot will start and connect to Discord.

## Commands

- `!ping` - Check if the bot is responsive and see latency
- `!help_nsfw` - Show help information (Admin only)

## How It Works

The bot monitors all messages in your server. When someone posts media in a non-NSFW channel, the bot will:
1. Delete the message containing media
2. Send a temporary notification explaining why
3. Log the action to the console

To allow media in specific channels, simply mark those channels as NSFW in Discord's channel settings.

## Required Permissions

The bot needs these permissions to function:
- Read Messages/View Channels
- Send Messages
- Manage Messages (to delete media)
- Read Message History

## Troubleshooting

If the bot isn't working:
1. Make sure "Message Content Intent" is enabled in Discord Developer Portal
2. Verify the bot has "Manage Messages" permission in your server
3. Check that the bot token is correct in Replit Secrets
4. Look at the console logs for error messages
