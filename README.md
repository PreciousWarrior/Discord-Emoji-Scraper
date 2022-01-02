# Discord-Emoji-Scraper

Scrapes emojis of a discord server/guild and downloads them to your machine, in case you lost the original emojis for your own server or would like to download emojis for any other server to use elsewhere. Supports animated and standard emojis.

# Installation

1. You will need to install python 3.x, PIP, and git in order to use this program. These tools come preinstalled in most MacOS and Linux systems. If you are running Windows, you can either install them seperately by searching for the installers on the internet, or install WSL (Windows subsystem for Linux)
2. Open a shell window, (Command Prompt on Windows or Terminal on MacOS)
3. Type the following commands (these commands will install the software)

    `$ git clone https://github.com/PreciousWarrior/Discord-Emoji-Scraper.git`

    `$ cd Discord-Emoji-Scraper`

    `# pip install -r requirements.txt`

# Usage

To scrape stickers, run: `python stickerscraper.py`

To scrape emojis, run: `python emojiscraper.py`

Follow any instructions that you see.

# Contributing

If you have any questions create an issue in the github repo.
If you are facing any errors, bugs or having suggestions, create an issue in the GitHub repo.
If you would like to work on any of the TODO points in the code, feel free to work on them and add a PR

**NOTE ABOUT STICKERS:** Stickers can be both static and animated picture aswell, however animated pictures use the APNG format (Animated PNG), animated stickers will end under the ".anpg", you should use convert them to gif/webp if you want to use them OR when prompted to convert stickers from apng to gif then accept it.

# WARNING! READ THIS BEFORE USING

Using this tool will break the Discord TOS since you will be scraping their website.
This tool may not work properly with MFA tokens (if you have two factor authentication enabled), so if you get a failed to fetch guild name error try using an alt account that has 2FA disabled.
By using this tool, you agree that the creator of this tool has no responsibility for any action taken
against your account or against you legally.
I strongly recommend you to use an alt account's token with this tool.
I strongly recommend you to use Tor, VPN or a proxy along with this tool.

# TODO

-   [x] Error handling
-   [x] Add cooldown for x seconds after x amount of emoji(s) were downloaded
-   [x] Sticker support
-   [x] (Stickers only) Automatic conversion to conver APNG format to GIF/WEBP
-   [ ] Add support for all guilds of a uid, or selection from guilds
-   [ ] Built-in proxy support
-   [ ] Add versions compiled to executables (like .exe for Windows, elf binaries for Linux, etc) (A GitHub deployment workflow could work here)
-   [ ] UI support?
-   [ ] Rewrite the code itself to be much more cleaner
-   [ ] Merge both emoji and sticker scraper in a single python file
-   [ ] Multithreading support

# Tutorial videos on some stuff

-   How to get guild ID: https://youtu.be/6dqYctHmazc
-   How to get discord account token: https://youtu.be/YEgFvgg7ZPI
