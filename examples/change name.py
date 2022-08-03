from DiscordAPI import DiscordSession


token = "YOUR_DISCORD_TOKEN"
password = "YOUR_DISCORD_PASSWORD"
new_username = "NEW_USERNAME"

user = DiscordSession(token)

response = user.change_username(new_username, password)

print(response)
