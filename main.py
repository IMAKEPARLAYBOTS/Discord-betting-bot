# main.py - Discord bot with ticket system and modular betting analysis
# Author: [Your Name]
# Date: September 25, 2025
# Uses discord.py for bot, pytesseract for OCR, openai for analysis

import discord
from discord.ext import commands
import config  # Import config for tokens and IDs
from keep_alive import keep_alive  # Import Flask keep-alive
import io
from PIL import Image
import pytesseract
import openai
import re  # For potential text parsing

# Set up OpenAI client
openai.api_key = config.OPENAI_API_KEY

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # For role checking
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    guild = bot.get_guild(config.GUILD_ID)
    if guild:
        print(f'Connected to guild: {guild.name}')

# Command: !ticket - Create a private ticket channel
@bot.command(name='ticket')
async def create_ticket(ctx):
    guild = ctx.guild
    category = guild.get_channel(config.TICKET_CATEGORY_ID)  # Category for tickets
    if not category or not isinstance(category, discord.CategoryChannel):
        await ctx.send("Ticket category not found.")
        return

    # Create private channel for the user
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    ticket_channel = await guild.create_text_channel(
        f'ticket-{ctx.author.name}',
        category=category,
        overwrites=overwrites
    )
    await ctx.send(f'Ticket created: {ticket_channel.mention}')
    await ticket_channel.send(f'Welcome {ctx.author.mention}! Use !parlay with an attached image.')

# Command: !parlay - Process attached image in ticket channel
@bot.command(name='parlay')
async def parlay(ctx):
    if not ctx.channel.name.startswith('ticket-'):
        await ctx.send('This command can only be used in a ticket channel.')
        return

    if not ctx.message.attachments:
        await ctx.send('Please attach a PrizePicks lineup image.')
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        await ctx.send('Attachment must be an image (PNG/JPG).')
        return

    # Download image
    image_bytes = await attachment.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Placeholder: OCR extraction
    extracted_text = ocr_extract(image)  # Call placeholder function
    await ctx.send(f'Extracted data: {extracted_text}')

    # Placeholder: Role checking
    is_premium = check_premium_role(ctx.author)  # Call placeholder function

    if is_premium:
        # Premium analysis
        analysis = premium_analysis(extracted_text)  # Call placeholder
    else:
        # Free analysis
        analysis = free_analysis(extracted_text)  # Call placeholder

    await ctx.send(analysis)

# Placeholder: OCR extraction function
# Extracts player names, stat types (e.g., points, rebounds), and projections from image
# Modular: Can add logic for other platforms (e.g., Underdog) by checking image patterns
def ocr_extract(image):
    # Use pytesseract to get text
    text = pytesseract.image_to_string(image)
    # Parse text (e.g., regex for players/stats/projections)
    # Example parsing (placeholder - implement based on PrizePicks format)
    players = re.findall(r'Player: (\w+ \w+)', text)  # Dummy regex
    stats = re.findall(r'Stat: (\w+)', text)
    projections = re.findall(r'Projection: (\d+\.?\d*)', text)
    data = list(zip(players, stats, projections)) if players else []
    return data  # Return list of tuples: [('Player Name', 'Stat', 'Projection'), ...]

# Placeholder: Check if user has Premium role
def check_premium_role(member):
    premium_role = discord.utils.get(member.roles, name=config.PREMIUM_ROLE_NAME)
    return premium_role is not None

# Placeholder: Premium analysis using detailed OpenAI prompt
# Acts as top sports betting analyst with last 5 games, opponent defense, trends, etc.
# Modular: Can pass platform='prizepicks' or others
def premium_analysis(data, platform='prizepicks'):
    prompt = f"""
    Act as a top sports betting analyst. Analyze this {platform} lineup:
    {data}
    For each pick, include:
    - Last 5 games performance
    - Opponent defense stats
    - Trends and injury notes
    - Confidence rating (1-10)
    - Suggestions for Flex/Power Play
    Provide a detailed report.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# Placeholder: Free analysis using short OpenAI prompt
# Simple MORE/LESS pick with short reason
# Modular: Similar to premium
def free_analysis(data, platform='prizepicks'):
    prompt = f"""
    For this {platform} lineup: {data}
    Give only a MORE or LESS pick for each with a short reason.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

# Start keep-alive server for Replit
keep_alive()

# Run the bot
bot.run(config.DISCORD_BOT_TOKEN)
