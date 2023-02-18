#!/usr/bin/env python
import os, time
import re, requests
from apnggif import apnggif
import platform

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

def get_list_of_stickers(guild_id, token):
    result=requests.get(url=f"https://discordapp.com/api/v9/guilds/{guild_id}/stickers", headers={"authorization":token})
    return result.json()

def scrape_sticker(id, proxy=None):
    if is_none_empty_whitespace(proxy):
        result=requests.get(url=f"https://media.discordapp.net/stickers/{id}")
        return result.content

def get_guild_name(guild_id, token):
    result=requests.get(url=f"https://discordapp.com/api/v7/guilds/{guild_id}", headers={"authorization":token})
    if platform.system() == "Windows":
        return re.sub(r"[<>:\"/\\|?*]", '-', result.json().get("name"))
    else:
        return result.json().get("name")  

def save(img_bytes, path):
    imagefile = open(path, 'wb')
    imagefile.write(img_bytes)
    imagefile.close()

def make_server_dir(server, config):
    dir_path = os.path.join(config.get("path"), server)
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def try_scraping(guild_name, sticker):
    id = sticker.get("id")
    name = sticker.get("name")
    print(f"Attempting to download '{name}' from {guild_name}")
    sticker_bytes = None
    while True:
        try:
            sticker_bytes = scrape_sticker(id)
        except Exception as exception:
            if exception == KeyboardInterrupt or exception == SystemExit:
                print("KeyboardInterrupt/SystemExit caught! Terminating.")
                raise
            else:
                print(f"Failed to get emoji '{name}' from {guild_name} , retrying!")
        else:
            print(f"Successfully got emoji '{name}' from {guild_name}")
            break
    return sticker_bytes

def scrape(config):
    if not os.path.isdir(config.get("path")):
        os.mkdir(config.get("path"))
    servers = config.get("guilds")
    for server in servers:
        stickers = get_list_of_stickers(server, config.get("token"))
        guild_name = get_guild_name(server, config.get("token"))
        if guild_name == None or stickers == None:
            print(f"Guild {server} is incorrect/doesn't exist/fail to fetch guild name or stickers.")
            continue
        cooldownsec = config.get("cooldownsec")
        make_server_dir(guild_name, config) #TODO technically if the server name had special characters (not-ASCII chars) it's gonna break so add support for that "somehow"
        count = 0
        print(f"Starting sticker download for server {guild_name}")
        for sticker in stickers:
            if (not config.get("cooldownpersticker") <= 0) & (count >= config.get("cooldownpersticker")):
                print(f"\nCooldown reached! Cooling down for {cooldownsec} seconds.")
                time.sleep(cooldownsec)
                count = 0
                print("Continuing from cooldown\n")
            sticker_bytes = try_scraping(guild_name, sticker)
            if sticker.get("format_type") == 1:
                save(sticker_bytes, os.path.join(config.get("path"), guild_name, (sticker.get("name") + ".png")))
            else:
                if config.get("convertapngtogif"):
                    pathorigin = os.path.join(config.get("path"), guild_name, (sticker.get("name") + "_original.apng"))
                    pathconv = os.path.join(config.get("path"), guild_name, (sticker.get("name") + ".gif"))
                    stickername = sticker.get("name")
                    save(sticker_bytes, pathorigin)
                    apnggif(pathorigin, pathconv)
                    print(f"Converted animated sticker '{stickername} from {guild_name}'")
                else:
                    save(sticker_bytes, os.path.join(config.get("path"), guild_name, (sticker.get("name") + ".apng")))
            count += 1
        print(f"Finished downloading stickers from {guild_name}")

def main():
    print(info)
    while True:
        config = {"token":"", "guilds":[], "path":os.getcwd()+"/Stickers", "cooldownsec":0, "cooldownpersticker":0, "convertapngtogif":False}
        config["token"] = input("Please enter your discord token (https://youtu.be/YEgFvgg7ZPI for help): ")

        while True:
            id = input("Enter the guild/server ID you want to scrape for stickers (when you are done, just press enter, https://youtu.be/6dqYctHmazc for help): ")
            if is_none_empty_whitespace(id): break
            elif not is_int(id): print("Incorrect guild id.")
            else: config["guilds"].append(id)
        
        file_path = input("Where would you like to save your stickers? (Press enter to use the current directory): ")
        if not is_none_empty_whitespace(file_path):
            config["path"] = file_path
        
        cooldownperemoji = input("Enter cooldown trigger per sticker (type nothing or 0 to continue without cooldown): ")
        if (is_int(cooldownperemoji)): config["cooldownpersticker"] = int(cooldownperemoji)

        if config["cooldownpersticker"] != 0:
            cooldownsec = input("Enter the cooldown time in seconds: ")
            if (not is_none_empty_whitespace(cooldownsec)) & (not is_int(cooldownsec)): break
            else: config["cooldownsec"] = int(cooldownsec)
        
        convertapngtogif = input("Would you like to convert apng files (animated stickers) to gif? Leave blank to disable (if this is enabled then original animated sticker files will have '_original' appended between their name and the file extension): ")
        if not is_none_empty_whitespace(convertapngtogif):
            config["convertapngtogif"] = True

        print("\n")
        print(config)
        if is_none_empty_whitespace(input("Are these settings correct? (press enter to continue or anything else to cancel): ")):
            if input(warning_info) == "I UNDERSTAND":
                scrape(config)
                print("Thanks for using the discord emoji scraper! You can find your files at-: " + config["path"])
                break
            print("Verification failed.")

main()
