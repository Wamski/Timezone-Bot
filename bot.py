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

# import database.py
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

            # Get the user time zone
            author: int = message.author.id
            timezoneStr: Str = get_user_timezone(author)
            authorTimezone = pytz.timezone(timezoneStr)

            settings = {
                'RELATIVE_BASE': datetime.now(authorTimezone),
                'PREFER_DATES_FROM': 'past',
            }

            parsedTime = dateparser.parse(timeString, settings=settings)
            
            # Convert to unix timestamp 
            if (parsedTime):
                localized = authorTimezone.localize(parsedTime.replace(tzinfo=None))
                unixTS = int(localized.timestamp())
                
                try: 
                    await message.reply(f"Corrected Time: <t:{unixTS}:t>")
                except Exception as e:
                    print("Failed to send converted time")
                    print(e)









# Setup Server intents, and allow the bot to read messages
intents = discord.Intents.default()
intents.message_content = True

# Initialize the client
client = Client(command_prefix="!", intents=intents)


# Initalize the slash commands
@client.tree.command(name='set_timezone', description='Appends a user defined timezone to the bot database')
@app_commands.describe(
    timezone = 'What is your timezone? (Ex: America/New_York) ',
)
async def setTimezone(interaction: discord.Interaction, timezone: str) -> None:
    try:
        set_user_timezone(interaction.user.id, timezone)
        await interaction.response.send_message(f'{interaction.user.mention}: Timezone set to {timezone}')
    except Exception as e:
        print("Failed to set user timezone")
        print(e)

@client.tree.command(name='view_timezones', description='View the timezones in your country')
@app_commands.describe(
    country_code = "What is your country code? (EX: US or CA) "
)
async def getTimzones(interaction: discord.Interaction, country_code: str) -> None:
    code = country_code.upper()
    zones = pytz.country_timezones[code]

    zoneList = "\n".join(zones)

    embed = discord.Embed(
        title=f"Timzones for {code}",
        description=f"```\n{zoneList}\n```",
        color=discord.Color.blue()
    )

    await interaction.response.send_message(embed=embed)

# Load the Token and run the client
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
client.run(TOKEN)

