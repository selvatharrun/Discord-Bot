import os
import discord
from discord.ext import commands
import model_v1
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

#ensuring that the model is loaded at startup.
model_path = model_v1.ensure_model()

print(f"Model path: {model_path}")
model_v1.load_model(model_path)

#all the discord bot events and commands bs starts here.
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
        if any(attachment.filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            #we handle the images here, predict and delete if needed.
            try:
                downloads_dir = Path("./downloads")
                downloads_dir.mkdir(parents=True, exist_ok=True)
                file_path = str(downloads_dir / attachment.filename)
                await attachment.save(file_path)

                # Run prediction (model.predict_face will load the persistent model if needed)
                results = model_v1.predict_face(file_path)
                confs_dict = model_v1.get_confidence(results)

                threshold = 0.5
                flagged = False
                # confs_dict: { image_index: { 'confidences': [...], 'labels': [...] } }
                for img_idx, data in confs_dict.items():
                    for conf in data.get('confidences', []):
                        if conf > threshold:
                            print(f"Detected face with confidence: {conf:.4f}")
                            flagged = True
                            break
                    if flagged:
                        break

                if flagged:
                    # Take action based on detection (e.g., alert user, log event)
                    try:
                        await message.delete()
                    except discord.Forbidden:
                        # If we lack delete permissions, still notify in channel
                        pass
                    warning_msg = await message.channel.send(
                        f'{message.author.mention}, your media was removed because it was flagged by the moderation bot. got you rayhan.'
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

This bot automatically removes media files (images, videos) from non-NSFW channels that rayhan sends.
and wtv others send too, but we know who is going to be sending them.

**Features:**
- Automatically deletes media files in non-NSFW channels that rayhan sends.
- Notifies users when their media is removed
- Works with: .jpg, .jpeg, .png, .gif, .webp, .mp4, .mov

**Commands:**
- `!ping` - Check bot latency
- `!help_nsfw` - Show this help message (Admin only)

**Setup:**
Mark channels as NSFW to allow media sharing in those channels. And the mute those channels, coz only rayhan is going to use it.
    """
    await ctx.send(help_text)

def main():
    token = "MTQzNjMxMzQzNzg4NTE3MzkzMg.GtZ6M_.fdlNLXcRLF_hrsvh8dvYvCE5Elb2QP1J7JKyKc"
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
