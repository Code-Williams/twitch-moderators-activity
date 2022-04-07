# Import needed librarys for this side
import requests, time, functions, config

# Create a unlimited loop for checking mods in chat
while True:

    # Get all informations about chat
    users = requests.get(config.API).json()

    # Filter chat informations for moderators only and remove bots who have moderator permission in chat
    moderators = functions.only_mods(users['chatters']['moderators'])

    # Update last check file with new moderators and remove leaved moderators
    update_mods = functions.update_mods(moderators)

    # Send log to Discord for both new moderators and leaved moderators
    sned_log = functions.send_log(update_mods)

    # Go to sleep for 300 seconds (You can change it but i think that's good timer for have not spam request and have good data)
    time.sleep(300)