<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" alt="Python" width="38" align="left" />

# Timezone Discord Bot

This bot will convert times entered in a Discord server and automatically convert them to each user's timezone.

## Setup

1. Virtual Environment  
This will create a virtual environment that dependencies can be installed inside of.
```bash
python3 -m venv .venv
```

2. Install dependencies  
    1. Activate the virtual environment
    2. Install dependecies
```bash
source .venv/bin/activate
pip3 install -r requirements.txt
```
3. Obtain a Discord Bot Token
    <img align="right" alt="NewApp" width=30% src="/Images/NewApp.png">

    1. Create a new App  

    2. Enable Intents  
    Inside of the Bot application, on the side bar, select "Bot". From there you must enable all of the intents for the bot to be able to read messages.
    <br>
    <img alt="Intents" src="/Images/Intents.png">
    <br><br>
    
    4. Reset and Obtain the Bot Token  
    Still inside the "Bot" tab, select the button saying "Reset Token". This might require a 2FA code to be able to reset. Once this is reset, it will give the token that needs to be placed into `.env`.
    <br>
    <img alt="Reset" src="/Images/Reset.png">


5. Setup .env  
Here is a .env example. Replace "your_token_here" with a token obtained from Discord's developer portal.
```bash
DISCORD_TOKEN=your_token_here
```

5. Invite the bot to your server  
    1. Select the "OAuth2" section on the sidebar. 
    2. From the "OAuth2 URL Generator" select bot
    <img alt="Bot" src="/Images/Bot.png">
    3. Bot permissions: Select "Send Messages" and "Read Message History"
    <img alt="Perms" src="/Images/Perms.png">
    4. Paste the generated URL on your address bar.
    5. Select the server you would like the bot to join and approve the permissions.
    <p align="center">
        <img alt="SelectServer" src="/Images/SelectServer.png" width="45%">
        <img alt="SelectPerms" src="/Images/SelectPerms.png" width="45%">
    </p>

6. Running the bot
```bash
python3 bot.py
```

## Your bot should now be able to interact inside of your server
<img alt="SelectPerms" src="/Images/Example.png">
