import discord
from discord import app_commands
from discord.ext import commands
import os
import re
import pytz
import dateparser
from datetime import datetime
from dotenv import load_dotenv
from typing import Final

# DATABASE INTEGRATION
from database import init_db, get_user_timezone, set_user_timezone

class Client(commands.Bot):
    async def on_ready(self) -> None:
        await client.tree.sync()
        print(f"{self.user} has connected to Discord!")

    # Anytime a user messages in a server this method runs
    async def on_message(self, message: discord.Message) -> None:
        # Ignore bot messages
        if message.author == self.user:
            return

        content: str = message.content

        # Search the content to see if a time is in the message
        timePattern = r"\b(?:\d{1,2}:\d{2}(?:\s?[aApP][mM])?|\d{1,2}\s?[aApP][mM])\b"
        match = re.search(timePattern, content)

        if match:
            # Get the time
            timeString = match.group(0)

            # Get the user time zone from the database
            author: int = message.author.id
            timezoneStr: str = get_user_timezone(author)
            authorTimezone = pytz.timezone(timezoneStr)

            # Configure dateparser to interpret the time based on the user's current local timezone
            settings = {
                'RELATIVE_BASE': datetime.now(authorTimezone),
                'PREFER_DATES_FROM': 'past',
            }
    
            parsedTime = dateparser.parse(timeString, settings=settings)
            
            # Discord uses Unix Timestamps to show dynamic time to different users 
            if (parsedTime):
                # Apply the user's timezone to the parsed datetime object
                localized = authorTimezone.localize(parsedTime.replace(tzinfo=None))
                unixTS = int(localized.timestamp())
                
                try:
                    # Reply with Discord's timestamp format
                    await message.reply(f"Your Time: <t:{unixTS}:t>")
                except Exception as e:
                    print("Failed to send converted time")
                    print(e)


# BOT CONFIGURATION:

# Set permissions: 'message_content' is required to read text in messages 
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client
client = Client(command_prefix="!", intents=intents)


# SLASH COMMANDS

# Command: /set_timezone
# set_timezone takes in a string for the user's timezone that will be stored inside of the 'user_prefs' table in the database
# The user's Discord ID will be used as the primary key of 'user_prefs'
@client.tree.command(name='set_timezone', description='Appends a user defined timezone to the bot database')
@app_commands.describe(
    timezone = 'What is your timezone? (Ex: America/New_York) ',
)
async def setTimezone(interaction: discord.Interaction, timezone: str) -> None:
    try:
        # 'Upsert' the user's timezone into the database and respond back to the user with their selected timezone
        set_user_timezone(interaction.user.id, timezone)
        await interaction.response.send_message(f'{interaction.user.mention}: Timezone set to {timezone}')
    except Exception as e:
        print("Failed to set user timezone")
        print(e)

# Command: /view_timezones
# view_timezones takes in 2 character string to use as a country code 'country_code'
# This country_code will be fed into pytz to retrieve the timezones for that specific country
# Sends an embed containing the country's timezones
@client.tree.command(name='view_timezones', description='View the timezones in your country')
@app_commands.describe(
    country_code = "What is your country code? (EX: US or CA) "
)
async def getTimzones(interaction: discord.Interaction, country_code: str) -> None:
    # Make sure the country_code is upercased and retrieve the timezones
    code = country_code.upper()
    zones = pytz.country_timezones[code]
    
    # Format the zones to be vertical
    zoneList = "\n".join(zones)

    # Create a discord embed
    embed = discord.Embed(
        title=f"Timzones for {code}",
        description=f"```\n{zoneList}\n```",
        color=discord.Color.blue()
    )
    
    # Attempt to send the embed
    try: 
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        print("Failed to create an embed of timezones")
        print(e)

# BOT START
# Load the Token and run the client
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)

