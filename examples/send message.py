from DiscordAPI import DiscordSession


token = "YOUR_DISCORD_TOKEN"
channel_id = "CHANNEL_ID_TO_SEND"
message = "YOUR_MESSAGE"

user = DiscordSession(token)


response = user.send_message(channel_id, message)

print(response)
