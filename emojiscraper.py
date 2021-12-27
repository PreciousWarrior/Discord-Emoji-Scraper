import os, subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
import requests

warning_info = '''
WARNING! Using this tool will break the Discord TOS since you will be scraping their website.
By continuing, you agree that the creator of this tool has no responsibility for any action taken
against your account or against you legally.
I strongly recommend you to use an alt account's token with this tool.
I strongly recommend you to use Tor, VPN or a proxy along with this tool.
To start scraping, please type "I UNDERSTAND" and press enter.
'''

info = '''
This bot is made by PreciousWarrior.
You can probably find the repository somewhere in my GitHub profile with a name along the lines of "DiscordEmojiScraper".
If you have any questions create an issue in the github repo.
If you are facing any errors, bugs or having suggestions, create an issue in the GitHub repo.
If you would like to work on any of the TODO points in the code, feel free to work on them and add a PR
'''

def is_none_empty_whitespace(any_string):
    if any_string == None:
        return True
    if any_string.strip(" ") == "":
        return True
    return False

def get_list_of_emojis(guild_id, token):
    result=requests.get(url=f"https://discordapp.com/api/v7/guilds/{guild_id}/emojis", headers={"authorization":token})
    return result.json()

def get_list_of_stickers(guild_id, token):
    result=requests.get(url=f"https://discordapp.com/api/v9/guilds/{guild_id}/stickers", headers={"authorization":token})
    return result.json()

def scrape_emoji(id, proxy=None):
    if is_none_empty_whitespace(proxy):
        result=requests.get(url=f"https://cdn.discordapp.com/emojis/{id}")
        return result.content

def get_guild_name(guild_id, token):
    result=requests.get(url=f"https://discordapp.com/api/v7/guilds/{guild_id}", headers={"authorization":token})
    return result.json().get("name")

def get_image_file_extension_from_bytes(image_bytes):
    if str(image_bytes)[0:7].find("PNG") != -1:
        return ".png"
    if str(image_bytes)[0:7].find("GIF") != -1:
        return ".gif"
    return ".png"


def save(img_bytes, path):
    imagefile = open(path, 'wb')
    imagefile.write(img_bytes)
    imagefile.close()

def make_server_dir(server, config):
    dir_path = os.path.join(config.get("path"), server)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def try_scraping(guild_name, emoji):
    id = emoji.get("id")
    name = emoji.get("name")
    print(f"Attempting to download :{name}: from {guild_name}")
    emoji_bytes = None
    while True:
        try:
            emoji_bytes = scrape_emoji(id)
        except:
            print(f"Failed to get emoji :{name}: from {guild_name} , retrying!")
        else:
            print(f"Successfully got emoji :{name}: from {guild_name}")
            break
    return emoji_bytes
    

def scrape(config):
    if not os.path.isdir(config.get("path")):
        print("Path in config.json does not exist.")

    servers = config.get("guilds")
    for server in servers:
        emojis = get_list_of_emojis(server, config.get("token"))
        guild_name = get_guild_name(server, config.get("token"))
        make_server_dir(guild_name, config) #TODO technically if the server name had special characters (not-ASCII chars) it's gonna break so add support for that "somehow"
        for emoji in emojis:
            emoji_bytes = try_scraping(guild_name, emoji)
            save(emoji_bytes, os.path.join(config.get("path"), guild_name, (emoji.get("name") + get_image_file_extension_from_bytes(emoji_bytes))))

def main():
    print(info)
    while True:
        config = {"token":"", "guilds":[], "path":os.getcwd()}
        config["token"] = input("Please enter your discord token (https://youtu.be/YEgFvgg7ZPI for help): ")

        while True:
            id = input("Enter the guild/server ID you want to scrape for emojis (when you are done, just press enter, https://youtu.be/6dqYctHmazc for help): ")
            if is_none_empty_whitespace(id): break
            else: config["guilds"].append(id)
        
        file_path = input("Where would you like to save your emojis? (Press enter to use the current directory): ")
        if not is_none_empty_whitespace(file_path):
            config["path"] = file_path
        
        print(config)
        if is_none_empty_whitespace(input("Are these settings correct? (press enter to continue or anything else to cancel): ")):
            if input(warning_info) == "I UNDERSTAND":
                scrape(config)
                print("Thanks for using the discord emoji scraper! You can find your files at-: " + config["path"])
                break
            print("Verification failed.")

main()