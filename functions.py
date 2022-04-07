import config
from datetime import datetime
from discord_webhook import DiscordEmbed, DiscordWebhook

### In the twitch chat we have bots who have moderator permission and so we dont want to know which bot is in the chat we just want users
# This function will remove blacklisted users from config.py file ###
def only_mods(moderators):
    only_moderators = []
    for moderator in moderators:
        if not moderator in config.BLACK_LIST:
            only_moderators.append(moderator)
    return only_moderators



### Update moderators informations like who is in the chat and who is not in the chat and write it in the last_check.txt file ###
def update_mods(moderators):
    new_mods = []
    leaved_mods = []

    last_check_file = open("last_check.txt", "r")
    last_check_mods = last_check_file.readlines()
    last_check_mods_st = ""
    last_check_file.close()

    # Check if a moderator joined to chat
    for moderator in moderators:
        if not moderator in last_check_mods:
            new_mods.append(moderator)
            last_check_mods.append(moderator)

    # Check if a moderator leaved from chat
    for moderator in last_check_mods:
        if not moderator in moderators:
            leaved_mods.append(moderator)
            last_check_mods.remove(moderator)

    # Convert list to string ( I don't remember how we can do it by functions in python :)))) )
    for moderator in last_check_mods:
        last_check_mods_st += moderator + "\n"

    last_check_file = open("last_check.txt", "w")
    last_check_file.write(last_check_mods_st)
    last_check_file.close()

    return new_mods, leaved_mods



### Send a log to Discord for who is joined to chat and who leaved from chat ###
def send_log(updated_mods):
    new_mods = updated_mods[0]
    leaved_mods = updated_mods[1]

    new_mods_st = ""
    leaved_mods_st = ""

    for moderator in new_mods:
        new_mods_st += moderator + "\n"

    for moderator in leaved_mods:
        leaved_mods_st += moderator + "\n"

    webhook = DiscordWebhook(url=config.WEBHOOK_URL)
    embed = DiscordEmbed(title="Live Moderators Log", description=f"**New moderators**:\n{new_mods_st}\n\n**Leaved moderators**:\n{leaved_mods_st}", color=config.EMBED_COLOR)
    webhook.add_embed(embed=embed)

    try:
        webhook.execute()
        return True
    except:
        return False

def write_file_log(updated_mods):
    new_mods = updated_mods[0]
    leaved_mods = updated_mods[1]

    log_file = open("log.txt", "a")
    now = datetime.now()
    strftime = now.strftime("%Y-%m-%d %H:%M:%S")

    for moderator in new_mods:
        log_file.write(f"[ { strftime } ] {moderator} - joined to chat\n")

    for moderator in leaved_mods:
        log_file.write(f"[ { strftime } ] {moderator} - leaved from chat\n")