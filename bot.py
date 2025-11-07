import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is ready and monitoring for NSFW content.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.nsfw:
        await bot.process_commands(message)
        return
    
    for attachment in message.attachments:
        if any(attachment.filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov']):
            try:
                await message.delete()
                warning_msg = await message.channel.send(
                    f'{message.author.mention}, media files are not allowed in this channel. '
                    f'Please use an NSFW-marked channel for sharing media content.'
                )
                await warning_msg.delete(delay=10)
                print(f'Deleted media from {message.author} in #{message.channel.name}')
            except discord.Forbidden:
                print(f'Missing permissions to delete message in #{message.channel.name}')
            except Exception as e:
                print(f'Error deleting message: {e}')
            return
    
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')

@bot.command(name='help_nsfw')
@commands.has_permissions(administrator=True)
async def help_nsfw(ctx):
    help_text = """
**NSFW Content Moderation Bot**

This bot automatically removes media files (images, videos) from non-NSFW channels.

**Features:**
- Automatically deletes media files in non-NSFW channels
- Notifies users when their media is removed
- Works with: .jpg, .jpeg, .png, .gif, .webp, .mp4, .mov

**Commands:**
- `!ping` - Check bot latency
- `!help_nsfw` - Show this help message (Admin only)

**Setup:**
Mark channels as NSFW to allow media sharing in those channels.
    """
    await ctx.send(help_text)

def main():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print('ERROR: DISCORD_BOT_TOKEN environment variable not set!')
        print('Please add your Discord bot token to the Secrets.')
        return
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print('ERROR: Invalid Discord bot token!')
    except Exception as e:
        print(f'ERROR: Failed to start bot: {e}')

if __name__ == '__main__':
    main()
