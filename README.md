# Discord NSFW Content Moderation Bot

A focused, reliable Discord moderation bot that automatically removes image/video media posted in non-NSFW channels and notifies users. Minimal, configurable, and easy to extend.

Badges
- Build: https://img.shields.io/badge/build-pending-lightgrey
- License: https://img.shields.io/badge/license-MIT-green

Why this repo
- Keeps servers free of unintended media in non-NSFW channels.
- Small, opinionated codebase for quick customization and reliable operation.

Quick start
1. Clone
   git clone https://github.com/selvatharrun/Discord-Bot.git
   cd Discord-Bot
2. Install
   npm install
3. Configure (use environment variables or your host's secret manager)
   DISCORD_BOT_TOKEN=your_bot_token
4. Enable intents
   In the Discord Developer Portal -> Bot -> Privileged Gateway Intents -> enable MESSAGE CONTENT INTENT
5. Run
   npm start

Minimum requirements
- Node.js 18+
- A Discord application with a Bot token

Core features
- Automatically deletes image/video attachments in non-NSFW channels
- Notifies the author when their media is removed
- Supports: .jpg, .jpeg, .png, .gif, .webp, .mp4, .mov
- Simple commands: !ping, !help_nsfw

Commands
- !ping — Replies with Pong and latency.
- !help_nsfw — Admin-only help for configuration and usage.

Permissions the bot needs
- Read Messages / View Channels
- Send Messages
- Manage Messages (to delete messages)
- Read Message History

How it works (brief)
- The bot watches messages. If a message in a channel that is not marked NSFW contains supported media, it deletes the message, sends a short notification to the user, and logs the action.

Deployment
- Docker
  - Build: docker build -t discord-nsfw-moderator .
  - Run: docker run -e DISCORD_BOT_TOKEN="$DISCORD_BOT_TOKEN" discord-nsfw-moderator
- Process manager (PM2)
  - pm2 start npm --name "discord-nsfw-moderator" -- start

Security & maintenance
- Never commit tokens or secrets. Use environment variables or secret managers.
- Ensure MESSAGE CONTENT INTENT is enabled, otherwise the bot cannot read message content.
- Keep dependencies updated and add tests for any non-Discord logic.

Contributing
1. Fork the repo
2. Create a branch: git checkout -b feature/name
3. Add tests and clear description
4. Open a PR

License
MIT — see LICENSE

Contact
Owner: @selvatharrun — file issues or PRs for bugs, features, or security reports.